# Quizt — プロジェクト仕様書 v2.0
> デザイン確定版（LearningQuizAppUI ハンドオフより）

---

## 1. アーキテクチャ全体像

```
┌─────────────────────────────────────────┐
│  Flutter App                            │
│                                         │
│  ・全画面UI（デザイン確定済み）             │
│  ・ローカル通知スケジュール（flutter_local）│
│  ・Hive（お気に入り・履歴・設定・統計）     │
└──────────────┬──────────────────────────┘
               │ HTTPS / API Gateway
               ▼
           Lambda（Python）
          ［ステートレス］
               │
               ▼
           Bedrock
       （Claude Sonnet）
```

サーバー側は「受け取って・生成して・返す」だけ。状態は一切持たない。

---

## 2. デザイントークン

デザインはすべて `styles.css` の CSS変数に基づく。Flutter では `AppTheme` クラスに集約する。

### カラー（ライトテーマ）

| トークン | 値 | 用途 |
|---|---|---|
| `bg` | `#f7f6f2` | 画面背景 |
| `surface` | `#ffffff` | カード・シート背景 |
| `surface2` | `#f1efe9` | 非アクティブ要素の背景 |
| `ink` | `#1a1714` | メインテキスト |
| `ink2` | `#4a4540` | サブテキスト |
| `ink3` | `#8a847d` | プレースホルダー・ラベル |
| `ink4` | `#c5beb5` | 非アクティブアイコン |
| `line` | `#ece8e0` | 薄いボーダー |
| `line2` | `#e2dcd1` | 通常のボーダー |
| `accent` | `#6c5ce7` | メインアクセント（パープル） |
| `accentSoft` | `#ece9ff` | アクセントの薄い背景 |
| `success` | `#2ec27e` | 正解・成功 |
| `successSoft` | `#d8f3e4` | 正解の薄い背景 |
| `danger` | `#e0535b` | 不正解・エラー |
| `dangerSoft` | `#fde4e6` | 不正解の薄い背景 |
| `warning` | `#f5a623` | 警告 |

### カラー（ダークテーマ）

| トークン | 値 |
|---|---|
| `bg` | `#14120f` |
| `surface` | `#1f1c18` |
| `surface2` | `#26221d` |
| `ink` | `#f5f1ea` |
| `ink2` | `#c8c1b6` |
| `ink3` | `#877f73` |
| `ink4` | `#4a443c` |
| `line` | `#2c2823` |
| `line2` | `#38332c` |
| `accentSoft` | `#3a261d` |

### グラデーション

```
accent gradient:
  155deg, #6c5ce7 → color-mix(accent 70%, #ff7eb6)
  ≈ Flutter: LinearGradient([Color(0xFF6C5CE7), Color(0xFFB06AC4)])
```

### タイポグラフィ

| 用途 | サイズ | ウェイト |
|---|---|---|
| 画面タイトル | 28px | 800 |
| ストリーク数字 | 64px | 800 |
| セクション見出し | 11px | 700・大文字・0.12em letter-spacing |
| 問題文 | 20px | 700 |
| 選択肢テキスト | 15px | 500 |
| 解説テキスト | 14px | 400・line-height 1.75 |
| カードラベル | 11〜13px | 600〜700 |

- 日本語: `Noto Sans JP`
- 数字・英字: `Inter`

### スペーシング・角丸

| トークン | 値 |
|---|---|
| `rSm` | 10px |
| `rMd` | 14px |
| `rLg` | 20px |
| `rXl` | 28px |
| 画面横パディング | 24px |
| カード内パディング | 16〜22px |

### シャドウ

```
shadowSm: 0 1px 2px rgba(20,15,10,.04), 0 1px 1px rgba(20,15,10,.03)
shadowMd: 0 6px 16px rgba(20,15,10,.06), 0 2px 4px rgba(20,15,10,.04)
shadowLg: 0 18px 40px rgba(20,15,10,.10), 0 4px 10px rgba(20,15,10,.05)
```

---

## 3. 画面仕様

### 画面一覧

