import fitz
from openai import OpenAI

# 读取PDF
doc = fitz.open("case.pdf")

text = ""

for page in doc:
    text += page.get_text()

print("PDF读取成功！")

# 连接Qwen
client = OpenAI(
    api_key="sk-ws-H.RYRHRII.IV9p.MEUCIQC5IDaP0T00JyiXAMENZhLtFSWW5JWR1Oo8e3Rw7YAe-QIgKvlo3PglxIRvymsGQrxqLMTpVeYycQoulN0L3xcioo4",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 提示词
prompt = f"""
请从下面的病例报告中提取关键医学实体。

请提取以下五类实体：

1. disease（疾病）
2. symptoms（症状）
3. examinations（检查）
4. treatments（治疗）
5. medications（药物）

要求：

1. 必须返回合法JSON。
2. 不允许输出任何解释。
3. 所有实体放入列表。
4. 输出格式必须严格如下：

{{
    "disease": [],
    "symptoms": [],
    "examinations": [],
    "treatments": [],
    "medications": []
}}

病例内容：

{text}
"""

# 调用模型
response = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

result = response.choices[0].message.content

print(result)

# 保存结果
with open(
    "medical_entities.json",
    "w",
    encoding="utf-8"
) as f:
    f.write(result)

print("结果已保存。")