import json
import boto3
import time

# Clients
bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1'  # Change to your Bedrock region
)

dynamodb = boto3.resource(
    service_name='dynamodb',
    region_name='eu-north-1'  # Change to your DynamoDB region
)

# DynamoDB table
table = dynamodb.Table('chat-history')

def lambda_handler(event, context):

    # Get user message and session ID
    user_message = event.get('message', 'Hello!')
    session_id   = event.get('session_id', 'default-session')

    # Step 1: Load chat history from DynamoDB
    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('session_id').eq(session_id)
    )

    # Build messages list from history
    chat_history = []
    for item in response['Items']:
        chat_history.append({"role": "user",      "content": item['user_message']})
        chat_history.append({"role": "assistant", "content": item['ai_reply']})

    # Add new message
    chat_history.append({"role": "user", "content": user_message})

    # Step 2: Call Bedrock with full history
    bedrock_response = bedrock.invoke_model(
        modelId='us.anthropic.claude-sonnet-4-20250514-v1:0',
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 500,
            "messages": chat_history
        })
    )

    response_body = json.loads(bedrock_response['body'].read())
    ai_reply = response_body['content'][0]['text']

    # Step 3: Save new conversation to DynamoDB
    table.put_item(
        Item={
            'session_id':   session_id,
            'timestamp':    str(int(time.time())),
            'user_message': user_message,
            'ai_reply':     ai_reply
        }
    )

    # Step 4: Return response
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message':    ai_reply,
            'session_id': session_id
        })
    }
