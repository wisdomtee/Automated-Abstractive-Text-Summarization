import plotly.graph_objects as go


def word_count_chart(original_words, summary_words):
    """
    Create an interactive bar chart comparing
    the original article and summary word counts.
    """

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=["Original", "Summary"],
            y=[original_words, summary_words],
            text=[original_words, summary_words],
            textposition="outside",
            marker_color=["#2563EB", "#10B981"],
        )
    )

    fig.update_layout(
        title="Word Count Comparison",
        xaxis_title="Text",
        yaxis_title="Words",
        template="plotly_white",
        height=420,
        showlegend=False,
        margin=dict(l=40, r=40, t=60, b=40),
    )

    return fig


def compression_chart(compression_percentage):
    """
    Display compression percentage
    using a gauge chart.
    """

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=compression_percentage,
            title={"text": "Compression (%)"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#2563EB"},
                "steps": [
                    {"range": [0, 30], "color": "#FEE2E2"},
                    {"range": [30, 60], "color": "#FEF3C7"},
                    {"range": [60, 100], "color": "#DCFCE7"},
                ],
            },
        )
    )

    fig.update_layout(
        template="plotly_white",
        height=350,
        margin=dict(l=30, r=30, t=50, b=20),
    )

    return fig


def reading_time_chart(original_time, summary_time):
    """
    Compare reading time before
    and after summarization.
    """

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=["Original", "Summary"],
            y=[original_time, summary_time],
            text=[f"{original_time} min", f"{summary_time} min"],
            textposition="outside",
            marker_color=["#F59E0B", "#10B981"],
        )
    )

    fig.update_layout(
        title="Estimated Reading Time",
        xaxis_title="Document",
        yaxis_title="Minutes",
        template="plotly_white",
        height=420,
        showlegend=False,
        margin=dict(l=40, r=40, t=60, b=40),
    )

    return fig