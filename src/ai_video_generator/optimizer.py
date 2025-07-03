from openai import OpenAI
import json, re

client = OpenAI(
    api_key=input("你的API密钥:"),
    base_url="https://api.deepseek.com"
)


def optimize_text_and_generate_tags(text: str, style: str = "二次元") -> list[dict]:
    """
    将文本逐句优化，并为每句生成风格提示词，返回结构化列表
    """
    prompt = f"""
你是一个风格优化助手，请将用户提供的多句自然语言文本进行优化，并输出为如下结构：
1. 优化后每一句话逻辑清晰，语言优美；
2. 为每句话添加3个风格提示词（风格为：{style}）；
3. 输出为 JSON 数组，格式为：
[
  {{
    "sentence": "原始句子",
    "optimized": "优化后句子",
    "tags": ["tag1", "tag2", "tag3"]
  }},
  ...
]
用户文本如下：
{text}
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个中文文本风格优化助手"},
            {"role": "user", "content": prompt},
        ],
        stream=False,
    )

    content = response.choices[0].message.content
    try:
        json_text = re.search(r"\[\s*{.*?}\s*\]", content, re.DOTALL).group()
        return json.loads(json_text)
    except:
        print("⚠️ 无法解析返回内容：\n", content)
        return []
