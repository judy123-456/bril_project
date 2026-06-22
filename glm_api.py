import requests
import json
import streamlit as st

# ============================================================
# 请选择一种模式（二选一，把另一种注释掉）：
# ============================================================

# 模式一：部署到云端时使用（从Secrets读取，不暴露Key）
API_KEY = st.secrets["ZHIPU_API_KEY"]

# 模式二：本地测试时使用（直接填Key）
# API_KEY = "你的真实智谱API Key"

# ============================================================


def call_glm(prompt, temperature=0.7, max_tokens=2000):
    """
    调用智谱GLM-4-Flash，永久免费
    参数：
        prompt: 用户输入文本
        temperature: 随机性（0-1），默认0.7
        max_tokens: 最大输出长度，默认2000
    返回：
        大模型生成的文本
    """
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "glm-4-flash",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except requests.exceptions.Timeout:
        return "请求超时，请稍后重试"
    except Exception as e:
        return f"调用出错：{str(e)}"


# ========== 测试（直接运行本文件可测试） ==========
if __name__ == "__main__":
    test_prompt = "请用一句话介绍你自己。"
    print("测试调用智谱API...")
    result = call_glm(test_prompt)
    print("返回结果：", result)