| # | ID | 画面名 | ボトムタブ |
|---|---|---|---|
| 1 | `home` | ホーム | ホーム |
| 2 | `quiz` | 問題（出題中） | なし |
| 3 | `explain` | 問題（解説） | なし |
| 4 | `explain_goal` | 5問達成モーダル | なし |
| 5 | `category` | カテゴリを選ぶ | カテゴリを選ぶ |
| 6 | `fav` | お気に入り | お気に入り |
| 7 | `history` | 履歴 | 履歴 |
| 8 | `settings` | 設定 | （タブなし・歯車アイコンからアクセス） |

### ボトムナビゲーション

タブは4つ。設定はホーム右上の歯車アイコンから遷移。

| タブID | ラベル | アイコン |
|---|---|---|
| `home` | ホーム | home |
| `category` | カテゴリを選ぶ | grid |
| `fav` | お気に入り | heart |
| `history` | 履歴 | clock |

アクティブタブ: `accent` カラー・strokeWidth `2.0`
非アクティブ: `ink3` カラー・strokeWidth `1.7`
タブバー高さ: `76px`（padding: 8px top / 22px bottom）

---

### 3.1 ホーム画面

**レイアウト構成（上から順）:**

1. **StatusBar**（iOS風・44px）
2. **スクロールエリア**
   - グリーティング（日付・挨拶文）
   - ストリークヒーローカード
   - 今日の目標カード
   - CTAボタン「問題を解く」
   - 2カラム統計カード（正答率・解答数）
3. **TabBar**

**グリーティング:**
```
padding: 12px 24px 16px
日付: fontSize 13, color ink3, fontWeight 500
挨拶: fontSize 26, fontWeight 800, letterSpacing -0.01em
```

**ストリークヒーローカード:**
```
margin: 0 16px 16px
background: accent gradient（155deg）
borderRadius: 24px
padding: 22px
boxShadow: accent 60% 透過

内部構成:
- "STREAK" ラベル（fire icon + テキスト、fontSize 12, opacity .9）
- ストリーク日数（fontSize 64, fontWeight 800, Inter）
- "日連続"（fontSize 16, fontWeight 600）
- 曜日ドット（月〜日、7個）
  - 達成日: 白丸・accentカラーのチェックアイコン
  - 未達成: rgba(255,255,255,.18)の丸
  - 本日: 白ボーダー + 外光輪
```

**今日の目標カード:**
```
background: surface, border: 1px solid line
borderRadius: 22px, padding: 20px 22px
boxShadow: shadowSm

上段: "今日の目標"ラベル + "あとN問でクリア" / 進捗数値（accent色）
下段: 5本のプログレスバー
  - 完了: accent
  - 未完了: surface2
  - height: 8px, borderRadius: 999px
```

**CTAボタン:**
```
height: 58px, borderRadius: 18px, fontSize: 16px
playアイコン + "問題を解く"
未達成時: accent background
達成済み時: accentSoft background / accent text
```

**統計2カラムカード:**
```
display: grid, gridTemplateColumns: 1fr 1fr, gap: 10px
各カード: padding 14px
  - 36x36px accentSoft背景の角丸アイコンボックス（borderRadius: 10px）
  - ラベル（fontSize 11, ink3）
  - 数値（fontSize 18, fontWeight 700, Inter）
左: トロフィーアイコン + "正答率" + "XX%"
右: 本アイコン + "解答数" + "XX"
```

---

### 3.2 問題画面（出題中）

**レイアウト構成:**

1. StatusBar
2. スクロールエリア（padding: 8px 24px 24px）
   - トップバー（閉じるボタン・ハートボタン）
   - カテゴリバッジ
   - 問題カード
   - 選択肢リスト
   - スペーサー
   - 「回答する」ボタン

**トップバー:**
```
display: flex, justifyContent: space-between
閉じるボタン: 40x40px, surface背景, line border, borderRadius 12px
ハートボタン: 透明背景, ink3カラー（お気に入り登録前）
```

**カテゴリバッジ:**
```
display: flex, gap: 10px, alignItems: center
左: 36x36px, accentSoft背景, borderRadius 11px, 絵文字アイコン
右上: カテゴリ名（fontSize 11, ink3, fontWeight 600）
右下: トピック名（fontSize 13, fontWeight 700, accent）
```

