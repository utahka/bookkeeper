"""
Transaction エンティティ

仕訳の不変条件を保証するドメインモデル
"""
from datetime import date
from decimal import Decimal
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class Transaction(BaseModel):
    """仕訳エンティティ"""

    model_config = ConfigDict(frozen=True)

    id: UUID | None = None  # リポジトリが UUID を生成（新規作成時は None）
    date: date
    debit_account: Annotated[str, Field(min_length=1)]
    debit_amount: Decimal
    credit_account: Annotated[str, Field(min_length=1)]
    credit_amount: Decimal
    description: Annotated[str, Field(min_length=1)]
    note: str = ""
    evidence_path: str = ""

    @field_validator('debit_account')
    @classmethod
    def validate_debit_account_not_empty(cls, v: str) -> str:
        """借方勘定科目は空文字列であってはならない"""
        if not v.strip():
            raise ValueError("借方勘定科目が空です")
        return v

    @field_validator('credit_account')
    @classmethod
    def validate_credit_account_not_empty(cls, v: str) -> str:
        """貸方勘定科目は空文字列であってはならない"""
        if not v.strip():
            raise ValueError("貸方勘定科目が空です")
        return v

    @field_validator('description')
    @classmethod
    def validate_description_not_empty(cls, v: str) -> str:
        """摘要は必須"""
        if not v.strip():
            raise ValueError("摘要が空です")
        return v

    @field_validator('debit_amount', 'credit_amount')
    @classmethod
    def validate_amount_positive(cls, v: Decimal) -> Decimal:
        """金額は正の数でなければならない"""
        if v <= 0:
            raise ValueError(f"金額は正の数でなければなりません: {v}")
        return v

    @model_validator(mode='after')
    def validate_amounts_match(self) -> 'Transaction':
        """借方金額と貸方金額は一致しなければならない"""
        if self.debit_amount != self.credit_amount:
            raise ValueError(
                f"借方金額 ({self.debit_amount}) と貸方金額 ({self.credit_amount}) が一致しません"
            )
        return self

    @property
    def amount(self) -> Decimal:
        """取引金額（借方・貸方は同額なので、どちらかを返す）"""
        return self.debit_amount
