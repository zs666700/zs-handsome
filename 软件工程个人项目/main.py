"""
论文查重工具
通过命令行参数接收原文、抄袭版文件路径，计算文本重复率并输出到结果文件
"""
import sys
import os
import re
import difflib


def preprocess(text):
    """
    文本预处理：去除空白、标点，英文转小写，归一化文本格式
    :param text: 原始文本字符串
    :return: 清洗后的纯有效文本
    """
    # 移除所有空白字符
    text = re.sub(r'\s+', '', text)
    # 英文统一转为小写
    text = text.lower()
    # 仅保留中文、英文、数字，过滤所有标点和特殊符号
    text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]', '', text)
    return text


def read_file(file_path):
    """
    读取文本文件，自动兼容UTF-8和GBK编码
    :param file_path: 文件绝对路径
    :return: 文件内容字符串
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='gbk') as file:
            return file.read()


def calculate_similarity(orig_text, copy_text):
    """
    计算两篇文本的重复率
    :param orig_text: 清洗后的原文
    :param copy_text: 清洗后的抄袭版文本
    :return: 重复率浮点数
    """
    if len(copy_text) == 0:
        return 0.0
    matcher = difflib.SequenceMatcher(
        None, orig_text, copy_text, autojunk=False
    )
    total_match = sum(block.size for block in matcher.get_matching_blocks())
    return total_match / len(copy_text)


def main():
    """主流程：参数解析 → 文件读取 → 预处理 → 计算 → 输出结果"""
    # 命令行参数模式（作业评测用）
    if len(sys.argv) == 4:
        orig_path = sys.argv[1]
        copy_path = sys.argv[2]
        output_path = sys.argv[3]
    # IDE本地测试模式：自动读取同目录下的测试文件
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        orig_path = os.path.join(base_dir, "orig.txt")
        copy_path = os.path.join(base_dir, "copy.txt")
        output_path = os.path.join(base_dir, "result.txt")

    # 异常处理：文件不存在时静默退出，不抛出堆栈
    try:
        orig_raw = read_file(orig_path)
        copy_raw = read_file(copy_path)
    except FileNotFoundError:
        sys.exit(1)

    # 文本预处理
    orig_clean = preprocess(orig_raw)
    copy_clean = preprocess(copy_raw)

    # 计算重复率，保留两位小数
    repeat_rate = calculate_similarity(orig_clean, copy_clean)
    result = round(repeat_rate, 2)

    # 写入结果文件
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(f"{result:.2f}")


if __name__ == "__main__":
    main()
