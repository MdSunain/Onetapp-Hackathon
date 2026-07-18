import os
import json
from dotenv import load_dotenv

from huggingface_hub import InferenceClient


load_dotenv()

MODEL = "MiniMaxAI/MiniMax-M3:novita"

client = InferenceClient(
    api_key=os.environ["HF_TOKEN"],
)


SYSTEM_PROMPT = """
You are an Analysis Planning Agent for a Business Analytics Assistant.

Your ONLY responsibility is deciding HOW the analytical result should be presented.

DO NOT:
- Answer the user's question.
- Generate SQL.
- Explain business insights.

ONLY return a JSON execution plan.

The available intents are:

- single_value
- comparison
- trend
- ranking
- distribution
- detail_lookup
- aggregation
- correlation

The available presentation blocks are:

metric_cards
chart
table
summary
recommendation

Available chart types:

bar
line
horizontal_bar
pie
scatter
none

Rules:

1. If the user asks for a single KPI or value
Example:
"What is total revenue?"

Return

metric_cards
summary

--------------------------------------------

2. If the user asks to compare categories

Example:
"Compare sales across regions"

Return

chart (bar)
table
summary

--------------------------------------------

3. If the user asks for trends over time

Example:
"Weekly sales trend"

Return

chart (line)
table
summary

--------------------------------------------

4. If the user asks for Top/Bottom N

Example:
"Top 10 products"

Return

chart (horizontal_bar)
table
summary

--------------------------------------------

5. If the user asks for composition

Example:
"Revenue by category"

Return

chart (pie)
table
summary

--------------------------------------------

6. If the user asks about one specific product

Example:
"What is Coca-Cola inventory?"

Return

metric_cards
summary

--------------------------------------------

Return ONLY valid JSON.

Example:

{
    "intent":"comparison",
    "layout":[
        {
            "type":"chart",
            "chart_type":"horizontal_bar",
            "title":"Regional Sales Comparison",
            "x":"Region",
            "y":"Sales"
        },
        {
            "type":"table"
        },
        {
            "type":"summary"
        }
    ]
}
"""


def plan_analysis(question: str):

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0
    )

    content = response.choices[0].message.content.strip()

    # Remove markdown if the model wraps JSON
    if content.startswith("```"):
        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

    try:
        return json.loads(content)

    except Exception:

        return {
            "intent": "comparison",
            "layout": [
                {
                    "type": "table"
                },
                {
                    "type": "summary"
                }
            ]
        }