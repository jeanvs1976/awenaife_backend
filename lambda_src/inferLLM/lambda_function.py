import json
import boto3
import os
from openai import OpenAI

s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket_name = os.environ.get("BUCKET_NAME") 
    prompt_file_key = os.environ.get("PROMPT_FILE") 
    openai_api_key  = os.environ.get("OPENAI_API_KEY")
    client = OpenAI(api_key=openai_api_key)

    try:
        s3_response_p = s3.get_object(Bucket=bucket_name, Key=prompt_file_key)
        prompt = s3_response_p['Body'].read().decode('utf-8')
        
        parsed_body = json.loads(event['body'])
        input_value = parsed_body['input']
        
        response_body = client.chat.completions.create(
            model="gpt-4o-mini",
            messages = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": input_value}
            ]
        )
        response_text = response_body.choices[0].message.content
        
        return {
            'statusCode': 200,
            'body': json.dumps({"Answer": response_text})
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({"Error": str(e)})
        }
