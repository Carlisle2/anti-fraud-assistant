import os
from dotenv import load_dotenv
from openai import OpenAI

# 加载 .env 文件中的环境变量
load_dotenv()

# 从环境变量中读取 API Key
api_key = os.getenv("DASHSCOPE_API_KEY")

# 创建 OpenAI 兼容客户端，指向阿里云百炼的接口地址
client = OpenAI(
    api_key=api_key,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 调用 qwen-plus 模型进行测试
try:
    response = client.chat.completions.create(
        model="qwen-plus",
        messages=[
            {"role": "system", "content": "你是一个测试助手。"},
            {"role": "user", "content": "请回复：连接成功"},
        ],
        temperature=0.1,
    )
    result = response.choices[0].message.content
    print("✅ 测试成功！模型返回内容：")
    print(result)
    print(f"\n实际使用的模型：{response.model}")
except Exception as e:
    print(f"❌ 测试失败，错误信息：{e}")