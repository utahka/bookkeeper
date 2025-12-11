"""
会計ツール エントリーポイント
"""

import sys
from bookkeeper.presentation.cli.commands import CLI


def main():
    """メイン関数"""
    cli = CLI()
    cli.run(sys.argv)


if __name__ == "__main__":
    main()
