🚀 LeanOps: AI-Powered Document Intelligence Pipeline
Built to help small businesses eliminate manual data entry through Serverless AI.

💡 The Problem
Small companies often waste 10+ hours a week manually entering data from PDFs (invoices, contracts, applications) into spreadsheets. Hiring a human for this is expensive; traditional software is too rigid to handle different document layouts.

✅ The Solution
An event-driven, serverless pipeline that uses Amazon Bedrock and Textract to "read" unstructured PDFs and convert them into structured data automatically.

Cost: ~$0.01 per document.

Maintenance: Zero server management.

Speed: From upload to database in < 10 seconds.

🛠️ Tech Stack
AWS Lambda: Orchestrates the flow.

Amazon Textract: Extracts raw text from complex PDF layouts.

Amazon Bedrock (Claude 3.5 Sonnet): Intelligently parses text into clean JSON.

Amazon DynamoDB: Stores extracted data for dashboarding.

Amazon S3: Trigger-point for the automated workflow.

🏗️ Architecture
🚀 Quick Start
Clone the repo: git clone https://github.com/ramiro85/leanops-ai

Deploy: Use the provided CloudFormation template to spin up the S3 bucket and Lambda.

Configure: Request model access in the Amazon Bedrock console.

Test: Drop a messy invoice PDF into the inbox/ folder in S3.

📊 Business Impact
Headcount Efficiency: One operations manager can now handle 5x the volume of documents.

Scalability: Handles 1 document or 10,000 documents with the same codebase.

Accuracy: Uses LLM reasoning to identify "Total Amount Due" even if the label varies across vendors.

**Cost Breakdown**
At current AWS rates, processing 1,000 invoices costs less than a cup of coffee. Compare that to 20 hours of manual labor at $20/hr ($400).
