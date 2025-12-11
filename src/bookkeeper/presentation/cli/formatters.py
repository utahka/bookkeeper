"""
CLI フォーマッター

出力を整形する
"""

from typing import List
from decimal import Decimal

from bookkeeper.domain.models.transaction import Transaction
from bookkeeper.domain.services.ledger_service import LedgerEntry


def format_journal(transactions: List[Transaction]) -> str:
    """
    仕訳帳を表形式でフォーマット

    Args:
        transactions: 仕訳のリスト

    Returns:
        フォーマットされた文字列
    """
    if not transactions:
        return "仕訳がありません。"

    lines = []
    lines.append("=" * 120)
    lines.append(
        f"{'日付':<12} {'借方科目':<15} {'借方金額':>12} {'貸方科目':<15} {'貸方金額':>12} {'摘要':<20}"
    )
    lines.append("=" * 120)

    for txn in transactions:
        lines.append(
            f"{txn.date.isoformat():<12} "
            f"{txn.debit_account:<15} "
            f"{_format_amount(txn.debit_amount):>12} "
            f"{txn.credit_account:<15} "
            f"{_format_amount(txn.credit_amount):>12} "
            f"{txn.description:<20}"
        )

    lines.append("=" * 120)
    lines.append(f"合計: {len(transactions)} 件")

    return "\n".join(lines)


def format_ledger(account_name: str, entries: List[LedgerEntry]) -> str:
    """
    元帳を表形式でフォーマット

    Args:
        account_name: 勘定科目名
        entries: 元帳エントリのリスト

    Returns:
        フォーマットされた文字列
    """
    if not entries:
        return f"「{account_name}」の取引がありません。"

    lines = []
    lines.append("=" * 100)
    lines.append(f"【{account_name} 元帳】")
    lines.append("=" * 100)
    lines.append(f"{'日付':<12} {'摘要':<30} {'借方':>12} {'貸方':>12} {'残高':>12}")
    lines.append("=" * 100)

    for entry in entries:
        debit_str = _format_amount(entry.debit_amount) if entry.debit_amount else ""
        credit_str = _format_amount(entry.credit_amount) if entry.credit_amount else ""

        lines.append(
            f"{entry.date:<12} "
            f"{entry.description:<30} "
            f"{debit_str:>12} "
            f"{credit_str:>12} "
            f"{_format_amount(entry.balance):>12}"
        )

    lines.append("=" * 100)
    lines.append(f"期末残高: {_format_amount(entries[-1].balance)}")

    return "\n".join(lines)


def _format_amount(amount: Decimal | None) -> str:
    """金額をフォーマット（3桁区切り）"""
    if amount is None:
        return ""
    return f"{amount:,}"
