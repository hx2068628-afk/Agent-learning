import hashlib
import os

from langchain_community.document_loaders import PyPDFLoader, TextLoader

from logger_handler import logger


def get_file_md5_hex(filepath):
    if not os.path.exists(filepath):
        logger.error(f"文件不存在: {filepath}")
        return None
    if not os.path.isfile(filepath):
        logger.error(f"路径不是普通文件: {filepath}")
        return None

    md5_obj = hashlib.md5()
    chunk_size = 4096
    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(chunk_size):
                md5_obj.update(chunk)
        return md5_obj.hexdigest()
    except Exception as e:
        logger.error(f"计算文件 MD5 失败: {filepath}, 错误信息: {str(e)}")
        return None


def listdir_with_allowed_type(path, allowed_types):
    files = []
    if not os.path.isdir(path):
        logger.error(f"[listdir_with_allowed_type]目录不存在或不是目录: {path}")
        return tuple(files)

    for f in os.listdir(path):
        if f.endswith(allowed_types):
            files.append(os.path.join(path, f))
    return tuple(files)


def pdf_loader(filepath, passwd=None):
    return PyPDFLoader(filepath, passwd).load()


def txt_loader(filepath):
    encodings = ["utf-8", "utf-8-sig", "gb18030", "gbk"]
    last_error = None
    for encoding in encodings:
        try:
            return TextLoader(filepath, encoding=encoding).load()
        except Exception as e:
            last_error = e

    logger.error(f"文本文件读取失败: {filepath}, 错误信息: {str(last_error)}")
    raise last_error
