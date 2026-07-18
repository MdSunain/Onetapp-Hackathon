import pandas as pd

PLAN = {
    "layout": [
        {
            "type": "metric_cards"
        },
        {
            "type": "summary"
        },
        {
            
            "type":"chart",
            "chart_type":"horizontal_bar",
            "x":"Week",
            "y":"Sales"
        },
        {
            "type": "table"
        }
    ]
}

RESPONSE = {

    "success": True,

    "insight": (
        "Weekly sales remained stable throughout 2022–2023, peaking during promotional periods. "
        "Revenue closely followed sales trends, indicating consistent campaign performance."
    ),

    "metrics": {

        "Revenue": "₹273.7M",

        "Weekly Sales": "4.96M",

        "Growth": "+8.3%",

        "Top Region": "South"

    },

    "table": pd.DataFrame({

        "Week": [
            "W1",
            "W2",
            "W3",
            "W4",
            "W5",
            "W6",
            "W7",
            "W8"
        ],

        "Sales": [
            43000,
            47000,
            45500,
            50000,
            52000,
            51000,
            49500,
            50500
        ]

    }),

    "recommendation": (
        "Increase promotional investment during high-performing weeks to maximize revenue while maintaining inventory availability."
    ),

    "sql": """
SELECT
    week,
    weekly_sales
FROM sales
ORDER BY week;
"""
}