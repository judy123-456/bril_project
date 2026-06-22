import tempfile
import os

def extract_text_from_bytes(file_bytes, file_type):
    """
    从上传的文件字节流中提取纯文本
    简化为直接解码 txt，如果是 PDF/Word 会提示
    """
    if file_type == 'txt':
        try:
            return file_bytes.decode('utf-8')
        except:
            return file_bytes.decode('latin-1')
    elif file_type == 'pdf':
        # 如果没装 pdfplumber，提示用户
        return "PDF解析需要安装 pdfplumber。请运行：pip install pdfplumber"
    elif file_type == 'docx':
        return "Word解析需要安装 python-docx。请运行：pip install python-docx"
    else:
        return f"不支持的文件格式：{file_type}"