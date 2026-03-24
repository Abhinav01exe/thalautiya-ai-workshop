# Day 2 — Backend: DynamoDB + API Gateway

## 🎯 Goal
Connect the full backend — store chat history in DynamoDB and expose a REST API via API Gateway.

## ✅ What You Will Build
By end of Day 2, you will have:
- Chat history saved in DynamoDB
- A live REST API accessible from anywhere

---

## 🛠️ Step-by-Step Setup

### Step 1 — Add DynamoDB Permission to IAM Role
1. IAM → Roles → `ai-lambda-role`
2. **"Add permissions"** → **"Attach policies"**
3. Search: `AmazonDynamoDBFullAccess` → ✅ Add

---

### Step 2 — Create DynamoDB Table
1. AWS Console → **DynamoDB** → **"Create table"**
2. Settings:
   - Table name: `chat-history`
   - Partition key: `session_id` (String)
   - Sort key: `timestamp` (String)
3. Leave rest as default → **"Create table"**

---

### Step 3 — Update Lambda Code
1. Lambda → `ai-assistant` → **Code** tab
2. Replace with code from `lambda_function.py`
3. Update `region_name` for DynamoDB to match your DynamoDB region
4. Click **"Deploy"**

---

### Step 4 — Create API Gateway
1. AWS Console → **API Gateway** → **"Create API"**
2. Select **REST API** → **"Build"**
3. Settings:
   - API name: `ai-assistant-api`
   - Endpoint type: `Regional`
4. Click **"Create API"**

---

### Step 5 — Create Resource and Method
1. **Resources** → **"Create resource"**
   - Resource name: `chat`
   - Enable CORS: ✅
2. Select `/chat` → **"Create method"**
   - Method: `POST`
   - Integration: `Lambda function`
   - Lambda: `ai-assistant`

---

### Step 6 — Enable CORS
1. Select `/chat` → **"Enable CORS"**
2. Access-Control-Allow-Origin: `*`
3. Methods: ✅ POST, ✅ OPTIONS
4. Click **"Save"**

---

### Step 7 — Deploy API
1. Click **"Deploy API"**
2. Stage: `*New stage*` → name: `prod`
3. Click **"Deploy"**
4. Copy the **Invoke URL** — you will need this!

---

### Step 8 — Test
Use Hoppscotch (hoppscotch.io) or any API tool:
- Method: `POST`
- URL: `YOUR_INVOKE_URL/chat`
- Body:
```json
{
  "message": "What is cloud computing?",
  "session_id": "user-123"
}
```

---

## 📦 Files
- `lambda_function.py` — Updated Lambda with DynamoDB support

---

## 🔑 Key Concepts Learned
- DynamoDB — NoSQL database on AWS
- How to store and retrieve conversation history
- API Gateway — creating REST APIs
- CORS — allowing browser requests
