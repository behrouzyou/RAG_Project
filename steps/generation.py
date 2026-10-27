from config import API_KEY, CHAT_MODEL
from openai import OpenAI

from steps.logger import log


def  build_rag_prompt(query, retrieved_chunks):
    log("rag_promps")
    context = ""
    for chunk in retrieved_chunks:
        context += f"\n[source:{chunk["source"]}, chunk:{chunk['id']}]\n"
        context += chunk["text"]
        context += "\n"

    prompt = f"""
    You must answer in Persian.
    Only use the rules in the context.
    When possible, cite the supporting source in your answer.
    If the answer is not in the context, say:
    در فایل قوانین چیزی درباره این مورد پیدا نکردم.

    Context:
    {context}

    Question:
    {query}
    """



    return prompt

def generate_answer(prompt):
    log("generate_answar")
    client = OpenAI(base_url='https://api.gapgpt.app/v1', api_key=API_KEY)

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        temperature=0,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

def validate_or_format(answer):
    if answer is None:
        return "پاسخی یافت نشد"
    return answer.strip()