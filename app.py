import os
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st

# 加载 .env 文件中的环境变量
load_dotenv()

# 从环境变量中读取 API Key
api_key = os.getenv("DASHSCOPE_API_KEY")

# 创建 OpenAI 兼容客户端，指向阿里云百炼的接口地址
client = OpenAI(
    api_key=api_key,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 第二版提示词
SYSTEM_PROMPT = """你是一名面向普通用户的智能反诈风险辅助分析助手，主要帮助50岁左右的用户快速判断收到的短信、聊天信息或电话话术是否存在潜在诈骗风险。

请根据用户提供的信息进行分析，重点关注以下内容：
1. 是否存在陌生链接、二维码或诱导点击行为；
2. 是否存在要求转账、付款或进行其他资金操作的行为；
3. 是否存在索要验证码、密码、银行卡信息等敏感信息的行为；
4. 是否存在冒充客服、银行、政府机关、平台工作人员、熟人等身份的情况；
5. 是否存在"立即处理""否则将产生严重后果"等制造紧迫感、恐慌感或利益诱惑的表达。

请严格按照以下格式进行回答：
1. 能不能相信：首先用一句简单、明确的话直接告诉用户："可以暂时相信" / "建议暂时不要相信" / "高度可疑，请停止操作"。
2. 风险等级：明确给出：低风险 / 中风险 / 高风险。
3. 为什么有风险：最多列出3点，使用简单、通俗的语言，不使用复杂的专业术语。
4. 现在应该怎么办：最多给出3条具体、可以直接执行的建议。

安全要求：
1. 优先给出明确结论，避免让用户阅读大量内容后才能知道是否存在风险；
2. 内容简洁，避免重复表达；
3. 不夸大或制造恐慌；
4. 不能仅凭一段信息直接认定对方一定构成诈骗；
5. 如果无法确定真实性，应明确告诉用户需要通过官方渠道进一步核实；
6. 如果涉及转账、陌生链接、验证码或个人敏感信息，应优先提醒用户暂停操作。"""


def analyze_message(user_input: str) -> str:
    """将用户输入的信息与提示词组合，调用大模型进行分析，并返回结果。"""
    response = client.chat.completions.create(
        model="qwen-plus",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input},
        ],
        temperature=0.1,
    )
    return response.choices[0].message.content


# ---------------- Streamlit 界面 ----------------

# 页面基本设置
st.set_page_config(
    page_title="AI 智能反诈助手",
    page_icon="🛡️",
    layout="centered",
)

# 标题
st.title("🛡️ AI 智能反诈助手")

# 服务说明
st.markdown(
    """
    本助手帮助您快速判断收到的短信、聊天信息或电话话术是否存在诈骗风险。
    请输入您收到的可疑信息，系统会给出风险分析和处理建议。
    """
)

# 隐私保护提醒
st.warning("⚠️ 请勿输入身份证号码、银行卡密码、支付密码、验证码等敏感信息。")

# 用户输入区域
user_input = st.text_area(
    label="请输入您收到的可疑短信或电话内容：",
    height=150,
    placeholder="例如：您好，我是某银行客服。系统检测到您的银行卡存在异常交易，请您立即提供手机验证码...",
)

# 分析按钮
if st.button("开始分析", type="primary", use_container_width=True):
    if not user_input.strip():
        st.error("请输入需要分析的信息内容。")
    else:
        with st.spinner("正在分析，请稍候..."):
            try:
                result = analyze_message(user_input.strip())
                st.success("分析完成")
                st.markdown("### 分析结果")
                st.markdown(result)
            except Exception as e:
                st.error(f"分析过程中出现错误：{e}")

# 免责声明
st.markdown("---")
st.caption(
    "本服务仅作为诈骗风险辅助分析工具，不能替代公安机关、银行、通信运营商或其他官方机构的判断。"
)