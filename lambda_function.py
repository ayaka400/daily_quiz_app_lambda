import json
import boto3

bedrock = boto3.client("bedrock-runtime", region_name="ap-northeast-1")

def lambda_handler(event, context):
    response = bedrock.invoke_model(
        modelId="arn:aws:bedrock:ap-northeast-1:884574952891:inference-profile/jp.anthropic.claude-sonnet-4-5-20250929-v1:0",
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [
                {"role": "user", "content": "ITクイズを1問、JSON形式で作ってください。"}
            ]
        })
    )
    result = json.loads(response["body"].read())

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": result["content"][0]["text"]
    }