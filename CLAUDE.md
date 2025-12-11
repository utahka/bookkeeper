# CLAUDE.md

このファイルは、Claude Code (claude.ai/code) がこのリポジトリで作業する際のガイダンスを提供します。

## 重要: コミュニケーション言語

**このリポジトリで作業する際は、必ず日本語で回答してください。**

コード内のコメント、ドキュメント、ユーザーとのやり取り、すべて日本語で行ってください。

## プロジェクト概要

青色申告のための複式簿記に対応した日本語会計CLIツールです。仕訳帳と元帳の機能を提供します。

## 技術スタック

- **言語**: Python 3.13+
- **パッケージマネージャ**: uv
- **CLIフレームワーク**: typer
- **アーキテクチャ**: クリーンアーキテクチャ

## アプリケーションの実行方法

```bash
# 依存関係の追加
uv add <パッケージ名>

# 仕訳を追加（対話形式）
uv run main.py add

# 仕訳帳を表示
uv run main.py journal

# 特定の勘定科目の元帳を表示
uv run main.py ledger 普通預金
uv run main.py ledger 売掛金

# ヘルプの表示
uv run main.py --help
uv run main.py <コマンド> --help
```

## アーキテクチャ

このコードベースは**クリーンアーキテクチャ**（オニオンアーキテクチャ、ヘキサゴナルアーキテクチャとも呼ばれる）に従い、厳密な階層化を実現しています。

### レイヤー構造

```
common/          → 共通機能（DI、設定など）
presentation/    → ユーザーインターフェース（CLIコマンド、フォーマッタ）
application/     → ユースケース（オーケストレーション層）
domain/          → ビジネスロジック（エンティティ、リポジトリ、サービス）
infrastructure/  → 外部関心事（永続化、設定）
```

### アーキテクチャの重要な原則

1. **依存関係の方向**: 依存関係は内側のみに向かう
   - `presentation` は `application` と `domain` に依存（`infrastructure`には依存しない）
   - `application` は `domain` に依存
   - `domain` は何にも依存しない（純粋なビジネスロジック）
   - `infrastructure` は `domain` に依存（インターフェースを実装）
   - `common/di` が依存関係を解決（DIパターン）

2. **依存性注入（DI）パターン**:
   - `common/di/di.py` で各ユースケースの初期化を行う
   - ファクトリ関数でリポジトリとサービスを注入
   - プレゼンテーション層はDIモジュールのみに依存
   - 例: `init_add_transaction_usecase()` がリポジトリを注入してユースケースを返す

3. **ドメイン層は純粋**:
   - `domain/models/transaction.py`: 不変条件バリデーションを持つイミュータブルエンティティ（借方=貸方、金額 > 0 など）
   - `domain/repositories/`: 抽象インターフェースのみ（ABCクラス）
   - `domain/services/ledger_service.py`: 仕訳帳から元帳を生成するビジネスロジック

4. **アプリケーション層はオーケストレーション**:
   - `application/use_cases/` 内のユースケースがドメインとインフラストラクチャを調整
   - 各ユースケースは単一のビジネス操作（AddTransaction, ListJournal, ViewLedger）

5. **インフラストラクチャ層は実装**:
   - `infrastructure/persistence/csv_transaction_repository.py`: TransactionRepository の具体実装
   - `infrastructure/config/settings.py`: 設定管理

6. **プレゼンテーション層はtyperを使用**:
   - `presentation/cli/commands.py` でtyperを使ってCLIを定義
   - `@app.command()` デコレータで各コマンドを宣言的に定義
   - DIモジュールからユースケースを取得して実行

### 複式簿記の概念

- 各 `Transaction` には借方と貸方があり、必ず貸借が一致する
- ドメインモデルは `Transaction.__post_init__()` でこの不変条件を強制
- 元帳生成（`LedgerService`）は残高を計算:
  - 借方エントリは残高を増加
  - 貸方エントリは残高を減少
- 勘定科目の種類は `domain/models/account.py` で定義（資産、負債、資本、収益、費用）

## データ保存

- 仕訳は `data/transactions.csv` に保存される
- CSVファイルが存在しない場合、ヘッダー付きで自動作成される
- データディレクトリのパス: `PROJECT_ROOT/data/`
- **重要**: `data/transactions.csv` は `.gitignore` で除外されている（実際の取引データを保護するため）

## 新機能の追加

### 新しい勘定科目タイプの追加

1. `src/bookkeeper/domain/models/account.py` の `ACCOUNT_TYPE_MAP` を更新
2. 他の変更は不要 - システムはデータ駆動型

### 新しいユースケースの追加

1. `application/use_cases/` に新しいユースケースクラスを作成
2. `__init__` で必要なリポジトリを注入
3. `execute()` メソッドを実装
4. `common/di/di.py` に初期化ファクトリ関数を追加
5. `common/di/__init__.py` でエクスポート
6. `presentation/cli/commands.py` でDI経由でユースケースを取得して使用

### 新しいCLIコマンドの追加

1. `presentation/cli/commands.py` に `@app.command()` で新しい関数を追加
2. DIモジュールから適切なユースケースを取得
3. typerの型アノテーションで引数を定義（自動的にヘルプが生成される）

### 永続化層の変更

1. `infrastructure/persistence/` に新しいリポジトリ実装を作成
2. `domain/repositories/` のインターフェースを実装
3. `common/di/di.py` の `_get_transaction_repository()` を更新して新しい実装を返す

### 依存関係の追加

- `uv add <パッケージ名>` を使用（`pyproject.toml` を直接編集しない）
- uv が自動的に `pyproject.toml` と `uv.lock` を更新

## 重要な注意事項

- UI内のすべての日本語テキストは意図的なもの（これは日本語会計ツールです）
- `Transaction` エンティティは重要なビジネスルールを強制 - バリデーションをバイパスしないこと
- ドメインロジックを変更する際は、不変条件が保護されていることを確認すること
- リポジトリパターンにより永続化メカニズムの簡単な切り替えが可能（現在はCSV、SQLite/PostgreSQLにも変更可能）
- プレゼンテーション層は決してインフラストラクチャ層に直接依存しない - 必ずDIモジュール経由で依存関係を解決する

## 開発のベストプラクティス

### パッケージ管理
- 依存関係の追加は `uv add` を使用
- 直接 `pyproject.toml` を編集しない

### CLIの実装
- typerの宣言的なAPIを活用
- 型アノテーションを使って自動的にヘルプを生成
- `typer.Argument()` や `typer.Option()` で引数を明示的に定義

### 依存性の管理
- プレゼンテーション層は常にDIモジュール経由でユースケースを取得
- インフラストラクチャの実装詳細をDI層に隠蔽
- テスタビリティを高めるため、具体的な実装への依存を避ける
