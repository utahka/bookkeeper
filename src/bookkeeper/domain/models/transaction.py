"""
Transaction エンティティ

仕訳の不変条件を保証するドメインモデル
"""
from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True)
class Transaction:
    """仕訳エンティティ"""
    
    date: date
    debit_account: str
    debit_amount: Decimal
    credit_account: str
    credit_amount: Decimal
    description: str
    note: str = ""
    evidence_path: str = ""
    
    def __post_init__(self):
        """不変条件のバリデーション"""
        # 借方金額と貸方金額は一致しなければならない
        if self.debit_amount != self.credit_amount:
            raise ValueError(
                f"借方金額 ({self.debit_amount}) と貸方金額 ({self.credit_amount}) が一致しません"
            )
        
        # 金額は正の数でなければならない
        if self.debit_amount <= 0:
            raise ValueError(f"金額は正の数でなければなりません: {self.debit_amount}")
        
        # 勘定科目は空文字列であってはならない
        if not self.debit_account.strip():
            raise ValueError("借方勘定科目が空です")
        if not self.credit_account.strip():
            raise ValueError("貸方勘定科目が空です")
        
        # 摘要は必須
        if not self.description.strip():
            raise ValueError("摘要が空です")
    
    @property
    def amount(self) -> Decimal:
        """取引金額（借方・貸方は同額なので、どちらかを返す）"""
        return self.debit_amount
