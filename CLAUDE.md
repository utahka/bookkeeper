# CLAUDE.md

このファイルは、Claude Code (claude.ai/code) がこのリポジトリで作業する際のガイダンスを提供します。

## 重要: コミュニケーション言語

**このリポジトリで作業する際は、必ず日本語で回答してください。**

コード内のコメント、ドキュメント、ユーザーとのやり取り、すべて日本語で行ってください。

## プロジェクト概要

青色申告のための複式簿記に対応した日本語会計CLIツールです。仕訳帳と元帳の機能を提供します。

## アプリケーションの実行方法

```bash
# 仕訳を追加（対話形式）
uv run main.py add

# 仕訳帳を表示
uv run main.py journal

# 特定の勘定科目の元帳を表示
uv run main.py ledger 普通預金
uv run main.py ledger 売掛金
```

## アーキテクチャ

このコードベースは**クリーンアーキテクチャ**（オニオンアーキテクチャ、ヘキサゴナルアーキテクチャとも呼ばれる）に従い、厳密な階層化を実現しています。

### レイヤー構造

```
presentation/    → ユーザーインターフェース（CLIコマンド、フォーマッタ）
application/     → ユースケース（オーケストレーション層）
domain/          → ビジネスロジック（エンティティ、リポジトリ、サービス）
infrastructure/  → 外部関心事（永続化、設定）
```

### アーキテクチャの重要な原則

1. **依存関係の方向**: 依存関係は内側のみに向かう
   - `presentation` は `application` と `domain` に依存
   - `application` は `domain` に依存
   - `domain` は何にも依存しない（純粋なビジネスロジック）
   - `infrastructure` は `domain` に依存（インターフェースを実装）

2. **ドメイン層は純粋**:
   - `domain/models/transaction.py`: 不変条件バリデーションを持つイミュータブルエンティティ（借方=貸方、金額 > 0 など）
   - `domain/repositories/`: 抽象インターフェースのみ（ABCクラス）
   - `domain/services/ledger_service.py`: 仕訳帳から元帳を生成するビジネスロジック

3. **アプリケーション層はオーケストレーション**:
   - `application/use_cases/` 内のユースケースがドメインとインフラストラクチャを調整
   - 各ユースケースは単一のビジネス操作（AddTransaction, ListJournal, ViewLedger）

4. **インフラストラクチャ層は実装**:
   - `infrastructure/persistence/csv_transaction_repository.py`: TransactionRepository の具体実装
   - `infrastructure/config/settings.py`: 設定管理

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

## 新機能の追加

### 新しい勘定科目タイプの追加

1. `src/bookkeeper/domain/models/account.py` の `ACCOUNT_TYPE_MAP` を更新
2. 他の変更は不要 - システムはデータ駆動型

### 新しいユースケースの追加

1. `application/use_cases/` に新しいユースケースクラスを作成
2. `__init__` で必要なリポジトリを注入
3. `execute()` メソッドを実装
4. `presentation/cli/commands.py` で接続

### 永続化層の変更

1. `infrastructure/persistence/` に新しいリポジトリ実装を作成
2. `TransactionRepository` インターフェースを実装
3. `presentation/cli/commands.py` の `CLI.__init__()` でリポジトリの初期化を更新

## 重要な注意事項

- UI内のすべての日本語テキストは意図的なもの（これは日本語会計ツールです）
- `Transaction` エンティティは重要なビジネスルールを強制 - バリデーションをバイパスしないこと
- ドメインロジックを変更する際は、不変条件が保護されていることを確認すること
- リポジトリパターンにより永続化メカニズムの簡単な切り替えが可能（現在はCSV、SQLite/PostgreSQLにも変更可能）
