"""
DataLoaderモジュールのユニットテスト

Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 7.1
"""

import unittest
import numpy as np
import os
import tempfile
import time
from pathlib import Path
import sys

# Import the module to test (will fail initially - RED phase)
sys.path.insert(0, str(Path(__file__).parent.parent))
from numpy_visualizer.data_loader import DataLoader
from numpy_visualizer.error_handler import ErrorHandler


class TestDataLoaderInitialization(unittest.TestCase):
    """DataLoaderの初期化テスト"""

    def test_init(self):
        """DataLoaderの初期化"""
        loader = DataLoader()
        self.assertIsNotNone(loader)

    def test_init_with_error_handler(self):
        """ErrorHandlerを指定して初期化"""
        error_handler = ErrorHandler()
        loader = DataLoader(error_handler=error_handler)
        self.assertIsNotNone(loader)
        self.assertEqual(loader.error_handler, error_handler)


class TestLoadNpyFile(unittest.TestCase):
    """
    .npyファイル読み込みのテスト
    Requirements: 1.1, 1.2, 1.4
    """

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.loader = DataLoader()

    def tearDown(self):
        # Clean up temp files
        for file in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file))
        os.rmdir(self.temp_dir)

    def test_load_1d_npy_file(self):
        """1次元.npyファイルの読み込み"""
        # Create test data
        test_data = np.array([1, 2, 3, 4, 5])
        test_file = Path(self.temp_dir) / "test_1d.npy"
        np.save(test_file, test_data)

        # Load data
        loaded_data = self.loader.load_data(test_file)

        self.assertIsInstance(loaded_data, np.ndarray)
        self.assertEqual(loaded_data.ndim, 1)
        np.testing.assert_array_equal(loaded_data, test_data)

    def test_load_2d_npy_file(self):
        """2次元.npyファイルの読み込み"""
        test_data = np.array([[1, 2, 3], [4, 5, 6]])
        test_file = Path(self.temp_dir) / "test_2d.npy"
        np.save(test_file, test_data)

        loaded_data = self.loader.load_data(test_file)

        self.assertIsInstance(loaded_data, np.ndarray)
        self.assertEqual(loaded_data.ndim, 2)
        np.testing.assert_array_equal(loaded_data, test_data)

    def test_load_3d_npy_file(self):
        """3次元.npyファイルの読み込み"""
        test_data = np.random.rand(3, 4, 5)
        test_file = Path(self.temp_dir) / "test_3d.npy"
        np.save(test_file, test_data)

        loaded_data = self.loader.load_data(test_file)

        self.assertIsInstance(loaded_data, np.ndarray)
        self.assertEqual(loaded_data.ndim, 3)
        np.testing.assert_array_equal(loaded_data, test_data)


class TestLoadNpzFile(unittest.TestCase):
    """
    .npzファイル読み込みのテスト
    Requirements: 1.1, 1.5
    """

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.loader = DataLoader()

    def tearDown(self):
        for file in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file))
        os.rmdir(self.temp_dir)

    def test_load_npz_single_array(self):
        """.npzファイル（単一配列）の読み込み"""
        test_data = np.array([1, 2, 3, 4, 5])
        test_file = Path(self.temp_dir) / "test_single.npz"
        np.savez(test_file, data=test_data)

        loaded_data = self.loader.load_data(test_file)

        self.assertIsInstance(loaded_data, dict)
        self.assertIn('data', loaded_data)
        np.testing.assert_array_equal(loaded_data['data'], test_data)

    def test_load_npz_multiple_arrays(self):
        """.npzファイル（複数配列）の読み込みと識別保持"""
        array1 = np.array([1, 2, 3])
        array2 = np.array([[4, 5], [6, 7]])
        array3 = np.random.rand(2, 3, 4)

        test_file = Path(self.temp_dir) / "test_multiple.npz"
        np.savez(test_file, first=array1, second=array2, third=array3)

        loaded_data = self.loader.load_data(test_file)

        self.assertIsInstance(loaded_data, dict)
        self.assertEqual(len(loaded_data), 3)
        self.assertIn('first', loaded_data)
        self.assertIn('second', loaded_data)
        self.assertIn('third', loaded_data)

        np.testing.assert_array_equal(loaded_data['first'], array1)
        np.testing.assert_array_equal(loaded_data['second'], array2)
        np.testing.assert_array_equal(loaded_data['third'], array3)