**問題カード:**
```
background: surface, border: 1px solid line
borderRadius: 22px, padding: 22px 20px
boxShadow: shadowSm
問題文: fontSize 20, fontWeight 700, lineHeight 1.5, letterSpacing -0.005em
```

**選択肢カード（4状態）:**

| 状態 | border | background | キーバッジ |
|---|---|---|---|
| 通常 | 2px solid line | surface | 透明+line2ボーダー、ink3テキスト |
| 選択中 | 2px solid accent | accentSoft | accent背景・白テキスト |
| 正解 | 2px solid success | successSoft | success背景・白チェック |
| 不正解 | 2px solid danger | dangerSoft | danger背景・白✕ |

```
padding: 14px 16px, gap: 12px
borderRadius: 16px
キーバッジ: 26x26px, borderRadius: 50%
テキスト: fontSize 15, fontWeight 500
```

**回答ボタン:**
```
className: btn block
height: 56px, borderRadius: 18px, fontSize: 16px
```

---

### 3.3 問題画面（解説）

**レイアウト構成:**

1. StatusBar
2. スクロールエリア（padding: 8px 0 24px）
   - 正解バナー（グラデーションカード）
   - 解説エリア
   - NEXTヒントボックス
3. ボトムバー（固定）

**正解バナー:**
```
margin: 0 16px 18px
background: accent gradient
color: white, borderRadius: 24px
padding: 26px 22px 22px
textAlign: center

内部:
- 64x64px 白丸 + accentカラーのチェックアイコン（size:36, stroke:3.2）
- "正解！" fontSize 22, fontWeight 800
- "今日 N / 5 問 達成" fontSize 13, opacity .92
- 装飾: ✦ スパークル（4箇所、opacity .7〜.9）
```

*不正解の場合: 背景を dangerSoft に変更、×アイコン、"不正解" テキスト*

**解説エリア:**
```
padding: 0 24px
"解説" セクションタイトル + お気に入りボタン（横並び）
解説テキスト: fontSize 14, ink2, lineHeight 1.75
  - キーワードに <strong> (ink)
```

**NEXTヒントボックス:**
```
background: accentSoft, borderRadius: 16px, padding: 16px
display: flex, gap: 12px
💡絵文字 + "NEXT"ラベル（fontSize 12, fontWeight 700, accent）
  + "〇〇についても調べてみてください。"（fontSize 13, ink）
```

**ボトムバー（固定）:**
```
padding: 12px 24px 16px
borderTop: 1px solid line, background: surface
display: flex, gap: 10px

左: "ホームに戻る"ボタン（ghost、flex: 0 0 auto、padding: 0 18px、fontSize: 13）
右: "次の問題 →"ボタン（primary、flex: 1、height: 52px、borderRadius: 16px）
```

---

### 3.4 5問達成モーダル

ベース画面（解説画面）の上にオーバーレイとして表示。

**オーバーレイ:**
```
position: absolute, inset: 0
background: rgba(15,12,9,.55)
backdropFilter: blur(2px)
display: flex, alignItems: center
padding: 0 28px
```

**モーダルカード:**
```
background: surface, borderRadius: 28px
width: 100%, padding: 32px 24px 22px
textAlign: center
boxShadow: 0 30px 80px rgba(0,0,0,.4)

装飾スパークル: ✨🎉✦⭐（4箇所に絶対配置）

トロフィーアイコン: 88x88px 円形グラデーション背景
  boxShadow: accent 70% 透過の輝き

"今日の目標達成！" fontSize 24, fontWeight 800
"5問すべて解きました 🎉" + ストリーク日数（accent bold）
  fontSize 14, ink3, lineHeight 1.6

達成ドット: 5個
  - 32x32px、accent背景、白チェックアイコン（size:16, stroke:3.2）

ボタン:
  "ホームに戻る"（primary block、height: 52px）
  "もう少し続ける"（ghost block、height: 44px、fontSize: 13）
```

---

### 3.5 カテゴリ画面

**レイアウト:**
1. StatusBar
2. スクロールエリア（padding: 8px 24px 24px）
   - タイトル・サブタイトル
   - 2カラムグリッド（カテゴリカード）
   - 「全カテゴリからおまかせ」バナー
