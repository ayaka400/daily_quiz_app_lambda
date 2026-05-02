"""
Bedrock へ送るプロンプトを組み立てるモジュール。
"""

from config import CATEGORIES

# 出力フォーマットの定義（プロンプト本文と分離して管理しやすくする）
OUTPUT_FORMAT = """\
{
  "question": "...",
  "choices": ["...", "...", "...", "..."],
  "answer": "...",
  "explanation": "...(200-300字)",
  "further_study": "〇〇についても調べてみてください。",
  "topic": "..."
}\
"""

PROMPT_TEMPLATE = """\
あなたはITエンジニア向け学習クイズの出題者です。
【カテゴリ】{category_name}
【カテゴリ説明】{category_description}
【形式】四択選択式
【除外トピック】{exclude_str}（これらと重複しないトピックで出題すること）
【要件】
- 実務で役立つエンジニア必須知識
- 初級〜中級レベル
- JSONのみ返すこと（前置き・説明文は不要）
- further_studyは必ず「〇〇についても調べてみてください。」の形式で
【出力形式】
{output_format}
"""


def build_prompt(category_id: str, exclude_topics: list[str]) -> str:
    cat = CATEGORIES.get(category_id, CATEGORIES["network"])
    exclude_str = "、".join(exclude_topics) if exclude_topics else "なし"
    return PROMPT_TEMPLATE.format(
        category_name=cat["name"],
        category_description=cat["description"],
        exclude_str=exclude_str,
        output_format=OUTPUT_FORMAT,
    )