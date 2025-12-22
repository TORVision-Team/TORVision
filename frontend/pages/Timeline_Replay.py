import streamlit as st
import plotly.graph_objects as go
# ---------------- PAGE CONFIG ----------------
st.set_page_config(layout="wide")
st.title("TOR Timeline Replay")

st.markdown(
    "Replay TOR traffic flow over time from entry to exit using forensic correlation"
)

# ---------------- TOR NODE POSITIONS ----------------
positions = {
    "Entry": (-4, 0),
    "M1": (-2, 1),
    "M2": (0, -1),
    "M3": (2, 1),
    "Exit": (4, 0)
}

timeline = ["Entry", "M1", "M2", "M3", "Exit"]

# ---------------- CORRELATION CONFIDENCE PER STEP ----------------
confidence_map = {
    1: 0.25,
    2: 0.45,
    3: 0.65,
    4: 0.85   # High confidence when Exit is reached
}

# ---------------- BUILD ANIMATION FRAMES ----------------
frames = []

for step in range(1, len(timeline) + 1):
    x_nodes, y_nodes, labels = [], [], []

    confidence = confidence_map.get(step, 0.1)

    for node in timeline[:step]:
        x, y = positions[node]
        x_nodes.append(x)
        y_nodes.append(y)
        labels.append(node)

    frame_data = [
        # ---- FLOW LINE (confidence-driven opacity) ----
        go.Scatter(
            x=x_nodes,
            y=y_nodes,
            mode="lines",
            line=dict(
                width=6,
                color=f"rgba(77,166,255,{confidence})"
            )
        ),

        # ---- SOFT GLOW LAYER (outer) ----
        go.Scatter(
            x=x_nodes,
            y=y_nodes,
            mode="markers",
            marker=dict(
                size=40,
                color=[
                    "rgba(255,75,75,0.15)" if node == "Exit" and confidence >= 0.8
                    else "rgba(0,255,255,0.15)"
                    for node in labels
                ]
            ),
            hoverinfo="skip"
        ),

        # ---- HALO LAYER (middle) ----
        go.Scatter(
            x=x_nodes,
            y=y_nodes,
            mode="markers",
            marker=dict(
                size=28,
                color=[
                    "rgba(255,75,75,0.35)" if node == "Exit" and confidence >= 0.8
                    else "rgba(0,255,255,0.35)"
                    for node in labels
                ]
            ),
            hoverinfo="skip"
        ),

        # ---- CORE NODE (sharp center) ----
        go.Scatter(
            x=x_nodes,
            y=y_nodes,
            mode="markers+text",
            marker=dict(
                size=16,
                color=[
                    "#ff4b4b" if node == "Exit" and confidence >= 0.8
                    else "#00ffff"
                    for node in labels
                ],
                line=dict(width=2, color="white")
            ),
            text=labels,
            textposition="bottom center"
        )
    ]

    frames.append(go.Frame(data=frame_data, name=str(step)))

# ---------------- INITIAL FIGURE ----------------
fig = go.Figure(
    data=frames[0].data,
    layout=go.Layout(
        paper_bgcolor="#0e1117",
        plot_bgcolor="#0e1117",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        title="TOR Circuit Timeline Replay",
        updatemenus=[
            {
                "type": "buttons",
                "showactive": False,
                "buttons": [
                    {
                        "label": "▶ Replay",
                        "method": "animate",
                        "args": [
                            None,
                            {
                                "frame": {"duration": 700, "redraw": True},
                                "fromcurrent": True,
                                "transition": {"duration": 300}
                            }
                        ],
                    }
                ],
            }
        ],
    ),
    frames=frames
)

# ---------------- DISPLAY ----------------
st.plotly_chart(fig, use_container_width=True)

# ---------------- LIVE CONFIDENCE METRIC ----------------
current_step = st.slider(
    "Replay Step",
    1,
    len(confidence_map),
    1
)

st.metric(
    label="Origin Correlation Confidence",
    value=f"{int(confidence_map[current_step] * 100)}%"
)