3. TabBar

**カテゴリカード（グリッド）:**
```
display: grid, gridTemplateColumns: 1fr 1fr, gap: 12px

各カード:
  padding: 16px, borderRadius: 20px
  background: surface, border: 1px solid line
  boxShadow: shadowSm, minHeight: 130px
  display: flex, flexDirection: column

  アイコンボックス: 44x44px, borderRadius: 14px
    background: カテゴリカラー + "24"（透明度）
    fontSize: 22（絵文字）
  カテゴリ名: fontSize 14, fontWeight 700
  正答率バー: height 4px, borderRadius 999px
    達成部分: カテゴリカラー
    未達成: surface2
  正答率数値: fontSize 11, ink3, fontWeight 700（Inter）
```

**カテゴリ定義（ハードコード）:**

| ID | 名前 | アイコン | カラー |
|---|---|---|---|
| `network` | ネットワーク | 🌐 | `#5ec3ff` |
| `os` | OS・Linux | 🐧 | `#ffb35e` |
| `security` | セキュリティ | 🔒 | `#ff7e9a` |
| `db` | DB | 🗄 | `#7bd88f` |
| `cloud` | クラウド | ☁️ | `#a78bfa` |
| `programming` | プログラミング | ⚙️ | `#ffd166` |
| `dev` | 開発プロセス | 🔧 | `#ffb35e` |

**おまかせバナー:**
```
marginTop: 18px, padding: 16px, borderRadius: 16px
background: accentSoft
shuffleアイコン（accent） + "全カテゴリからおまかせ"（fontSize 14, fontWeight 600, accent）
+ chevron-rightアイコン
```

---

### 3.6 お気に入り画面

**レイアウト:**
1. StatusBar
2. スクロールエリア（padding: 8px 0 24px）
   - タイトル・サブタイトル
   - カテゴリフィルタータブ（横スクロール）
   - お気に入りカードリスト
3. TabBar

**カテゴリフィルタータブ:**
```
display: flex, gap: 8px, padding: 0 24px 14px, overflowX: auto

アクティブ: accent背景・白テキスト・borderなし
非アクティブ: surface背景・ink2テキスト・line border
padding: 8px 14px, borderRadius: 999px, fontSize: 12, fontWeight: 600
```

**お気に入りカード:**
```
className: card
padding: 16px, position: relative

左端アクセントバー:
  position: absolute, left: 0, top: 14px, bottom: 14px, width: 3px
  background: カテゴリカラー, borderRadius: 0 3px 3px 0

上段: カテゴリ+トピック（fontSize 11, カテゴリカラー, fontWeight 700）
     + heart-fillアイコン（accent）
下段: 問題文（fontSize 14, fontWeight 600, lineHeight 1.5）
```

---

### 3.7 履歴画面

**レイアウト:**
1. StatusBar
2. スクロールエリア（padding: 8px 0 24px）
   - タイトル・サブタイトル
   - 総合正答率カード
   - カテゴリ別正答率リスト
3. TabBar

**総合正答率カード:**
```
background: accent gradient, color: white
borderRadius: 24px, padding: 22px
display: flex, alignItems: center, gap: 20px

左: 90x90px 円形進捗リング（conic-gradient）
  内側: accentカラーの円 + 正答率数値（fontSize 22, fontWeight 800, Inter）

右:
  "OVERALL"（fontSize 11, fontWeight 700, opacity .9, letterSpacing .08em）
  解答数・期間（fontSize 15, fontWeight 700）
  先月比（fontSize 12, opacity .92, fontWeight 600）
```

**カテゴリ別正答率:**
```
各行:
  上段: カテゴリ名（fontSize 13, fontWeight 600）
        + 正答率（カテゴリカラー, fontWeight 700, Inter）・問数（ink3）
  下段: 横バー（height 8px, borderRadius 999px）
    達成部分: カテゴリカラー
    未達成: surface2
```

---

### 3.8 設定画面

**レイアウト:**
1. StatusBar
2. スクロールエリア（padding: 8px 0 24px）
   - タイトル "設定"
   - セクション別設定カード
3. TabBar（homeタブ active のまま、またはタブなしで歯車からアクセス）

