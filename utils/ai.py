
from dotenv import load_dotenv
import os
from huggingface_hub import InferenceClient

from utils.prompts import SYSTEM_PROMPT

load_dotenv()

client = InferenceClient(
    api_key=os.environ["HF_TOKEN"],
)

MODEL = "MiniMaxAI/MiniMax-M3:novita"


def generate_sql(question):

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return response.choices[0].message.content



def generate_business_insight(question, result_df):

    table = result_df.to_string(index=False)

    prompt = f"""
            You are a Business Intelligence Analyst.
            A business user asked:

            {question}

            The SQL query has already been executed.

            The result is:

            {table}

            Instructions:

            1. Use ONLY the numbers shown.
            2. Never invent values.
            3. Give a concise business explanation.
            4. Mention trends if visible.
            
            Rules:
            - Maximum 2 sentences.
            - Maximum 35 words.
            - Mention only the most important business insight.
            - Use plain English suitable for executives.
            - No headings.
            - No HTML.
            - No Markdown.
            - No bullet points.
            - No recommendations.
            - Return only the summary text.
        """

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content