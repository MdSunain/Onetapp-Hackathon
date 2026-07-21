import streamlit as st
from utils.chart import render_chart


def render_layout(plan, response, question):

    # ---------------- User ----------------

    with st.chat_message("user"):
        st.write(question)

    # ---------------- Assistant ----------------

    with st.chat_message("assistant"):
        st.markdown(
            f"""<div style="font-size:22px;
            font-weight:600;
            line-height:1.7;">
            {response["insight"]}
            </div>
            """,
        unsafe_allow_html=True
    )

    
    st.write("")

    # ----------------------------------------------------
    # Parse Planner
    # ----------------------------------------------------

    metric_block = None
    chart_block = None
    table_block = None
    recommendation_block = None

    
    for block in plan["layout"]:

        if block["type"] == "metric_cards":
            metric_block = block

        elif block["type"] == "chart":
            chart_block = block

        elif block["type"] == "table":
            table_block = block

        elif block["type"] == "recommendation":
            recommendation_block = block

    # ----------------------------------------------------
    # Supporting Analysis
    # ----------------------------------------------------

    has_supporting = any([
        metric_block,
        chart_block,
        table_block,
        recommendation_block
    ])

    if has_supporting:

        with st.expander("📊 Supporting Analysis", expanded=False):
            
            
            # ---------------- KPI ----------------

            if metric_block:
                with st.container(border=True):
                    render_metrics(response)

            # ---------------- Chart + Table ----------------

            if chart_block or table_block:

                left, right = st.columns([2,1])

                if chart_block:

                    with left:

                        with st.container(border=True):

                            st.subheader(
                                chart_block.get(
                                    "title",
                                    "Visualization"
                                )
                            )

                            render_chart(
                                response["table"],
                                chart_block["chart_type"],
                                chart_block["x"],
                                chart_block["y"]
                            )

                if table_block:

                    with right:

                        with st.container(border=True):

                            st.subheader("Supporting Data")

                            st.dataframe(
                                response["table"],
                                use_container_width=True,
                                height=350
                            )

            # ---------------- Recommendation ----------------

            if recommendation_block:

                with st.container(border=True):

                    render_recommendation(response)

    render_sql(response)


def render_metrics(response):

    metrics = response.get("metrics")

    if not isinstance(metrics, dict) or len(metrics) == 0:
        return

    cols = st.columns(len(metrics))

    colors = [
        "#EEF2FF",
        "#ECFDF5",
        "#FEF3C7",
        "#FCE7F3"
    ]

    for i, ((title, value), col) in enumerate(zip(metrics.items(), cols)):

        with col:

            with st.container(border=True):

                st.markdown(
    f"""
    <div style="background:{colors[i]};
    padding:18px;
    border-radius:14px;">

    <div style="
    font-size:14px;
    font-weight:600;
    color:#6B7280;">
    {title}
    </div>

    <div style="
    font-size:34px;
    font-weight:800;
    margin-top:12px;
    color:#111827;">
    {value}
    </div>

    </div>
    """,
    unsafe_allow_html=True)
                
def render_summary(response):

    if not response.get("insight"):
        return

    with st.container(border=True):
        st.markdown(
            f"""
        ### {response["insight"]}
        """)

    st.divider()


def render_recommendation(response):

    if not response.get("recommendation"):
        return

    st.subheader("💡 Recommendation")

    st.success(response["recommendation"])

    st.divider()

def render_chart_block(block, response):

    st.subheader(block.get("title", "Visualization"))

    render_chart(
        df=response["table"],
        chart_type=block["chart_type"],
        x=block["x"],
        y=block["y"]
    )

    st.divider()

def render_table(response):

    st.subheader("Supporting Data")

    st.dataframe(
        response["table"],
        use_container_width=True
    )

    st.divider()


def render_sql(response):

    with st.expander("Generated SQL"):

        st.code(
            response["sql"],
            language="sql"
        )