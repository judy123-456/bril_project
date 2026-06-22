import streamlit as st
import json
from utils import extract_text_from_bytes
from bril_extractor import extract_price_clause

st.set_page_config(page_title="丝路贸易AI文档助手", page_icon="📄", layout="wide")
st.title("📄 丝路贸易AI文档助手 — 价格条款抽取")
st.caption("支持印尼语销售确认书/采购订单的价格条款自动抽取与风险提示")

with st.sidebar:
    st.markdown("### 关于本工具")
    st.markdown("""
    - 支持格式：PDF、Word、TXT
    - 抽取字段：价格数值、税费状态、价格稳定性
    - 风险等级：低/中/高
    """)
    st.markdown("---")
    st.markdown("### 免责声明")
    st.markdown("⚠️ **本工具不替代专业法律意见**")

uploaded_file = st.file_uploader("上传印尼语销售确认书或采购订单", type=["pdf", "docx", "txt"])

if uploaded_file is not None:
    st.info(f"已上传：{uploaded_file.name} ({uploaded_file.size} bytes)")
    if st.button("🔍 抽取并分析", type="primary"):
        with st.spinner("正在分析合同条款..."):
            # ===== 真实调用B的接口 =====
            file_bytes = uploaded_file.read()
            file_type = uploaded_file.name.split('.')[-1]
            text = extract_text_from_bytes(file_bytes, file_type)
            result = extract_price_clause(text)

            st.markdown("---")
            st.markdown("### 📊 抽取结果")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("💰 价格数值", result.get("price_value", "未检测到"))
            with col2:
                tax_display = {
                    "included": "✅ 含税",
                    "excluded": "⚠️ 不含税",
                    "not_mentioned": "❓ 未提及"
                }.get(result.get("tax_status", ""), result.get("tax_status", "未检测到"))
                st.metric("📋 税费状态", tax_display)
            with col3:
                stability_display = {
                    "fixed": "✅ 固定价格",
                    "variable": "⚠️ 可变价格",
                    "not_mentioned": "❓ 未提及"
                }.get(result.get("price_stability", ""), result.get("price_stability", "未检测到"))
                st.metric("📌 价格稳定性", stability_display)

            st.markdown("---")
            risk_message = result.get("risk_message", "未发现明显风险")
            if "极高" in risk_message or "高风险" in risk_message or "变量" in risk_message.lower():
                st.error(f"🔴 风险提示：{risk_message}")
            elif "不含" in risk_message or "注意" in risk_message:
                st.warning(f"🟡 风险提示：{risk_message}")
            else:
                st.success(f"🟢 {risk_message}")
            st.caption(f"判断方法：{result.get('method', 'unknown')}")