import json
from glm_api import call_glm

# ========== 加载规则库 ==========
with open("analects_kb.json", "r", encoding="utf-8") as f:
    KB = json.load(f)

def rewrite_analects(original_text, literal_score, archaic_score):
    """
    根据滑块值改写《论语》原文
    参数：
        original_text: 中文原文
        literal_score: 直译↔意译 (0-100)
        archaic_score: 古雅↔现代 (0-100)
    返回：
        生成的英文译文
    """

    # 1. 根据分数确定策略
    if literal_score <= 33:
        print("KB字典的键：", list(KB.keys()))
        literal_instruction = KB["style_mapping"]["literal_to_free"]["0-33"]
    elif literal_score <= 66:
        literal_instruction = KB["style_mapping"]["literal_to_free"]["34-66"]
    else:
        literal_instruction = KB["style_mapping"]["literal_to_free"]["67-100"]

    if archaic_score <= 33:
        archaic_instruction = KB["style_mapping"]["archaic_to_modern"]["0-33"]
    elif archaic_score <= 66:
        archaic_instruction = KB["style_mapping"]["archaic_to_modern"]["34-66"]
    else:
        archaic_instruction = KB["style_mapping"]["archaic_to_modern"]["67-100"]

    # 2. 如果原文匹配知识库中的样本，提供参考译文让AI学习
    reference_text = ""
    for sample in KB["samples"]:
        if sample["original"] == original_text:
            refs = []
            for t in sample["translations"]:
                refs.append(f"{t['translator']}: {t['text']}")
            reference_text = "参考译文：\n" + "\n".join(refs)
            break

    # 3. 构建提示词
    prompt = f"""
你是一个《论语》英译风格调节器。请将以下中文原文翻译成英文，并严格遵循风格指令。

【直译↔意译控制】（当前值 {literal_score}/100）：
{literal_instruction}

【古雅↔现代控制】（当前值 {archaic_score}/100）：
{archaic_instruction}

{reference_text}

中文原文：{original_text}

请只输出最终的英文译文，不要附加任何解释、注释或额外文本。
"""

    # 4. 调用大模型
    result = call_glm(prompt, temperature=0.5)
    return result

# ========== 快捷预设 ==========
def style_legge(text):
    """理雅各风格：直译+古雅"""
    return rewrite_analects(text, literal_score=0, archaic_score=0)

def style_kuhongming(text):
    """辜鸿铭风格：意译+现代"""
    return rewrite_analects(text, literal_score=100, archaic_score=100)

# ========== 测试 ==========
if __name__ == "__main__":
    test_text = "学而时习之，不亦说乎？"
    print("理雅各风格：", style_legge(test_text))
    print("辜鸿铭风格：", style_kuhongming(test_text))
    print("中间风格：", rewrite_analects(test_text, 50, 50))