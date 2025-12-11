"""
LedgerService ドメインサービス

仕訳帳から各種元帳を生成するビジネスロジック
"""

from typing import List
from dataclasses import dataclass
from decimal import Decimal

from bookkeeper.domain.models.transaction import Transaction


@dataclass
class LedgerEntry:
    """元帳の1行を表すデータ"""

    date: str
    description: str
    debit_amount: Decimal | None  # 借方に現れた場合
    credit_amount: Decimal | None  # 貸方に現れた場合
    balance: Decimal  # 残高


class LedgerService:
    """元帳生成サービス"""

    @staticmethod
    def generate_ledger(
        transactions: List[Transaction], account_name: str
    ) -> List[LedgerEntry]:
        """
        指定した勘定科目の元帳を生成

        Args:
            transactions: 全仕訳のリスト
            account_name: 対象の勘定科目名

        Returns:
            元帳エントリのリスト
        """
        ledger_entries = []
        balance = Decimal("0")

        for txn in transactions:
            debit_amt = None
            credit_amt = None

            # 借方に現れた場合
            if txn.debit_account == account_name:
                debit_amt = txn.debit_amount
                balance += txn.debit_amount

            # 貸方に現れた場合
            if txn.credit_account == account_name:
                credit_amt = txn.credit_amount
                balance -= txn.credit_amount

            # どちらかに現れた場合のみ記録
            if debit_amt is not None or credit_amt is not None:
                ledger_entries.append(
                    LedgerEntry(
                        date=txn.date.isoformat(),
                        description=txn.description,
                        debit_amount=debit_amt,
                        credit_amount=credit_amt,
                        balance=balance,
                    )
                )

        return ledger_entries
