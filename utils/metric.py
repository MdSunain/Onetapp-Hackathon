import pandas as pd


def extract_metrics(df):

    metrics = {}

    if df.empty:
        return metrics

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    text_cols = df.select_dtypes(exclude="number").columns.tolist()

    # -------------------------
    # Case 1
    # One row -> every numeric column becomes a KPI
    # -------------------------

    if len(df) == 1:

        row = df.iloc[0]

        for col in numeric_cols:
            metrics[col] = row[col]

        return metrics

    # -------------------------
    # Case 2
    # One category + one numeric value
    # -------------------------

    if len(numeric_cols) == 1 and len(text_cols) == 1:

        value_col = numeric_cols[0]
        label_col = text_cols[0]

        idx = df[value_col].idxmax()

        metrics[f"Highest {value_col}"] = df.loc[idx, value_col]
        metrics["Top " + label_col] = df.loc[idx, label_col]

        return metrics

    # -------------------------
    # Case 3
    # Time series
    # -------------------------

    if len(numeric_cols) == 1 and len(df) > 1:

        value_col = numeric_cols[0]

        metrics["Latest"] = df[value_col].iloc[-1]
        metrics["Average"] = round(df[value_col].mean(), 2)

        return metrics

    # -------------------------
    # Fallback
    # -------------------------

    for col in numeric_cols[:4]:
        metrics[col] = round(df[col].sum(), 2)

    return metrics


def render_table(df):
    df.dataframe(
                    use_container_width=True,
                    height=430
                )