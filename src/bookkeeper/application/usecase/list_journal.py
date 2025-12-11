"""
ListJournal ユースケース

仕訳帳（全仕訳）を取得する
"""

from typing import List

from bookkeeper.domain.entity.transaction import Transaction
from bookkeeper.domain.repository.transaction_repository import TransactionRepository


class ListJournalUseCase:
    """仕訳帳取得ユースケース"""

    def __init__(self, repository: TransactionRepository):
        self.repository = repository

    def execute(self) -> List[Transaction]:
        """
        全ての仕訳を取得する

        Returns:
            仕訳のリスト
        """
        return self.repository.find_all()
