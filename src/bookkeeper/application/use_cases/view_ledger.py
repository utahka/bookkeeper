"""
ViewLedger ユースケース

指定した勘定科目の元帳を取得する
"""

from typing import List

from bookkeeper.domain.repositories.transaction_repository import TransactionRepository
from bookkeeper.domain.services.ledger_service import LedgerService, LedgerEntry


class ViewLedgerUseCase:
    """元帳表示ユースケース"""

    def __init__(self, repository: TransactionRepository):
        self.repository = repository
        self.ledger_service = LedgerService()

    def execute(self, account_name: str) -> List[LedgerEntry]:
        """
        指定した勘定科目の元帳を取得

        Args:
            account_name: 勘定科目名

        Returns:
            元帳エントリのリスト
        """
        # 全仕訳を取得
        transactions = self.repository.find_all()

        # 元帳を生成
        return self.ledger_service.generate_ledger(transactions, account_name)