class TestFileErrorHandling(unittest.TestCase):
    """
    ファイルエラーハンドリングのテスト
    Requirement: 1.3
    """

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.error_handler = ErrorHandler(
            log_file=os.path.join(self.temp_dir, "test.log")
        )
        self.loader = DataLoader(error_handler=self.error_handler)

    def tearDown(self):
        self.error_handler.close()
        for file in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file))
        os.rmdir(self.temp_dir)

    def test_file_not_found_error(self):
        """存在しないファイルを読み込むとFileNotFoundErrorが発生"""
        nonexistent_file = Path(self.temp_dir) / "nonexistent.npy"

        with self.assertRaises(FileNotFoundError):
            self.loader.load_data(nonexistent_file)

    def test_invalid_file_format(self):
        """無効なファイル形式でValueErrorが発生"""
        invalid_file = Path(self.temp_dir) / "invalid.txt"
        with open(invalid_file, 'w') as f:
            f.write("This is not a numpy file")

        with self.assertRaises(ValueError):
            self.loader.load_data(invalid_file)


class TestArrayValidation(unittest.TestCase):
    """
    配列検証のテスト
    Requirement: 1.4
    """

    def setUp(self):
        self.loader = DataLoader()

    def test_validate_1d_array(self):
        """1次元配列の検証成功"""
        array = np.array([1, 2, 3, 4, 5])
        is_valid, message = self.loader.validate_array(array)

        self.assertTrue(is_valid)
        self.assertIn("1次元", message)

    def test_validate_2d_array(self):
        """2次元配列の検証成功"""
        array = np.array([[1, 2], [3, 4]])
        is_valid, message = self.loader.validate_array(array)

        self.assertTrue(is_valid)
        self.assertIn("2次元", message)

    def test_validate_3d_array(self):
        """3次元配列の検証成功"""
        array = np.random.rand(2, 3, 4)
        is_valid, message = self.loader.validate_array(array)

        self.assertTrue(is_valid)
        self.assertIn("3次元", message)

    def test_validate_4d_array_fails(self):
        """4次元配列は検証失敗"""
        array = np.random.rand(2, 3, 4, 5)
        is_valid, message = self.loader.validate_array(array)

        self.assertFalse(is_valid)
        self.assertIn("サポートされていません", message)

    def test_validate_0d_array_fails(self):
        """0次元配列（スカラー）は検証失敗"""
        array = np.array(42)
        is_valid, message = self.loader.validate_array(array)

        self.assertFalse(is_valid)


class TestOptimize1D(unittest.TestCase):
    """
    1次元配列最適化のテスト
    Requirement: 1.6
    """

    def setUp(self):
        self.loader = DataLoader()

    def test_optimize_already_1d(self):
        """既に1次元の配列は変更されない"""
        array = np.array([1, 2, 3, 4, 5])
        optimized = self.loader.optimize_1d(array)

        self.assertEqual(optimized.ndim, 1)
        np.testing.assert_array_equal(optimized, array)

    def test_optimize_2d_single_row(self):
        """2次元配列（1行）を1次元に最適化"""
        array = np.array([[1, 2, 3, 4, 5]])
        optimized = self.loader.optimize_1d(array)

        self.assertEqual(optimized.ndim, 1)
        self.assertEqual(optimized.shape, (5,))

    def test_optimize_2d_single_column(self):
        """2次元配列（1列）を1次元に最適化"""
        array = np.array([[1], [2], [3], [4], [5]])
        optimized = self.loader.optimize_1d(array)

        self.assertEqual(optimized.ndim, 1)
        self.assertEqual(optimized.shape, (5,))


class TestPerformance(unittest.TestCase):
    """
    パフォーマンステスト
    Requirement: 7.1
    """

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.loader = DataLoader()

    def tearDown(self):
        for file in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file))
        os.rmdir(self.temp_dir)

    def test_load_large_array_performance(self):
        """100万要素の配列を5秒以内に読み込む"""
        large_array = np.random.rand(1000000)
        test_file = Path(self.temp_dir) / "large.npy"
        np.save(test_file, large_array)

        start_time = time.time()
        loaded_data = self.loader.load_data(test_file)
        end_time = time.time()

        elapsed_time = end_time - start_time

        self.assertIsInstance(loaded_data, np.ndarray)
        self.assertEqual(loaded_data.shape, (1000000,))
        self.assertLess(elapsed_time, 5.0, f"読み込みに{elapsed_time:.2f}秒かかりました（5秒以内が必要）")


if __name__ == '__main__':
    unittest.main()
