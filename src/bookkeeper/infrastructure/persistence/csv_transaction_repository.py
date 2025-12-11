"""
CSV TransactionRepository 実装

CSVファイルで仕訳を永続化
"""

import csv
from pathlib import Path
from typing import List
from datetime import date
from decimal import Decimal

from bookkeeper.domain.models.transaction import Transaction
from bookkeeper.domain.repositories.transaction_repository import TransactionRepository


class CsvTransactionRepository(TransactionRepository):
    """CSV形式の仕訳リポジトリ"""

    CSV_HEADERS = [
        "date",
        "debit_account",
        "debit_amount",
        "credit_account",
        "credit_amount",
        "description",
        "note",
        "evidence_path",
    ]

    def __init__(self, csv_path: Path):
        self.csv_path = csv_path
        self._ensure_csv_exists()

    def _ensure_csv_exists(self):
        """CSVファイルが存在しない場合はヘッダー付きで作成"""
        if not self.csv_path.exists():
            self.csv_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=self.CSV_HEADERS)
                writer.writeheader()

    def add(self, transaction: Transaction) -> None:
        """仕訳を追加"""
        with open(self.csv_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.CSV_HEADERS)
            writer.writerow(
                {
                    "date": transaction.date.isoformat(),
                    "debit_account": transaction.debit_account,
                    "debit_amount": str(transaction.debit_amount),
                    "credit_account": transaction.credit_account,
                    "credit_amount": str(transaction.credit_amount),
                    "description": transaction.description,
                    "note": transaction.note,
                    "evidence_path": transaction.evidence_path,
                }
            )

    def find_all(self) -> List[Transaction]:
        """全ての仕訳を取得"""
        transactions = []

        if not self.csv_path.exists():
            return transactions

        with open(self.csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                transactions.append(self._row_to_transaction(row))

        return transactions

    def find_by_account(self, account_name: str) -> List[Transaction]:
        """指定した勘定科目を含む仕訳を取得"""
        all_transactions = self.find_all()
        return [
            txn
            for txn in all_transactions
            if txn.debit_account == account_name or txn.credit_account == account_name
        ]

    def _row_to_transaction(self, row: dict) -> Transaction:
        """CSV行をTransactionエンティティに変換"""
        return Transaction(
            date=date.fromisoformat(row["date"]),
            debit_account=row["debit_account"],
            debit_amount=Decimal(row["debit_amount"]),
            credit_account=row["credit_account"],
            credit_amount=Decimal(row["credit_amount"]),
            description=row["description"],
            note=row.get("note", ""),
            evidence_path=row.get("evidence_path", ""),
        )
