import streamlit as st
import google.generativeai as genai
import os

# --- 页面配置 ---
st.set_page_config(page_title="全网差评挖掘机", page_icon="⛏️", layout="wide")

# --- 标题 ---
st.title("⛏️ 全网用户真实痛点/差评挖掘机")
st.markdown("""
**拒绝主观建议，只看真实反馈。**
本工具将全网扫描 **Amazon (1星/2星), Reddit, YouTube, TikTok, 垂直论坛** 等平台，
挖掘关于指定品类的**真实用户抱怨、产品缺陷、使用翻车**案例。
""")

# --- 侧边栏：设置 ---
with st.sidebar:
    st.header("🔑 第一步：输入钥匙")
    api_key = st.text_input("Google API Key", type="password")
    
    # --- 自动检测模型逻辑 ---
    valid_model_name = None
    if api_key:
        os.environ["GOOGLE_API_KEY"] = api_key
        genai.configure(api_key=api_key)
        try:
            models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            if models:
                st.success(f"✅ 连接成功！")
                # 优先寻找最新最强的模型
                for m in models:
                    if 'gemini-1.5-pro' in m: # 1.5 Pro 搜索能力更强
                        valid_model_name = m
                        break
                if not valid_model_name:
                    for m in models:
                        if 'flash' in m:
                            valid_model_name = m
                            break
                if not valid_model_name:
                    valid_model_name = models[0]
                
                st.info(f"已调用高性能侦探模型: {valid_model_name}")
            else:
                st.error("未找到可用模型，请检查 API Key 权限。")
        except Exception as e:
            st.error(f"验证失败: {e}")

# --- 主功能区 ---
col1, col2 = st.columns([3, 1])
with col1:
    product_name = st.text_input("第二步：输入品类名称 (越具体越好)", placeholder="例如：Cat Water Fountain (猫饮水机)")
with col2:
    st.write("") # 占位
    st.write("") 
    submit_btn = st.button("开始全网挖掘 ⛏️", type="primary")

if submit_btn:
    if not api_key:
        st.error("❌ 请先在侧边栏输入 Google API Key")
    elif not valid_model_name:
        st.error("❌ 模型连接失败，请检查设置")
    elif not product_name:
        st.warning("⚠️ 请输入品类名称")
    else:
        try:
            with st.spinner(f"正在潜入 Amazon, Reddit, YouTube, TikTok 挖掘 '{product_name}' 的黑料... 请耐心等待..."):
                
                model = genai.GenerativeModel(valid_model_name)
                
                # --- 核心 Prompt：极度客观、数据导向 ---
                prompt = f"""
                你现在是一个没有感情的【全网舆情数据挖掘机器人】。
                用户的查询品类是："{product_name}"。

                ❌ 严禁输出：市场建议、营销策略、未来的机会点、任何主观的“我认为”。
                ✅ 必须输出：用户原话、具体的抱怨点、真实的使用场景、发生的故障细节。

                请调用你的搜索能力和知识库，覆盖以下平台：
                1. **Amazon/Ebay** (重点关注 1星/2星 差评)
                2. **Reddit** (重点关注 r/pets, r/cats, r/dogs 等板块的避雷贴)
                3. **YouTube/TikTok** (重点关注“Don't buy this”、“Fail review”类视频下的评论)
                4. **专业垂直论坛** (如宠物主论坛)

                请按照以下结构输出报告：

                ### 1. 🤬 愤怒值最高的 3 大致命缺陷 (Fatal Flaws)
                (这里列出导致用户退货、发怒、甚至受伤的最严重问题)
                *   **缺陷点**: [简短描述]
                *   **用户原声模拟**: "[引用一句典型的愤怒评论]"
                *   **涉及平台**: [来源平台]

                ### 2. 📉 全平台差评分布矩阵 (Negative Feedback Matrix)
                请挖掘更细节的吐槽，按维度分类：
                *   **⚙️ 硬件/质量问题**: (例如：用了3天就坏、漏水、噪音大...)
                *   **🤢 体验/感官问题**: (例如：味道刺鼻、很难清洗、猫咪害怕...)
                *   **📦 物流/包装问题**: (例如：收到时已碎、缺少零件...)
                *   **🤥 虚假宣传问题**: (例如：实物比图片小、根本不耐咬...)

                ### 3. 🎬 真实翻车场景还原 (Real-life Failure Scenarios)
                请描述 2-3 个具体的使用场景，说明在这个场景下产品是如何失效的。
                (例如：半夜2点机器突然发出怪声把狗吓尿了...)

                ### 4. ⚠️ 高频避雷关键词 (Keywords Cloud)
                列出用户在差评中提到频率最高的 5-10 个关键词 (中英文对照)。

                请保持语气客观、犀利、直接。不要美化任何问题。
                """
                
                response = model.generate_content(prompt)
                
                st.markdown(response.text)
                
                # 添加一个免责提示
                st.caption("注：以上数据基于 AI 对全网公开信息的检索与聚合，仅供参考。")
                
        except Exception as e:
            st.error(f"挖掘过程中断: {e}")