import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="消费者原声直达", page_icon="🗣️", layout="wide")

st.title("🗣️ 消费者原声直达 (Raw Voice)")
st.markdown("""
**不做总结，只看原话。**
本工具直接调用 Google 搜索底层索引，挖掘 Amazon, Reddit, YouTube 评论区中**最真实的负面反馈片段**。
包含：**用户原话 (Verbatim)** + **来源链接 (Source)**。
""")

# --- 侧边栏 ---
with st.sidebar:
    st.header("🔑 设置")
    api_key = st.text_input("Google API Key", type="password")
    
    # 自动模型检测
    valid_model_name = None
    if api_key:
        os.environ["GOOGLE_API_KEY"] = api_key
        genai.configure(api_key=api_key)
        try:
            models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            if models:
                # 优先找 Pro 模型，搜索能力最强
                for m in models:
                    if 'gemini-1.5-pro' in m:
                        valid_model_name = m
                        break
                if not valid_model_name:
                    # 其次找 Flash
                    for m in models:
                        if 'flash' in m:
                            valid_model_name = m
                            break
                if not valid_model_name:
                    valid_model_name = models[0]
                st.success(f"✅ 连接成功")
                st.caption(f"引擎: {valid_model_name}")
            else:
                st.error("Key 无效")
        except:
            st.error("验证出错")

# --- 主界面 ---
product_name = st.text_input("输入品类名称 (例如: Cat Water Fountain)", value="")
run_btn = st.button("🔍 抓取一手差评原话", type="primary")

if run_btn and api_key and valid_model_name and product_name:
    try:
        with st.spinner("正在从 Google 索引库中提取原始数据..."):
            model = genai.GenerativeModel(valid_model_name)
            
            # --- 核心修改：搬运工模式 Prompt ---
            prompt = f"""
            你现在是一个【数据搬运工】。你的任务是利用 Google Search 工具，
            查找关于 "{product_name}" 的【真实用户负面评价】。

            ⚠️ 严格规则：
            1. **不要总结**：不要说“用户普遍反映...”，我要看具体的原话。
            2. **原文引用**：必须直接摘录 Google 搜索摘要中的用户吐槽原文（中英文皆可，保留情绪色彩）。
            3. **必须带链接**：每一条原话后面，必须附上来源 URL。
            4. **覆盖多平台**：Amazon 差评, Reddit 吐槽贴, YouTube 避雷评论。

            请输出一个表格（Markdown Table），包含 20 条左右的高质量负面反馈：
            
            | 🤬 吐槽/差评原话 (原文摘录) | 🌍 来源平台 | 🔗 证据链接 |
            | :--- | :--- | :--- |
            | (这里填入摘录的内容，例如: "Leak all over my floor after 2 days!") | Amazon | [点击跳转](URL) |
            | (例如: "Dont buy this, the pump died instantly.") | Reddit | [点击跳转](URL) |

            （请尽可能多找，挖掘最新的、最具体的抱怨）
            """
            
            response = model.generate_content(prompt)
            st.markdown(response.text)
            
    except Exception as e:
        st.error(f"出错: {e}")