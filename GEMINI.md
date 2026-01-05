# Bookkeeper プロジェクト用 Gemini コンテキスト

## 1. プロジェクト概要
**Bookkeeper** は、日本の青色申告に対応した複式簿記用のコマンドラインインターフェース（CLI）ツールです。ユーザーは仕訳の入力、仕訳帳の閲覧、および元帳の生成を行うことができます。

**主な機能:**
*   **複式簿記:** 借方と貸方の金額が常に一致することを保証します。
*   **仕訳帳 (Journaling):** 日々の取引を記録します。
*   **元帳生成 (Ledger Generation):** 勘定科目ごとに取引を集計します。
*   **CSV 永続化:** データの保存にローカル CSV ファイルを使用し、Polars を用いて効率的に管理します。

## 2. コミュニケーション・ガイドライン
**重要:** ユーザーとのすべてのやり取り（説明、コードコメント、コミットメッセージ、ドキュメントなど）は、**必ず日本語で行ってください**。

## 3. アーキテクチャと設計
このプロジェクトは、**クリーンアーキテクチャ**（オニオンアーキテクチャ）に厳格に従っています。

### 依存関係のルール
依存関係は常に**内側**に向かう必要があります。
*   `presentation` → `application` → `domain`
*   `infrastructure` → `domain`
*   `domain` は**何にも依存しません**。

### レイヤーの責任
*   **`domain/`**: コアとなるビジネスロジックを含みます。
    *   **Entities:** `Transaction` (厳格なバリデーションルールを持つ Pydantic モデル)。
    *   **Repositories:** データアクセスのためのインターフェース (ABC)。
    *   **Services:** `LedgerService`（残高計算など）のようなドメインサービス。
*   **`application/`**: ユースケース（アプリケーションビジネスルール）を含みます。
    *   `presentation` と `domain` の間のデータフローを調整します。
    *   例: `AddTransactionUseCase`, `ListJournalUseCase`。
*   **`infrastructure/`**: フレームワークとドライバ。
    *   **Repository 実装:** Polars を使用した `CsvTransactionRepository`。
    *   **設定:** `settings.py`。
*   **`presentation/`**: インターフェースアダプター。
    *   **CLI:** `commands.py` 内で `Typer` を使用して実装。
    *   **Formatters:** ターミナル出力用の整形。
*   **`common/`**: 横断的関心事。
    *   **DI:** 依存性注入コンテナ (`di.py`) のファクトリ。

## 4. 技術スタック
*   **言語:** Python 3.13+
*   **パッケージマネージャ:** `uv` (高速な Python パッケージインストーラーおよびリゾルバー)
*   **CLI フレームワーク:** `Typer`
*   **データ処理:** `Polars` (効率的な CSV 入出力のための Rust 製 DataFrame ライブラリ)
*   **バリデーション:** `Pydantic`

## 5. 操作ワークフロー

### アプリケーションの実行
`uv` によって管理される仮想環境内でアプリケーションを実行するには、`uv run` を使用します。

```bash
# 仕訳を追加（対話形式）
uv run main.py add

# 仕訳帳を表示
uv run main.py journal

# 特定の勘定科目の元帳を表示
uv run main.py ledger <勘定科目名>
# 例: uv run main.py ledger 普通預金
```

### 依存関係の管理
`pyproject.toml` を手動で編集しないでください。`uv` を使用します。

```bash
# 新しいパッケージを追加
uv add <package_name>
```

## 6. 開発規約

### コードスタイル
*   PEP 8 に準拠してください。
*   すべての場所で型ヒント（Type Hints）を使用してください。
*   **コメント:** 価値の高いコメントを最小限に、**日本語**で記述してください。

### ドメインロジック
*   **バリデーション:** `Transaction` エンティティのバリデーションをバイパスしないでください。これにより `debit_amount == credit_amount` および `amount > 0` が保証されます。
*   **不変性:** ドメインエンティティは可能な限り不変（immutable）として扱ってください。

### 依存性注入 (DI)
*   プレゼンテーション層でリポジトリを直接インスタンス化しないでください。
*   常に `src/bookkeeper/common/di/di.py` のファクトリ関数（例: `init_add_transaction_usecase()`）を使用してください。

### 永続化 (Polars)
*   **ストレージ:** `data/transactions.csv` (git では無視されます)。
*   **スキーマ:** `CsvTransactionRepository` 内で定義されています。
*   **金額の扱い:** 浮動小数点誤差を防ぐため、CSV 内では Decimal 金額を**文字列**として保存し、アプリケーション内で `Decimal` オブジェクトに変換します。

## 7. 主要ファイル
*   `main.py`: アプリケーションのエントリーポイント。
*   `src/bookkeeper/presentation/cli/commands.py`: CLI コマンドの定義。
*   `src/bookkeeper/domain/entity/transaction.py`: バリデーションを含むコア・ドメインモデル。
*   `src/bookkeeper/infrastructure/repository/csv_transaction_repository.py`: CSV ストレージの実装。
*   `src/bookkeeper/common/di/di.py`: 依存性注入の配線。