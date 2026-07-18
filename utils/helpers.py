from utils.ai import generate_sql
from utils.ai import generate_business_insight

from utils.database import clean_sql
from utils.database import validate_sql
from utils.database import execute_sql
from utils.metric import extract_metrics

def ask_business_assistant(question):
    sql = generate_sql(question)

    sql = clean_sql(sql)

    valid, message = validate_sql(sql)

    if not valid:

        return {
            "success": False,
            "error": message
        }

    result = execute_sql(sql)
    metrics = extract_metrics(result)
    insight = generate_business_insight(
        question,
        result
    )

    return {

        "success": True,
        "sql": sql,
        "table": result,
        "metrics":metrics,
        "insight": insight
    }