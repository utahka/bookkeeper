"""
依存性注入（DI）モジュール

各ユースケースの初期化を行うファクトリ関数を提供
"""

from bookkeeper.application.use_cases.add_transaction import AddTransactionUseCase
from bookkeeper.application.use_cases.list_journal import ListJournalUseCase
from bookkeeper.application.use_cases.view_ledger import ViewLedgerUseCase
from bookkeeper.domain.repositories.transaction_repository import TransactionRepository
from bookkeeper.infrastructure.config.settings import settings
from bookkeeper.infrastructure.persistence.csv_transaction_repository import (
    CsvTransactionRepository,
)


def _get_transaction_repository() -> TransactionRepository:
    """TransactionRepositoryの実装を取得"""
    settings.ensure_data_dir()
    return CsvTransactionRepository(settings.TRANSACTIONS_CSV)


def init_add_transaction_usecase() -> AddTransactionUseCase:
    """AddTransactionUseCaseを初期化"""
    repository = _get_transaction_repository()
    return AddTransactionUseCase(repository)


def init_list_journal_usecase() -> ListJournalUseCase:
    """ListJournalUseCaseを初期化"""
    repository = _get_transaction_repository()
    return ListJournalUseCase(repository)


def init_view_ledger_usecase() -> ViewLedgerUseCase:
    """ViewLedgerUseCaseを初期化"""
    repository = _get_transaction_repository()
    return ViewLedgerUseCase(repository)
