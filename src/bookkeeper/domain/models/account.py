"""
Account 値オブジェクト

勘定科目の種類を表現
"""

from enum import Enum


class AccountType(Enum):
    """勘定科目の種類"""

    ASSET = "資産"  # 現金、普通預金、売掛金など
    LIABILITY = "負債"  # 買掛金、未払金など
    EQUITY = "資本"  # 事業主借、事業主貸など
    REVENUE = "収益"  # 売上など
    EXPENSE = "費用"  # 消耗品費、通信費、旅費交通費など


# 勘定科目名とその種類のマッピング（将来的にはDBや設定ファイルから読み込む）
ACCOUNT_TYPE_MAP = {
    # 資産
    "現金": AccountType.ASSET,
    "普通預金": AccountType.ASSET,
    "当座預金": AccountType.ASSET,
    "売掛金": AccountType.ASSET,
    # 負債
    "買掛金": AccountType.LIABILITY,
    "未払金": AccountType.LIABILITY,
    # 資本（事業主勘定）
    "事業主借": AccountType.EQUITY,  # プライベート資金を事業に入れた
    "事業主貸": AccountType.EQUITY,  # 事業資金をプライベートに使った
    # 収益
    "売上": AccountType.REVENUE,
    # 費用
    "消耗品費": AccountType.EXPENSE,
    "通信費": AccountType.EXPENSE,
    "旅費交通費": AccountType.EXPENSE,
    "新聞図書費": AccountType.EXPENSE,
    "地代家賃": AccountType.EXPENSE,
    "外注工賃": AccountType.EXPENSE,
}


def get_account_type(account_name: str) -> AccountType | None:
    """勘定科目名から種類を取得"""
    return ACCOUNT_TYPE_MAP.get(account_name)
