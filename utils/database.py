import re
import sqlite3
import pandas as pd


DATABASE = "business_analytics.db"
conn = sqlite3.connect(DATABASE, check_same_thread=False)


def clean_sql(sql):

    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")
    sql = sql.strip()

    return sql


def validate_sql(sql):

    sql_lower = sql.lower()

    blocked = [
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "truncate",
        "create",
        "attach",
        "pragma"
    ]

    if not sql_lower.startswith(("select", "with")):
        return False, "Only SELECT or WITH queries are allowed."

    for word in blocked:
        if word in sql_lower:
            return False, f"Blocked keyword detected: {word}"

    if "sales_inventory" not in sql_lower:
        return False, "Query must reference the sales_inventory table."

    return True, "SQL is valid."


# this executes the validated SQL query
def execute_sql(sql):

    return pd.read_sql_query(sql, conn)