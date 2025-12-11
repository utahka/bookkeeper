"""
AddTransaction ユースケース

仕訳を追加する
"""

from bookkeeper.domain.entity.transaction import Transaction
from bookkeeper.domain.repository.transaction_repository import TransactionRepository


class AddTransactionUseCase:
    """仕訳追加ユースケース"""

    def __init__(self, repository: TransactionRepository):
        self.repository = repository

    def execute(self, transaction: Transaction) -> None:
        """
        仕訳を追加する

        Args:
            transaction: 追加する仕訳エンティティ
        """
        # エンティティ自体がバリデーションを持っているので、
        # ここでは単純にリポジトリに保存するだけ
        self.repository.add(transaction)