**設定行コンポーネント（Row）:**
```
display: flex, alignItems: center, gap: 14px, padding: 14px 16px

左アイコン: 36x36px, accentSoft背景, accent色, borderRadius 10px
中央: タイトル（fontSize 14, fontWeight 600）+ 説明（fontSize 12, ink3）
右: トグルまたはchevron-right
```

**トグルスイッチ:**
```
width: 46px, height: 28px, borderRadius: 999px
ON: accent背景
OFF: line2背景
つまみ: 24x24px 白丸、left: ON=20px / OFF=2px
boxShadow: 0 2px 4px rgba(0,0,0,.2)
```

**セクション構成:**

| セクション | 項目 |
|---|---|
| 通知 | プッシュ通知（トグル）/ 朝の通知 7:00（トグル）/ 夜の通知 21:00（トグル） |
| 学習 | 1日の目標（chevron）/ 出題カテゴリ（chevron） |
| 表示 | ダークモード（トグル） |
| その他 | 利用規約（chevron）/ バージョン（テキスト） |

---

## 4. バックエンド仕様

### APIエンドポイント

**POST `/generate-question`**

リクエスト:
```json
{
  "category": "network",
  "format": "choice",
  "exclude_topics": ["TLS/HTTPS", "DNS"]
}
```

レスポンス:
```json
{
  "question": "HTTPSにおいてTLS証明書が果たす役割は何ですか？",
  "format": "choice",
  "choices": [
    "通信の暗号化",
    "DNSの名前解決",
    "IPアドレスの割り当て",
    "パケットのルーティング"
  ],
  "answer": "通信の暗号化",
  "explanation": "TLS証明書は、サーバーの正当性を保証し...",
  "further_study": "公開鍵暗号方式についても調べてみてください。",
  "topic": "TLS/HTTPS"
}
```

### Bedrockプロンプト構造（Lambda内）

```
あなたはITエンジニア向け学習クイズの出題者です。

【カテゴリ】{category_name}
【カテゴリ説明】{category_description}
【形式】四択選択式
【除外トピック】{exclude_topics}（重複しないトピックで出題）

【要件】
- 実務で役立つエンジニア必須知識
- 初級〜中級レベル
- 問題・解説・さらに学ぶトピックをJSON形式で返すこと
- JSONのみ返すこと（前置き不要）
- further_studyは必ず「〇〇についても調べてみてください。」の形式で

【出力形式】
{
  "question": "...",
  "choices": ["...", "...", "...", "..."],
  "answer": "...",
  "explanation": "...(200-300字)",
  "further_study": "〇〇についても調べてみてください。",
  "topic": "..."
}
```

### カテゴリ定義（Lambda内で管理）

```python
CATEGORIES = {
  "network": {
    "name": "ネットワーク基礎",
    "description": "TCP/IP、HTTP/HTTPS、DNS、TLS、ロードバランサーなどネットワーク全般"
  },
  "os": {
    "name": "OS・Linux",
    "description": "プロセス管理、ファイルシステム、パーミッション、シェルコマンド、カーネル"
  },
  "security": {
    "name": "セキュリティ",
    "description": "認証・認可、暗号化、主要脆弱性（OWASP）、セキュリティベストプラクティス"
  },
  "db": {
    "name": "データベース",
    "description": "RDB/NoSQL、インデックス、トランザクション、正規化、SQL"
  },
  "cloud": {
    "name": "クラウド・インフラ",
    "description": "AWS/GCP基礎、IaC、コンテナ（Docker/k8s）、CI/CD"
  },
  "programming": {
    "name": "プログラミング基礎",
    "description": "アルゴリズム、データ構造、計算量、オブジェクト指向、設計パターン"
  },
  "dev": {
    "name": "開発プロセス",
    "description": "Git、アジャイル・スクラム、テスト手法、コードレビュー"
  }
}
```

---

## 5. Flutter ローカルストレージ（Hive）

### Box構成

**`favorites_box`**
```dart
key: questionHash（SHA256の先頭16文字）
value: {
  question: String,
  format: String,       // "choice" | "text"
  choices: List<String>,
  answer: String,
  explanation: String,
  furtherStudy: String,
  topic: String,
  category: String,
  savedAt: DateTime,
}
```

