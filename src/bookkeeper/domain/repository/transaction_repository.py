"""
TransactionRepository インターフェース

仕訳の永続化を抽象化
"""

from abc import ABC, abstractmethod
from typing import List

from bookkeeper.domain.entity.transaction import Transaction


class TransactionRepository(ABC):
    """仕訳リポジトリのインターフェース"""

    @abstractmethod
    def add(self, transaction: Transaction) -> None:
        """仕訳を追加"""
        pass

    @abstractmethod
    def find_all(self) -> List[Transaction]:
        """全ての仕訳を取得"""
        pass

    @abstractmethod
    def find_by_account(self, account_name: str) -> List[Transaction]:
        """指定した勘定科目を含む仕訳を取得"""
        pass
