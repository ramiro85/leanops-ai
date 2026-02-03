import json
import boto3
import urllib.parse
from datetime import datetime
from decimal import Decimal

# Initialize the clients outside the handler for better performance (Warm Starts)
textract = boto3.client('textract', region_name='us-east-1')
bedrock = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('ExtractedRatesConf')


def lambda_handler(event, context):
    # 1. Get S3 details and handle spaces/special characters in file names
    bucket = event['Records'][0]['s3']['bucket']['name']
    raw_key = event['Records'][0]['s3']['object']['key']
    key = urllib.parse.unquote_plus(raw_key)

    try:
        # 2. Extract text from PDF using Textract
        textract_response = textract.detect_document_text(
            Document={'S3Object': {'Bucket': bucket, 'Name': key}}
        )

        extracted_text = ""
        for block in textract_response['Blocks']:
            if block['BlockType'] == 'LINE':
                extracted_text += block['Text'] + "\n"

        print("Textract: Text extracted successfully.")

        # 3. Use the extracted text for Bedrock
        prompt = (
            "You are an expert Logistics Dispatcher. Your goal is to extract structured data from this Rate Confirmation / BOL. "
            "CRITICAL: Locate the 'Load Number(reference_number)'. It may be labeled as 'Load #', 'PO #', 'Ref #', 'Shipment ID' or 'Control Number'. "
            "Look at the top right and top left headers specifically for this ID. "

            "Extract the following fields precisely: "
            "1. reference_number (The primary identification number) "
            "2. rate (The base linehaul rate) "
            "3. total_amount (Total including fuel/accessorials) "
            "4. broker (Company name) "
            "5. trailer_type (e.g., Van, Reefer, Flatbed) "
            "6. pickup_location (City, State) "
            "7. delivery_location (City, State) "
            "8. pickup_date (YYYY-MM-DD) "
            "9. delivery_date (YYYY-MM-DD) "
            "10. pickup_mode (FSFS or Appt) "
            "11. delivery_mode (FSFS or Appt) "

            "If a field is missing, use null. "
            "RETURN ONLY A FLAT JSON VALID OBJECT. NO MARKDOWN. NO CONVERSATION."
        )

        model_id = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"
        bedrock_response = bedrock.converse(
            modelId=model_id,
            messages=[{
                "role": "user",
                "content": [{"text": f"{prompt}\n\nText: {extracted_text}"}]
            }],
            inferenceConfig={"maxTokens": 1000, "temperature": 0}  # Increased maxTokens for logistics data
        )

        # 4. Clean and Parse the JSON
        ai_json = bedrock_response['output']['message']['content'][0]['text']

        # Strip markdown if present
        if ai_json.startswith("```"):
            ai_json = ai_json.split("```json")[-1].split("```")[0].strip()

        # THE FIX: Tell json.loads to use Decimal for any numbers it finds
        extracted_data = json.loads(ai_json, parse_float=Decimal)

        # Clean up any potential 'null' or empty strings that should be numbers
        if extracted_data.get('total_amount') == "":
            extracted_data['total_amount'] = Decimal('0.00')

        # 5. Enrich the data
        extracted_data['processed_at'] = datetime.now().isoformat()
        extracted_data['s3_url'] = f"https://{bucket}[.s3.amazonaws.com/](https://.s3.amazonaws.com/){key}"

        # Ensure your Partition Key is present! 
        # If your table's key is 'reference_number', ensure the AI found one.
        if 'reference_number' not in extracted_data:
            extracted_data['reference_number'] = f"UNKNOWN-{datetime.now().strftime('%Y%m%d%H%M')}"

        # 6. Push to DynamoDB
        table.put_item(Item=extracted_data)

        print(f"Success: Saved load {extracted_data.get('reference_number')} to DynamoDB.")
        return {"status": "success", "data": extracted_data}


    except Exception as e:
        print(f"Error occurred: {str(e)}")
        # This ensures you know EXACTLY what failed in the logs
        return {'statusCode': 500, 'body': f"Failed: {str(e)}"}