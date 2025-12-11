"""
設定ファイル

データファイルのパスなどを管理
"""

from pathlib import Path


class Settings:
    """アプリケーション設定"""

    # プロジェクトルート
    PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent

    # データディレクトリ
    DATA_DIR = PROJECT_ROOT / "data"

    # 仕訳帳CSVファイル
    TRANSACTIONS_CSV = DATA_DIR / "transactions.csv"

    @classmethod
    def ensure_data_dir(cls):
        """データディレクトリが存在しない場合は作成"""
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)


# シングルトンインスタンス
settings = Settings()
