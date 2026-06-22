import json
from glm_api import call_glm

# ========== 加载规则库 ==========
with open("price_rules.json", "r", encoding="utf-8") as f:
    RULES = json.load(f)

def extract_price_clause(text):
    """
    从印尼语合同文本中抽取价格条款
    参数：
        text: 合同文本（纯字符串）
    返回：
        包含price_value, tax_status, price_stability, risk_message的字典
    """
    # 先尝试关键词匹配（规则优先）
    result = {
        "price_value": "not_mentioned",
        "tax_status": "not_mentioned",
        "price_stability": "not_mentioned",
        "risk_message": "未发现明显风险",
        "method": "rule_based"
    }

    # 关键词匹配
    text_lower = text.lower()
    for keyword in RULES["risk_keywords"]["fixed"]:
        if keyword.lower() in text_lower:
            result["price_stability"] = "fixed"
            break
    if result["price_stability"] == "not_mentioned":
        for keyword in RULES["risk_keywords"]["variable"]:
            if keyword.lower() in text_lower:
                result["price_stability"] = "variable"
                break

    for keyword in RULES["risk_keywords"]["included"]:
        if keyword.lower() in text_lower:
            result["tax_status"] = "included"
            break
    if result["tax_status"] == "not_mentioned":
        for keyword in RULES["risk_keywords"]["excluded"]:
            if keyword.lower() in text_lower:
                result["tax_status"] = "excluded"
                break

    # 简单提取价格数值
    import re
    price_match = re.search(r'Rp\s*[\d\.]+', text)
    if price_match:
        result["price_value"] = price_match.group()

    # 如果规则匹配不到，调用大模型
    if result["price_stability"] == "not_mentioned" or result["tax_status"] == "not_mentioned":
        prompt = f"""
你是一个印尼语合同分析助手。请从以下文本中提取价格条款信息，以JSON格式返回：

{{
  "price_value": "价格数值和单位，如 Rp 10.000.000 per unit",
  "tax_status": "含税或税率说明（included/excluded/not_mentioned）",
  "price_stability": "固定或可变（fixed/variable/not_mentioned）",
  "risk": "一句话风险提示（简短）"
}}

文本内容：
{text}

只返回JSON，不要其他文字。
"""
        llm_result = call_glm(prompt)
        try:
            # 尝试解析JSON
            import re
            json_match = re.search(r'\{.*\}', llm_result, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                if result["price_stability"] == "not_mentioned":
                    result["price_stability"] = data.get("price_stability", "not_mentioned")
                if result["tax_status"] == "not_mentioned":
                    result["tax_status"] = data.get("tax_status", "not_mentioned")
                if result["price_value"] == "not_mentioned":
                    result["price_value"] = data.get("price_value", "not_mentioned")
                result["risk_message"] = data.get("risk", "未发现明显风险")
                result["method"] = "llm_assisted"
        except:
            result["method"] = "llm_failed"

    # 生成风险提示
    if result["risk_message"] == "未发现明显风险":
        risk_parts = []
        if "variable" in result["price_stability"]:
            risk_parts.append("价格可能变动，建议锁定")
        if "excluded" in result["tax_status"]:
            risk_parts.append("不含税费，需额外预算")
        if "reference" in str(result["price_value"]).lower():
            risk_parts.append("参考价非最终价，存在不确定性")
        if risk_parts:
            result["risk_message"] = "；".join(risk_parts) + "。本工具不替代专业法律意见。"
        else:
            result["risk_message"] = "未发现明显风险。本工具不替代专业法律意见。"

    return result

# ========== 测试 ==========
if __name__ == "__main__":
    test_text = "Harga barang tersebut adalah Rp 10.000.000 per unit, belum termasuk PPN 11% dan biaya pengiriman. Harga tetap berlaku selama 30 hari sejak tanggal penawaran."
    print("测试抽取...")
    result = extract_price_clause(test_text)
    print(json.dumps(result, indent=2, ensure_ascii=False))