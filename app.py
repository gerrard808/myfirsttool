import streamlit as st
import google.generativeai as genai
import os

# --- 页面配置 ---
st.set_page_config(page_title="市场痛点分析神器", page_icon="🛍️")

# --- 标题 ---
st.title("🛍️ 亚马逊/Reddit 市场痛点分析器")

# --- 侧边栏：设置 ---
with st.sidebar:
    st.header("🔑 第一步：输入钥匙")
    api_key = st.text_input("Google API Key", type="password")
    
    # --- 侦探功能：自动检测可用模型 ---
    valid_model_name = None
    if api_key:
        os.environ["GOOGLE_API_KEY"] = api_key
        genai.configure(api_key=api_key)
        try:
            # 获取支持内容生成的模型列表
            models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            if models:
                st.success(f"✅ 连接成功！")
                # 默认优先找 flash 或 pro 模型
                for m in models:
                    if 'flash' in m:
                        valid_model_name = m
                        break
                if not valid_model_name:
                    valid_model_name = models[0] # 如果没找到flash，就用第一个
                
                st.info(f"已自动选择模型: {valid_model_name}")
            else:
                st.error("你的 API Key 没有找到任何可用模型，请检查 Key 是否开通了权限。")
        except Exception as e:
            st.error(f"API Key 验证失败: {e}")

# --- 主功能区 ---
product_name = st.text_input("第二步：输入品类名称", placeholder="例如：Dog Chew Toy")

if st.button("开始深度分析 🚀"):
    if not api_key:
        st.error("请先在侧边栏输入 Google API Key！")
    elif not valid_model_name:
        st.error("未能找到可用的 AI 模型，请检查侧边栏的连接状态。")
    elif not product_name:
        st.warning("请输入品类名称！")
    else:
        try:
            with st.spinner(f"正在使用 {valid_model_name} 进行全网搜索与分析..."):
                
                # 使用自动检测到的模型名字
                model = genai.GenerativeModel(valid_model_name)
                
                prompt = f"""
                你是一个专业的市场调研专家。请针对品类 "{product_name}" 进行 VOC (用户之声) 分析。
                请模拟搜索 Amazon 的一星差评和 Reddit 相关讨论帖。
                
                请输出以下结构化报告：
                1. **😒 核心痛点 Top 3** (用户抱怨最多的三个问题)
                2. **🔍 场景分析** (什么情况下容易出问题？)
                3. **💡 产品改进机会** (我们应该怎么做差异化？)
                4. **📊 总结** (红海还是蓝海？)
                
                请用中文回答，风格犀利、专业。
                """
                
                response = model.generate_content(prompt)
                st.success("分析完成！")
                st.markdown("---")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"发生错误: {e}")