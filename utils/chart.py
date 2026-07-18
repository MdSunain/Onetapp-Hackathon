# import streamlit as st
# import altair as alt
# import pandas as pd


# def render_bar_chart(df):

#     if len(df.columns) < 2:
#         st.warning("Not enough columns to render a bar chart.")
#         return

#     x = df.columns[0]
#     y = df.columns[1]

#     chart = (
#         alt.Chart(df)
#         .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
#         .encode(
#             x=alt.X(f"{x}:N", title=x),
#             y=alt.Y(f"{y}:Q", title=y),
#             tooltip=list(df.columns)
#         )
#         .properties(
#             height=420
#         )
#         .interactive()
#     )

#     st.altair_chart(chart, use_container_width=True)

# def render_chart(df, chart_type):

#     if chart_type == "bar":
#         render_bar_chart(df)

#     else:
#         st.info(f"{chart_type} chart is not implemented yet.")

import streamlit as st
import matplotlib.pyplot as plt


def render_chart(df, chart_type, x, y):

    if df.empty:
        st.warning("No data available.")
        return

    if len(df.columns) < 2:
        st.warning("Need at least two columns to generate a chart.")
        return

    x = df.columns[0]
    y = df.columns[1]

    fig, ax = plt.subplots(figsize=(8, 4))

    # ---------- BAR ----------
    if chart_type == "bar":

        bars = ax.bar(df[x], df[y])

        ax.set_xlabel(x)
        ax.set_ylabel(y)
        ax.set_title(f"{y} by {x}")

        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width()/2,
                height,
                f"{height:,.0f}",
                ha="center",
                va="bottom",
                fontsize=9
            )

    # ---------- HORIZONTAL BAR ----------
    elif chart_type == "horizontal_bar":

        bars = ax.barh(df[x], df[y])

        ax.set_xlabel(y)
        ax.set_ylabel(x)
        ax.set_title(f"{y} by {x}")

        for bar in bars:
            width = bar.get_width()
            ax.text(
                width,
                bar.get_y() + bar.get_height()/2,
                f"{width:,.0f}",
                va="center",
                fontsize=9
            )

    # ---------- LINE ----------
    elif chart_type == "line":

        ax.plot(
            df[x],
            df[y],
            marker="o",
            linewidth=2
        )

        ax.set_xlabel(x)
        ax.set_ylabel(y)
        ax.set_title(f"{y} over {x}")

    # ---------- PIE ----------
    elif chart_type == "pie":

        ax.pie(
            df[y],
            labels=df[x],
            autopct="%1.1f%%",
            startangle=90
        )

        ax.set_title(f"{y} Distribution")

    # ---------- SCATTER ----------
    elif chart_type == "scatter":

        ax.scatter(df[x], df[y])

        ax.set_xlabel(x)
        ax.set_ylabel(y)
        ax.set_title(f"{y} vs {x}")

    else:
        st.info(f"{chart_type} not supported yet.")
        return

    ax.grid(alpha=0.25)

    plt.tight_layout()

    st.pyplot(fig)