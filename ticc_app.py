import streamlit as st
from ticc_style import rewrite_analects, style_legge, style_kuhongming

st.set_page_config(page_title="典籍译风调节器", page_icon="📜", layout="wide")
st.title("📜 典籍译风调节器 — 《论语》风格调色盘")
st.caption("基于理雅各、辜鸿铭译例归纳，面向社交媒体传播场景")

with st.sidebar:
    st.markdown("### 🎛️ 控制面板")
    example_texts = [
        "学而时习之，不亦说乎？",
        "有朋自远方来，不亦乐乎？",
        "人不知而不愠，不亦君子乎？",
        "温故而知新，可以为师矣。",
        "吾道一以贯之。"
    ]
    selected_example = st.selectbox("快速选择示例", ["自定义"] + example_texts)
    st.markdown("---")
    st.markdown("### 📖 译文来源")
    st.markdown("""
    - 理雅各 (1893)
    - 辜鸿铭 (1898)
    - 刘殿爵 (1979)
    """)

col_input, col_sliders = st.columns([3, 2])
with col_input:
    if selected_example != "自定义":
        original_text = st.text_area("《论语》原文", selected_example, height=80)
    else:
        original_text = st.text_area("《论语》原文", "学而时习之，不亦说乎？", height=80)

with col_sliders:
    st.markdown("### 风格调节")
    literal_score = st.slider("直译 ↔ 意译", 0, 100, 50)
    archaic_score = st.slider("古雅 ↔ 现代", 0, 100, 50)

st.markdown("### ⚡ 一键预设风格")
col_preset1, col_preset2, col_preset3 = st.columns(3)
with col_preset1:
    if st.button("🏛️ 理雅各风格（直译+古雅）", use_container_width=True):
        literal_score = 0
        archaic_score = 0
        st.rerun()
with col_preset2:
    if st.button("🌿 辜鸿铭风格（意译+现代）", use_container_width=True):
        literal_score = 100
        archaic_score = 100
        st.rerun()
with col_preset3:
    if st.button("⚖️ 平衡风格（居中）", use_container_width=True):
        literal_score = 50
        archaic_score = 50
        st.rerun()

if st.button("🎨 生成译文", type="primary"):
    if not original_text.strip():
        st.warning("请输入《论语》原文")
    else:
        with st.spinner("正在生成译文..."):
            # ===== 真实调用B的接口 =====
            result = rewrite_analects(original_text, literal_score, archaic_score)

            st.markdown("---")
            st.markdown("### ✨ 生成译文")
            st.caption(f"当前参数：直译↔意译 = {literal_score}，古雅↔现代 = {archaic_score}")
            st.success(result)

st.markdown("---")
st.markdown("💡 **使用说明**\n1. 输入或选择《论语》原文\n2. 拖动滑块调节风格\n3. 点击预设风格快速切换\n4. 点击生成译文查看结果")