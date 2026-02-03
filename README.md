# 🚀 LeanOps — AI-Powered Document Intelligence Pipeline

**LeanOps** is a serverless, event-driven document processing pipeline designed to help small businesses **eliminate manual data entry** using AI.

It automatically converts unstructured PDFs (invoices, contracts, applications) into clean, structured data — with **no servers to manage** and **near-zero operational overhead**.

---

## 💡 The Problem

Small companies often waste **10+ hours per week** manually entering data from PDFs into spreadsheets.

- Hiring human operators is expensive and does not scale  
- Traditional OCR software breaks on varying document layouts  
- Inconsistent vendor formats lead to errors and rework  

---

## ✅ The Solution

LeanOps uses **AWS serverless services and LLM reasoning** to extract, understand, and structure data from messy PDFs automatically.

**Key benefits:**

- 💸 **Cost:** ~**$0.01 per document**
- ⚙️ **Maintenance:** Zero server management
- ⚡ **Speed:** From upload to database in **< 10 seconds**
- 🧠 **Intelligence:** Uses AI reasoning, not rigid templates

---

## 🛠️ Tech Stack

- **AWS Lambda** – Orchestrates the event-driven workflow  
- **Amazon Textract** – Extracts raw text from complex PDF layouts  
- **Amazon Bedrock (Claude 3.5 Sonnet)** – Parses text into clean, structured JSON  
- **Amazon DynamoDB** – Stores extracted data for analytics and dashboards  
- **Amazon S3** – Entry point and trigger for the automation pipeline  

---

## 🏗️ Architecture

1. PDF uploaded to **S3**
2. S3 event triggers **Lambda**
3. Lambda calls **Textract** for text extraction
4. Extracted text is passed to **Bedrock (LLM)** for semantic parsing
5. Clean JSON is stored in **DynamoDB**
6. Data becomes immediately available for downstream systems

---

## 🚀 Quick Start

```bash
git clone https://github.com/ramiro85/leanops-ai
cd leanops-ai

# Build the project (use-container ensures dependencies match Lambda's environment)
sam build --use-container

# Deploy the stack (first time use --guided)
sam deploy --guided
