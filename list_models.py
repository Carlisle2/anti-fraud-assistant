import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

try:
    models = client.models.list()
    print("✅ 当前账号可用的模型：")
    for model in models.data:
        print(f" - {model.id}")
except Exception as e:
    print(f"❌ 获取模型列表失败：{e}")