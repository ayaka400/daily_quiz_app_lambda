import os

# --- AWS / Bedrock ---
AWS_REGION   = os.environ.get("AWS_REGION", "ap-northeast-1")
BEDROCK_MODEL_ID = os.environ.get("BEDROCK_MODEL_ID", "arn:aws:bedrock:ap-northeast-1:884574952891:inference-profile/jp.anthropic.claude-sonnet-4-5-20250929-v1:0")
MAX_TOKENS   = int(os.environ.get("MAX_TOKENS", "1000"))

# --- カテゴリ定義 ---
CATEGORIES = {
    "network":     {"name": "ネットワーク基礎",   "description": "TCP/IP、HTTP/HTTPS、DNS、TLS、ロードバランサーなど"},
    "os":          {"name": "OS・Linux",          "description": "プロセス管理、ファイルシステム、パーミッション、シェルコマンド"},
    "security":    {"name": "セキュリティ",        "description": "認証・認可、暗号化、主要脆弱性（OWASP）、ベストプラクティス"},
    "db":          {"name": "データベース",        "description": "RDB/NoSQL、インデックス、トランザクション、SQL"},
    "cloud":       {"name": "クラウド・インフラ",  "description": "AWS/GCP基礎、IaC、コンテナ（Docker/k8s）、CI/CD"},
    "programming": {"name": "プログラミング基礎",  "description": "アルゴリズム、データ構造、計算量、設計パターン"},
    "dev":         {"name": "開発プロセス",        "description": "Git、アジャイル・スクラム、テスト手法、コードレビュー"},
}

DEFAULT_CATEGORY = os.environ.get("DEFAULT_CATEGORY", "network")