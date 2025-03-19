# Chatbot-Kopiloto

## https://github.com/Ivan252512/chatbot-kopiloto

This project implements a chatbot based on OpenAI GPT-4 that debates and maintains its stance in each conversation. It is deployed on AWS Lambda using Serverless Framework and stores conversation history in DynamoDB.

## 📌 Prerequisites

Before deploying the service, ensure you have installed:
- **Python 3.8+**
- **Node.js and npm**
- **AWS CLI configured** with a profile that has permissions for Secrets Manager and DynamoDB
- **Serverless Framework installed** (`npm install -g serverless`)

You also need to create and export the following environment variables before executing `make secrets`:
```sh
export SERVERLESS_ACCESS_KEY="your_serverless_access_key"
export OPENAI_ORG="your_openai_org"
export OPENAI_API_KEY="your_openai_api_key"
```

---

## 🚀 Service Deployment
The chatbot is deployed on **AWS Lambda** and uses **DynamoDB** to store conversation history.

### **1️⃣ Install Dependencies**
```sh
make install
```
This will install:
- Python dependencies defined in `requirements.txt`
- Serverless Framework and its plugins

### **2️⃣ Create Secrets in AWS**
```sh
make secrets
```
This command creates secrets in **AWS Secrets Manager**:
- `ServerlessAccessKey`
- `OPENAI_ORG`
- `OPENAI_API_KEY`

If the secrets already exist, it will display a message indicating that they are already created.

### **3️⃣ Deploy to AWS**
```sh
make deploy
```
This uploads the code to AWS Lambda, creates the DynamoDB table, and configures the API Gateway.

---

## 📌 Testing and Usage

### **4️⃣ Run Tests**
```sh
make test
```
Runs the tests defined in `tests/` using `pytest`.

### **5️⃣ Remove Deployment**
```sh
make remove
```
Deletes the Lambda function and the AWS API.

### **6️⃣ Clean Local Environment**
```sh
make clean
```
Removes temporary files and cache directories.

---

## 📌 Using the API (THE URL IS FULLY FUNCTIONAL)

You can interact with the chatbot using **cURL**.

### **Start a New Conversation**
```sh
curl --location 'https://l90i2qvjka.execute-api.us-east-1.amazonaws.com/stg/chatbot/discuss' \
--header 'Content-Type: application/json' \
--data '{
    "conversation_id": null,
    "message": "El agua moja"
}'
```
**Expected Response:**
```json
{
    "conversation_id": "8c9af6ee-2223-4ac3-899e-9fce5aec9c51",
    "message": [
        {"role": "user", "content": "El agua moja"},
        {"role": "bot", "content": "No estoy de acuerdo. El agua en sí misma no puede estar mojada..."}
    ]
}
```

### **Continue a Conversation**
```sh
curl --location 'https://l90i2qvjka.execute-api.us-east-1.amazonaws.com/stg/chatbot/discuss' \
--header 'Content-Type: application/json' \
--data '{
    "conversation_id": "8c9af6ee-2223-4ac3-899e-9fce5aec9c51",
    "message": "Como no va a mojar, entonces que hace?"
}'
```
**Expected Response:**
```json
{
    "conversation_id": "8c9af6ee-2223-4ac3-899e-9fce5aec9c51",
    "message": [
        {"role": "user", "content": "El agua moja"},
        {"role": "bot", "content": "No estoy de acuerdo. El agua en sí misma no puede estar mojada..."},
        {"role": "user", "content": "Como no va a mojar, entonces que hace?"},
        {"role": "bot", "content": "El agua es un líquido que sirve para hidratar, limpiar, transportar nutrientes..."}
    ]
}
```

---

## 🎯 **Conclusion**
This chatbot is designed to **maintain its stance in a discussion**, storing the history in **DynamoDB**. The service is **serverless**, scalable, and easy to deploy.