**`history_box`**
```dart
key: autoIncrement
value: {
  question: String,
  answer: String,
  userAnswer: String,
  isCorrect: bool,
  category: String,
  topic: String,
  answeredAt: DateTime,
}
```

**`settings_box`**
```dart
"daily_goal": int,           // デフォルト: 5
"notify_morning": bool,      // デフォルト: true
"notify_evening": bool,      // デフォルト: true
"dark_mode": bool,           // デフォルト: false
"recent_topics": Map<String, List<String>>
  // カテゴリ別・直近10トピック
  // 例: {"network": ["TLS/HTTPS", "DNS"], "db": ["B+木"]}
```

**`stats_box`**
```dart
"streak": int,               // 現在の連続日数
"streak_last_date": String,  // "2026-05-02"
"today_count": int,          // 本日の解答数
"today_date": String,        // "2026-05-02"
"total_count": int,          // 累計解答数
"correct_count": int,        // 累計正解数
"category_stats": Map<String, Map<String, int>>
  // 例: {"network": {"total": 24, "correct": 18}}
```

---

## 6. ローカル通知

`flutter_local_notifications` で初回起動時にスケジュール登録。

```dart
// 朝7:00
NotificationDetails(
  id: 1,
  title: "☀️ 今日の朝のクイズ",
  body: "今日も5問チャレンジしよう！",
  scheduledTime: Time(7, 0, 0),
  repeatInterval: RepeatInterval.daily,
)

// 夜21:00
NotificationDetails(
  id: 2,
  title: "🌙 今日の夜のクイズ",
  body: "1日の締めくくりに学習しよう。",
  scheduledTime: Time(21, 0, 0),
  repeatInterval: RepeatInterval.daily,
)
```

通知タップ → アプリ起動 → ランダムカテゴリで即問題生成

---

## 7. 問題生成フロー（Flutter ↔ Lambda）

```
Flutter                              Lambda / Bedrock
  │                                        │
  │ 1. recent_topicsをHiveから取得          │
  │ 2. POST /generate-question ──────────▶│
  │    {category, format,                 │ プロンプト組み立て
  │     exclude_topics}                   │      ↓
  │                                        │ Bedrock呼び出し
  │                                        │      ↓
  │◀─── JSON（問題・解説・topic） ─────── │ レスポンス整形
  │
  │ 3. topicをsettings_boxのrecent_topicsに追記
  │ 4. 問題画面に遷移・表示
  │
  │ （回答後）
  │ 5. 正誤をhistory_boxに保存
  │ 6. stats_boxを更新（today_count, streak等）
  │ 7. today_count === daily_goalなら達成モーダル表示
```

---

## 8. 技術スタック

| レイヤー | 技術 | 備考 |
|---|---|---|
| フロントエンド | Flutter | iOS / Android |
| ローカルDB | Hive | お気に入り・履歴・設定・統計 |
| 通知 | flutter_local_notifications | ローカルスケジュール |
| HTTPクライアント | dio または http | API呼び出し |
| 状態管理 | Riverpod または Provider | （チーム判断） |
| APIエンドポイント | Amazon API Gateway | HTTPS |
| サーバー処理 | AWS Lambda（Python） | ステートレス |
| AI問題生成 | Amazon Bedrock（Claude Sonnet） | |
| 認証 | なし（MVP） | フェーズ3でCognito追加 |
| サーバーDB | なし（MVP） | フェーズ3でDynamoDB追加 |

---

## 9. フェーズ別ロードマップ

### フェーズ1（MVP）
- 四択問題のみ
- カテゴリ選択・ランダム出題
- ローカル通知（朝・夜）
- お気に入り・履歴・統計（ローカル）
- デイリー目標5問・ストリーク
- ライトテーマのみ

### フェーズ2
- テキスト入力式問題
- ダークテーマ切り替え
- 間違えた問題の復習モード
- 1日の目標問題数カスタマイズ
- 出題カテゴリ絞り込み設定

### フェーズ3
- サーバーDB追加（Cognito + DynamoDB）
- 機種変・複数端末対応
- ユーザー独自テーマ設定
- 学習レポート・詳細統計
