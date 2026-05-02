import json
import boto3

from config  import AWS_REGION, BEDROCK_MODEL_ID, MAX_TOKENS, DEFAULT_CATEGORY
from prompts import build_prompt

bedrock = boto3.client("bedrock-runtime", region_name=AWS_REGION)


def _invoke_bedrock(prompt: str) -> dict:
    """Bedrock を呼び出し、パース済みの dict を返す。"""
    response = bedrock.invoke_model(
        modelId=BEDROCK_MODEL_ID,
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": MAX_TOKENS,
            "messages": [{"role": "user", "content": prompt}],
        }),
    )
    raw  = json.loads(response["body"].read())
    text = raw["content"][0]["text"].strip()

    # 前後に余分なテキストがある場合の保険
    start = text.find("{")
    end   = text.rfind("}") + 1
    return json.loads(text[start:end])


def lambda_handler(event, context):
    body     = json.loads(event.get("body") or "{}")
    category = body.get("category", DEFAULT_CATEGORY)
    exclude  = body.get("exclude_topics", [])

    prompt        = build_prompt(category, exclude)
    question_json = _invoke_bedrock(prompt)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",  # Flutter からの呼び出し許可
        },
        "body": json.dumps(question_json, ensure_ascii=False),
    }