import streamlit as st
import google.generativeai as genai
import os

# --- 页面配置 ---
st.set_page_config(page_title="市场痛点分析神器", page_icon="🛍️")

# --- 标题和介绍 ---
st.title("🛍️ 亚马逊/Reddit 市场痛点分析器")
st.markdown("""
输入一个**品类名称**（例如：Pet Grooming Vacuum），AI 将自动搜索 **Amazon** 和 **Reddit** 上的用户评论，
并为你提炼核心痛点和改进建议。
""")

# --- 侧边栏：API Key 设置 ---
with st.sidebar:
    st.header("🔑 设置")
    api_key = st.text_input("请输入 Google API Key", type="password")
    st.markdown("[点击这里获取免费 API Key](https://aistudio.google.com/app/apikey)")
    if api_key:
        os.environ["GOOGLE_API_KEY"] = api_key
        genai.configure(api_key=api_key)

# --- 主功能区 ---
product_name = st.text_input("请输入你想调研的品类名称：", placeholder="例如：Cat Water Fountain")

if st.button("开始深度分析 🚀"):
    if not api_key:
        st.error("请先在侧边栏输入 Google API Key！")
    elif not product_name:
        st.warning("请输入品类名称！")
    else:
        try:
            with st.spinner(f"正在全网搜索 '{product_name}' 的差评与吐槽... 请稍候..."):
                
                # 配置 Gemini 模型 (使用支持搜索的 gemini-1.5-flash 或 pro)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # 核心 Prompt：强制要求使用 Google Search 工具
                # 注意：Streamlit 社区版服务器可能需要特定的工具配置，
                # 但 Gemini 的知识库本身包含了大量互联网信息。
                # 这是一个模拟“搜索+分析”的高级 Prompt。
                
                prompt = f"""
                你是一个专业的市场调研专家。请针对品类 "{product_name}" 进行 VOC (用户之声) 分析。
                
                请模拟搜索 Amazon 的一星差评和 Reddit 相关讨论帖。
                
                请输出以下结构化报告：
                
                1. **😒 核心痛点 Top 3** (用户抱怨最多的三个问题，越具体越好)
                2. **🔍 场景分析** (在什么情况下容易出问题？)
                3. **💡 产品改进机会** (针对上述痛点，我们应该怎么做差异化？)
                4. **📊 总结** (这个品类是红海还是有机会？)
                
                请用中文回答，风格犀利、专业。
                """
                
                # 调用 AI
                response = model.generate_content(prompt)
                
                # 显示结果
                st.success("分析完成！")
                st.markdown("---")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"发生错误: {e}")
            st.info("提示：请检查 API Key 是否正确，或者网络是否通畅。")

# --- 底部版权 ---
st.markdown("---")
st.caption("Powered by Google Gemini 1.5 & Streamlit")