"""
论文查重程序单元测试
覆盖预处理、文件读取、查重核心、异常分支四大模块
"""
import unittest
import os
import sys

# 自动将当前文件所在目录加入Python搜索路径，彻底解决模块导入失败问题
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from main import preprocess, read_file, calculate_similarity


class TestPlagiarismChecker(unittest.TestCase):
    """测试用例集合"""

    def setUp(self):
        """测试前置：创建临时测试目录和文件路径"""
        self.test_dir = os.path.dirname(os.path.abspath(__file__))
        self.test_file = os.path.join(self.test_dir, "test_tmp.txt")

    def tearDown(self):
        """测试后置：清理临时文件"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    # ==================== 1. preprocess 预处理测试（4个） ====================
    def test_preprocess_mixed_content(self):
        """测试1：中英文混合、带标点空格的文本清洗"""
        text = "你好，世界！ Hello World. 123"
        self.assertEqual(preprocess(text), "你好世界helloworld123")

    def test_preprocess_empty_text(self):
        """测试2：空文本输入"""
        self.assertEqual(preprocess(""), "")

    def test_preprocess_only_punctuation(self):
        """测试3：纯标点符号文本，清洗后为空"""
        text = "，。！？；：\"\"'()【】"
        self.assertEqual(preprocess(text), "")

    def test_preprocess_english_case(self):
        """测试4：英文大小写统一转为小写"""
        text = "Python JAVA C++"
        self.assertEqual(preprocess(text), "pythonjavac")

    # ==================== 2. read_file 文件读取测试（2个） ====================
    def test_read_file_utf8(self):
        """测试5：读取UTF-8编码文件"""
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write("UTF-8测试文本")
        self.assertEqual(read_file(self.test_file), "UTF-8测试文本")

    def test_read_file_gbk(self):
        """测试6：读取GBK编码文件（编码兼容性）"""
        with open(self.test_file, 'w', encoding='gbk') as f:
            f.write("GBK测试文本")
        self.assertEqual(read_file(self.test_file), "GBK测试文本")

    # ==================== 3. 查重核心逻辑测试（5个） ====================
    def test_similarity_full_match(self):
        """测试7：完全相同的文本，重复率为1.0"""
        orig = preprocess("今天是星期天，天气晴，晚上去看电影")
        copy = preprocess("今天是星期天，天气晴，晚上去看电影")
        self.assertAlmostEqual(calculate_similarity(orig, copy), 1.0, places=2)

    def test_similarity_no_match(self):
        """测试8：完全不同的文本，重复率接近0"""
        orig = preprocess("今天天气很好适合出门")
        copy = preprocess("人工智能技术发展迅速")
        self.assertAlmostEqual(calculate_similarity(orig, copy), 0.0, places=2)

    def test_similarity_partial_match(self):
        """测试9：部分相似的文本"""
        orig = preprocess("今天天气真好适合出门散步")
        copy = preprocess("今天下雨适合在家休息")
        self.assertAlmostEqual(calculate_similarity(orig, copy), 0.4, places=2)

    def test_similarity_empty_copy(self):
        """测试10：抄袭版文件为空，避免除零错误，返回0"""
        orig = preprocess("原文内容")
        copy = preprocess("")
        self.assertEqual(calculate_similarity(orig, copy), 0.0)

    def test_similarity_single_char_diff(self):
        """测试11：单字差异场景"""
        orig = preprocess("你好世界")
        copy = preprocess("你好视界")
        self.assertAlmostEqual(calculate_similarity(orig, copy), 0.75, places=2)

    # ==================== 4. 异常分支测试（1个） ====================
    def test_main_file_not_found(self):
        """测试12：文件不存在时程序正常退出，返回退出码1"""
        # 模拟命令行参数，传入不存在的文件
        sys.argv = ["main.py", "no_file.txt", "copy.txt", "out.txt"]
        with self.assertRaises(SystemExit) as cm:
            from main import main
            main()
        self.assertEqual(cm.exception.code, 1)


if __name__ == '__main__':
    unittest.main()