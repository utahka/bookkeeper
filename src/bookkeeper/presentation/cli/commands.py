"""
CLI コマンド

ユーザーインターフェース
"""

import sys
from datetime import date, datetime
from decimal import Decimal, InvalidOperation

from bookkeeper.domain.models.transaction import Transaction
from bookkeeper.application.use_cases.add_transaction import AddTransactionUseCase
from bookkeeper.application.use_cases.list_journal import ListJournalUseCase
from bookkeeper.application.use_cases.view_ledger import ViewLedgerUseCase
from bookkeeper.infrastructure.persistence.csv_transaction_repository import (
    CsvTransactionRepository,
)
from bookkeeper.infrastructure.config.settings import settings
from bookkeeper.presentation.cli.formatters import format_journal, format_ledger


class CLI:
    """CLIアプリケーション"""

    def __init__(self):
        # リポジトリの初期化
        settings.ensure_data_dir()
        self.repository = CsvTransactionRepository(settings.TRANSACTIONS_CSV)

        # ユースケースの初期化
        self.add_transaction_use_case = AddTransactionUseCase(self.repository)
        self.list_journal_use_case = ListJournalUseCase(self.repository)
        self.view_ledger_use_case = ViewLedgerUseCase(self.repository)

    def run(self, args: list[str]):
        """CLIを実行"""
        if len(args) < 2:
            self._print_usage()
            return

        command = args[1]

        if command == "add":
            self._add_command()
        elif command == "journal":
            self._journal_command()
        elif command == "ledger":
            if len(args) < 3:
                print("エラー: 勘定科目名を指定してください")
                print("使用例: uv run main.py ledger 普通預金")
                return
            account_name = args[2]
            self._ledger_command(account_name)
        else:
            print(f"エラー: 不明なコマンド '{command}'")
            self._print_usage()

    def _print_usage(self):
        """使い方を表示"""
        print("青色申告 会計ツール")
        print()
        print("使い方:")
        print("  uv run main.py add              仕訳を追加")
        print("  uv run main.py journal          仕訳帳を表示")
        print("  uv run main.py ledger <科目>    元帳を表示")
        print()
        print("例:")
        print("  uv run main.py ledger 普通預金")
        print("  uv run main.py ledger 売掛金")

    def _add_command(self):
        """仕訳追加コマンド"""
        print("=== 仕訳追加 ===")
        print()

        try:
            # 日付入力
            date_str = input("日付 (YYYY-MM-DD, 空欄で今日): ").strip()
            if not date_str:
                txn_date = date.today()
            else:
                txn_date = datetime.strptime(date_str, "%Y-%m-%d").date()

            # 借方
            debit_account = input("借方勘定科目: ").strip()
            debit_amount_str = input("借方金額: ").strip()
            debit_amount = Decimal(debit_amount_str)

            # 貸方
            credit_account = input("貸方勘定科目: ").strip()
            credit_amount_str = input("貸方金額 (空欄で借方と同額): ").strip()
            if not credit_amount_str:
                credit_amount = debit_amount
            else:
                credit_amount = Decimal(credit_amount_str)

            # 摘要
            description = input("摘要: ").strip()

            # 備考（任意）
            note = input("備考 (任意): ").strip()

            # 証憑パス（任意）
            evidence_path = input("証憑パス (任意): ").strip()

            # Transactionエンティティを作成（バリデーションが実行される）
            transaction = Transaction(
                date=txn_date,
                debit_account=debit_account,
                debit_amount=debit_amount,
                credit_account=credit_account,
                credit_amount=credit_amount,
                description=description,
                note=note,
                evidence_path=evidence_path,
            )

            # 保存
            self.add_transaction_use_case.execute(transaction)

            print()
            print("✓ 仕訳を追加しました")

        except (ValueError, InvalidOperation) as e:
            print(f"エラー: {e}")
            sys.exit(1)
        except KeyboardInterrupt:
            print("\n中断しました")
            sys.exit(0)

    def _journal_command(self):
        """仕訳帳表示コマンド"""
        transactions = self.list_journal_use_case.execute()
        print(format_journal(transactions))

    def _ledger_command(self, account_name: str):
        """元帳表示コマンド"""
        entries = self.view_ledger_use_case.execute(account_name)
        print(format_ledger(account_name, entries))
