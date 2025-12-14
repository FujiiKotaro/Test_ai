"""
ErrorHandlerモジュールのユニットテスト

Requirements: 1.3, 6.3, 7.3, 7.4
"""

import unittest
import logging
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
import tempfile
import sys

# Import the module to test (will fail initially - RED phase)
sys.path.insert(0, str(Path(__file__).parent.parent))
from numpy_visualizer.error_handler import ErrorHandler


class TestErrorHandlerInitialization(unittest.TestCase):
    """ErrorHandlerの初期化テスト"""

    def setUp(self):
        """テストごとの初期化"""
        self.temp_dir = tempfile.mkdtemp()
        self.log_file = os.path.join(self.temp_dir, "test.log")

    def tearDown(self):
        """テスト後のクリーンアップ"""
        if hasattr(self, 'handler'):
            self.handler.close()
        if os.path.exists(self.log_file):
            os.remove(self.log_file)
        os.rmdir(self.temp_dir)

    def test_init_with_default_log_file(self):
        """デフォルトログファイル名での初期化"""
        handler = ErrorHandler()
        self.assertIsNotNone(handler)
        self.assertEqual(handler.log_file, "visualizer.log")

    def test_init_with_custom_log_file(self):
        """カスタムログファイル名での初期化"""
        handler = ErrorHandler(log_file=self.log_file)
        self.assertEqual(handler.log_file, self.log_file)

    def test_logger_is_configured(self):
        """ロガーが正しく設定されている"""
        handler = ErrorHandler(log_file=self.log_file)
        self.assertIsNotNone(handler.logger)
        self.assertIsInstance(handler.logger, logging.Logger)


class TestFileErrorHandling(unittest.TestCase):
    """ファイルエラーハンドリングのテスト (Requirement 1.3)"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.log_file = os.path.join(self.temp_dir, "test.log")
        self.handler = ErrorHandler(log_file=self.log_file)

    def tearDown(self):
        self.handler.close()
        if os.path.exists(self.log_file):
            os.remove(self.log_file)
        os.rmdir(self.temp_dir)

    def test_handle_file_not_found_error(self):
        """FileNotFoundErrorの処理"""
        error = FileNotFoundError("File does not exist")
        file_path = "/path/to/nonexistent.npy"

        message = self.handler.handle_file_error(error, file_path)

        self.assertIsInstance(message, str)
        self.assertIn("ファイルが見つかりません", message)
        self.assertIn(file_path, message)

    def test_handle_value_error(self):
        """ValueError（無効なファイル形式）の処理"""
        error = ValueError("Invalid file format")
        file_path = "/path/to/invalid.txt"

        message = self.handler.handle_file_error(error, file_path)

        self.assertIsInstance(message, str)
        self.assertIn("無効なファイル形式", message)

    def test_file_error_is_logged(self):
        """ファイルエラーがログに記録される"""
        error = FileNotFoundError("Test error")
        file_path = "/test/path.npy"

        self.handler.handle_file_error(error, file_path)

        # ログファイルが作成されている
        self.assertTrue(os.path.exists(self.log_file))

        # ログファイルにエラー情報が含まれている
        with open(self.log_file, 'r', encoding='utf-8') as f:
            log_content = f.read()
            self.assertIn("FileNotFoundError", log_content)
            self.assertIn(file_path, log_content)


class TestSystemErrorHandling(unittest.TestCase):
    """システムエラーハンドリングのテスト (Requirement 7.3)"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.log_file = os.path.join(self.temp_dir, "test.log")
        self.handler = ErrorHandler(log_file=self.log_file)

    def tearDown(self):
        self.handler.close()
        if os.path.exists(self.log_file):
            os.remove(self.log_file)
        os.rmdir(self.temp_dir)

    def test_handle_memory_error(self):
        """MemoryErrorの処理と安全終了"""
        error = MemoryError("Not enough memory")

        with patch('sys.exit') as mock_exit:
            self.handler.handle_system_error(error)
            mock_exit.assert_called_once_with(1)

    def test_system_error_is_logged(self):
        """システムエラーがログに記録される"""
        error = MemoryError("Test memory error")

        with patch('sys.exit'):
            self.handler.handle_system_error(error)

        # ログファイルにエラー情報が含まれている
        with open(self.log_file, 'r', encoding='utf-8') as f:
            log_content = f.read()
            self.assertIn("MemoryError", log_content)
            self.assertIn("システムエラー", log_content)


class TestExceptionLogging(unittest.TestCase):
    """例外ログ記録のテスト (Requirement 7.4)"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.log_file = os.path.join(self.temp_dir, "test.log")
        self.handler = ErrorHandler(log_file=self.log_file)

    def tearDown(self):
        self.handler.close()
        if os.path.exists(self.log_file):
            os.remove(self.log_file)
        os.rmdir(self.temp_dir)

    def test_log_exception_without_context(self):
        """コンテキストなしで例外をログ記録"""
        error = ValueError("Test exception")

        self.handler.log_exception(error)

        with open(self.log_file, 'r', encoding='utf-8') as f:
            log_content = f.read()
            self.assertIn("ValueError", log_content)
            self.assertIn("Test exception", log_content)

    def test_log_exception_with_context(self):
        """コンテキスト情報付きで例外をログ記録"""
        error = RuntimeError("Test runtime error")
        context = "データ処理中"

        self.handler.log_exception(error, context=context)

        with open(self.log_file, 'r', encoding='utf-8') as f:
            log_content = f.read()
            self.assertIn("RuntimeError", log_content)
            self.assertIn(context, log_content)

    def test_log_multiple_exceptions(self):
        """複数の例外を記録できる"""
        error1 = ValueError("First error")
        error2 = TypeError("Second error")

        self.handler.log_exception(error1, context="処理1")
        self.handler.log_exception(error2, context="処理2")

        with open(self.log_file, 'r', encoding='utf-8') as f:
            log_content = f.read()
            self.assertIn("ValueError", log_content)
            self.assertIn("TypeError", log_content)
            self.assertIn("処理1", log_content)
            self.assertIn("処理2", log_content)


class TestInvalidArgumentHandling(unittest.TestCase):
    """無効引数エラーハンドリングのテスト (Requirement 6.3)"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.log_file = os.path.join(self.temp_dir, "test.log")
        self.handler = ErrorHandler(log_file=self.log_file)

    def tearDown(self):
        self.handler.close()
        if os.path.exists(self.log_file):
            os.remove(self.log_file)
        os.rmdir(self.temp_dir)

    def test_handle_invalid_argument_error(self):
        """無効な引数エラーの処理"""
        error = ValueError("Invalid argument: --invalid-option")
        context = "CLI引数解析"

        message = self.handler.handle_file_error(error, context)

        self.assertIsInstance(message, str)
        self.assertIn("無効", message)


if __name__ == '__main__':
    unittest.main()
