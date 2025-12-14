"""
ErrorHandlerモジュール

例外処理、ログ記録、エラーメッセージ生成を担当

Requirements: 1.3, 6.3, 7.3, 7.4
"""

import logging
import sys
from typing import Optional
from pathlib import Path


class ErrorHandler:
    """
    エラーハンドリングとログ記録を提供するクラス

    Attributes:
        log_file (str): ログファイルのパス
        logger (logging.Logger): Pythonロガーインスタンス
    """

    def __init__(self, log_file: str = "visualizer.log"):
        """
        ErrorHandlerの初期化

        Args:
            log_file: ログファイルパス（デフォルト: visualizer.log）
        """
        self.log_file = log_file
        self.logger = self._setup_logger()

    def __del__(self):
        """デストラクタ：ログハンドラをクリーンアップ"""
        self.close()

    def close(self):
        """ログハンドラを明示的にクローズ"""
        for handler in self.logger.handlers[:]:
            handler.close()
            self.logger.removeHandler(handler)

    def _setup_logger(self) -> logging.Logger:
        """
        ロガーの設定

        Returns:
            設定されたロガーインスタンス
        """
        logger = logging.getLogger('numpy_visualizer')
        logger.setLevel(logging.DEBUG)

        # 既存のハンドラをクリア（重複回避）
        logger.handlers.clear()

        # ファイルハンドラの設定
        file_handler = logging.FileHandler(
            self.log_file,
            mode='a',
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)

        # フォーマッターの設定
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        return logger

    def handle_file_error(self, error: Exception, file_path: str) -> str:
        """
        ファイル関連エラーを処理

        Args:
            error: 発生した例外
            file_path: エラーが発生したファイルパス

        Returns:
            ユーザー向けエラーメッセージ

        Requirements: 1.3
        """
        # エラーをログに記録
        self.log_exception(error, context=f"ファイル処理: {file_path}")

        # ユーザー向けエラーメッセージを生成
        if isinstance(error, FileNotFoundError):
            message = f"エラー: ファイルが見つかりません: {file_path}\n"
            message += "ファイルパスを確認してください。"
            return message

        elif isinstance(error, ValueError):
            message = f"エラー: 無効なファイル形式: {file_path}\n"
            message += ".npyまたは.npzファイルを指定してください。"
            return message

        elif isinstance(error, PermissionError):
            message = f"エラー: ファイルへのアクセス権限がありません: {file_path}\n"
            message += "ファイルの権限を確認してください。"
            return message

        else:
            message = f"エラー: ファイル読み込み中に問題が発生しました: {file_path}\n"
            message += f"詳細: {str(error)}"
            return message

    def handle_system_error(self, error: Exception) -> None:
        """
        システムエラー（メモリ不足等）を処理し安全に終了

        Args:
            error: 発生したシステムエラー

        Requirements: 7.3
        """
        # エラーをログに記録
        self.log_exception(error, context="システムエラー")

        # ユーザーにエラーメッセージを表示
        if isinstance(error, MemoryError):
            print("致命的エラー: メモリが不足しています。", file=sys.stderr)
            print("データサイズを小さくするか、システムメモリを増やしてください。", file=sys.stderr)
        else:
            print(f"致命的エラー: システムエラーが発生しました: {str(error)}", file=sys.stderr)

        # ログファイルへの記録を確実に完了
        logging.shutdown()

        # 安全に終了
        sys.exit(1)

    def log_exception(self, error: Exception, context: Optional[str] = None) -> None:
        """
        例外をログファイルに記録

        Args:
            error: 記録する例外
            context: エラーのコンテキスト情報（オプション）

        Requirements: 7.4
        """
        if context:
            self.logger.error(
                f"[{context}] {type(error).__name__}: {str(error)}",
                exc_info=True
            )
        else:
            self.logger.error(
                f"{type(error).__name__}: {str(error)}",
                exc_info=True
            )

    def handle_invalid_args(self, error: Exception, help_text: str) -> str:
        """
        無効な引数エラーを処理

        Args:
            error: 発生した例外
            help_text: ヘルプテキスト

        Returns:
            ユーザー向けエラーメッセージ

        Requirements: 6.3
        """
        # エラーをログに記録
        self.log_exception(error, context="CLI引数解析")

        # ユーザー向けエラーメッセージを生成
        message = f"エラー: 無効な引数が指定されました\n"
        message += f"詳細: {str(error)}\n\n"
        message += help_text

        return message
