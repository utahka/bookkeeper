"""
CSV TransactionRepository 実装

Polarsを使って効率的にCSVで仕訳を永続化
"""

from pathlib import Path
from typing import List
from decimal import Decimal
from uuid import UUID, uuid4

import polars as pl

from bookkeeper.domain.entity.transaction import Transaction
from bookkeeper.domain.repository.transaction_repository import TransactionRepository


class CsvTransactionRepository(TransactionRepository):
    """CSV形式の仕訳リポジトリ（Polarsベース）"""

    # スキーマ定義
    SCHEMA = {
        "id": pl.String,  # UUID を文字列として保存
        "date": pl.Date,
        "debit_account": pl.String,
        "debit_amount": pl.String,  # Decimalとして扱うため文字列で保存
        "credit_account": pl.String,
        "credit_amount": pl.String,  # Decimalとして扱うため文字列で保存
        "description": pl.String,
        "note": pl.String,
        "evidence_path": pl.String,
    }

    def __init__(self, csv_path: Path):
        self.csv_path = csv_path
        self._ensure_csv_exists()

    def _ensure_csv_exists(self):
        """CSVファイルが存在しない場合はヘッダー付きで作成"""
        if not self.csv_path.exists():
            self.csv_path.parent.mkdir(parents=True, exist_ok=True)
            # 空のDataFrameを作成してヘッダーを書き込む
            df = pl.DataFrame(schema=self.SCHEMA)
            df.write_csv(self.csv_path)

    def add(self, transaction: Transaction) -> None:
        """仕訳を追加"""
        # UUID を生成（transaction.id が None の場合）
        transaction_id = transaction.id if transaction.id else uuid4()

        # 新しい行をDataFrameとして作成
        new_row = pl.DataFrame(
            {
                "id": [str(transaction_id)],
                "date": [transaction.date],
                "debit_account": [transaction.debit_account],
                "debit_amount": [str(transaction.debit_amount)],
                "credit_account": [transaction.credit_account],
                "credit_amount": [str(transaction.credit_amount)],
                "description": [transaction.description],
                "note": [transaction.note],
                "evidence_path": [transaction.evidence_path],
            }
        )

        # 既存のデータを読み込んで追加
        if self.csv_path.stat().st_size > 0:
            try:
                df = pl.read_csv(self.csv_path, schema_overrides=self.SCHEMA)
                df = pl.concat([df, new_row])
            except pl.exceptions.NoDataError:
                # ヘッダーのみの場合
                df = new_row
        else:
            df = new_row

        # 書き込み
        df.write_csv(self.csv_path)

    def find_all(self) -> List[Transaction]:
        """全ての仕訳を取得"""
        if not self.csv_path.exists() or self.csv_path.stat().st_size == 0:
            return []

        try:
            df = pl.read_csv(self.csv_path, schema_overrides=self.SCHEMA)
            return self._df_to_transactions(df)
        except pl.exceptions.NoDataError:
            # ヘッダーのみの場合
            return []

    def find_by_account(self, account_name: str) -> List[Transaction]:
        """指定した勘定科目を含む仕訳を取得"""
        if not self.csv_path.exists() or self.csv_path.stat().st_size == 0:
            return []

        try:
            df = pl.read_csv(self.csv_path, schema_overrides=self.SCHEMA)
            # Polarsの効率的なフィルタリング
            filtered = df.filter(
                (pl.col("debit_account") == account_name)
                | (pl.col("credit_account") == account_name)
            )
            return self._df_to_transactions(filtered)
        except pl.exceptions.NoDataError:
            return []

    def _df_to_transactions(self, df: pl.DataFrame) -> List[Transaction]:
        """DataFrameをTransactionのリストに変換"""
        transactions = []
        for row in df.iter_rows(named=True):
            transactions.append(
                Transaction(
                    id=UUID(row["id"]) if row.get("id") else None,
                    date=row["date"],
                    debit_account=row["debit_account"],
                    debit_amount=Decimal(row["debit_amount"]),
                    credit_account=row["credit_account"],
                    credit_amount=Decimal(row["credit_amount"]),
                    description=row["description"],
                    note=row.get("note", "") or "",
                    evidence_path=row.get("evidence_path", "") or "",
                )
            )
        return transactions
