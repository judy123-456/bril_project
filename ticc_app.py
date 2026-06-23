import streamlit as st
from ticc_style import rewrite_analects, style_legge, style_kuhongming

st.set_page_config(page_title="典籍译风调节器", page_icon="📜", layout="wide")
st.title("📜 典籍译风调节器 — 《论语》风格调色盘")
st.caption("基于理雅各、辜鸿铭译例归纳，面向社交媒体传播场景")

# ========== 初始化 session_state ==========
if "literal" not in st.session_state:
    st.session_state.literal = 50
if "archaic" not in st.session_state:
    st.session_state.archaic = 50
if "auto_result" not in st.session_state:
    st.session_state.auto_result = None
if "preset" not in st.session_state:
    st.session_state.preset = "自定义"

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
    
    # ========== 预设风格选择 ==========
    preset_options = ["自定义", "理雅各风格", "辜鸿铭风格", "平衡风格"]
    selected_preset = st.radio(
        "选择预设风格",
        preset_options,
        index=preset_options.index(st.session_state.preset) if st.session_state.preset in preset_options else 0,
        horizontal=True,
        key="preset_radio"
    )
    
    if selected_preset == "理雅各风格":
        st.session_state.literal = 0
        st.session_state.archaic = 0
        st.session_state.preset = "理雅各风格"
    elif selected_preset == "辜鸿铭风格":
        st.session_state.literal = 100
        st.session_state.archaic = 100
        st.session_state.preset = "辜鸿铭风格"
    elif selected_preset == "平衡风格":
        st.session_state.literal = 50
        st.session_state.archaic = 50
        st.session_state.preset = "平衡风格"
    else:
        st.session_state.preset = "自定义"
    
    literal_score = st.slider(
        "直译 ↔ 意译",
        0, 100,
        value=st.session_state.literal,
        key="literal"
    )
    archaic_score = st.slider(
        "古雅 ↔ 现代",
        0, 100,
        value=st.session_state.archaic,
        key="archaic"
    )

# ========== 生成按钮 ==========
if st.button("🎨 生成译文", type="primary"):
    if not original_text.strip():
        st.warning("请输入《论语》原文")
    else:
        with st.spinner("正在生成译文..."):
            result = rewrite_analects(original_text, literal_score, archaic_score)
            st.session_state.auto_result = result

# ========== 显示结果 ==========
if st.session_state.auto_result:
    st.markdown("---")
    st.markdown("### ✨ 生成译文")
    st.caption(f"当前参数：直译↔意译 = {st.session_state.literal}，古雅↔现代 = {st.session_state.archaic}")
    st.success(st.session_state.auto_result)

st.markdown("---")
st.markdown("💡 **使用说明**\n1. 输入或选择《论语》原文\n2. 选择预设风格或手动拖动滑块\n3. 点击生成译文查看结果")
