"""
CLI コマンド

ユーザーインターフェース
"""

import sys
from datetime import date, datetime
from decimal import Decimal, InvalidOperation

import typer

from bookkeeper.common.di import (
    init_add_transaction_usecase,
    init_list_journal_usecase,
    init_view_ledger_usecase,
)
from bookkeeper.domain.models.transaction import Transaction
from bookkeeper.presentation.cli.formatters import format_journal, format_ledger


# Typerアプリケーションの作成
app = typer.Typer(
    name="bookkeeper",
    help="青色申告 会計ツール",
    no_args_is_help=True,
)


@app.command()
def add():
    """仕訳を追加"""
    print("=== 仕訳追加 ===")
    print()

    use_case = init_add_transaction_usecase()

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
        use_case.execute(transaction)

        print()
        print("✓ 仕訳を追加しました")

    except (ValueError, InvalidOperation) as e:
        print(f"エラー: {e}")
        raise typer.Exit(code=1)
    except KeyboardInterrupt:
        print("\n中断しました")
        raise typer.Exit(code=0)


@app.command()
def journal():
    """仕訳帳を表示"""
    use_case = init_list_journal_usecase()
    transactions = use_case.execute()
    print(format_journal(transactions))


@app.command()
def ledger(account_name: str = typer.Argument(..., help="勘定科目名")):
    """元帳を表示"""
    use_case = init_view_ledger_usecase()
    entries = use_case.execute(account_name)
    print(format_ledger(account_name, entries))
