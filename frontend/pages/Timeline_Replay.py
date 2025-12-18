import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

# ---------------- PAGE CONFIG ----------------
st.set_page_config(layout="wide")
st.title("TOR Timeline Replay (Live Generated)")

st.markdown(
    """
    Use the timeline slider to replay TOR traffic flow from Entry to Exit.
    """
)

# ---------------- NODE POSITIONS ----------------
# These coordinates define the TOR circuit layout
positions = {
    "Entry": (-4, 0),
    "M1": (-2, 1),
    "M2": (0, -1),
    "M3": (2, 1),
    "Exit": (4, 0)
}

# ---------------- CURVED FLOW FUNCTION ----------------
def draw_curve(ax, start, end, color, alpha=0.8, lw=3):
    """
    Draws a smooth curved path between two TOR nodes
    """
    verts = [
        start,
        ((start[0] + end[0]) / 2, start[1] + 1.5),
        end
    ]
    codes = [Path.MOVETO, Path.CURVE3, Path.CURVE3]

    path = Path(verts, codes)
    patch = patches.PathPatch(
        path,
        facecolor="none",
        edgecolor=color,
        lw=lw,
        alpha=alpha
    )
    ax.add_patch(patch)

# ---------------- TIMELINE CONTROL ----------------
timeline = ["Entry", "M1", "M2", "M3", "Exit"]

current_step = st.slider(
    "Replay Timeline",
    min_value=0,
    max_value=len(timeline) - 1,
    value=0
)

# ---------------- CREATE FIGURE ----------------
fig, ax = plt.subplots(figsize=(12, 4))
fig.patch.set_facecolor("#0e1117")
ax.set_facecolor("#0e1117")

# ---------------- DRAW FLOWS BASED ON TIME ----------------
for i in range(current_step):
    start = positions[timeline[i]]
    end = positions[timeline[i + 1]]
    draw_curve(ax, start, end, color="#4da6ff", lw=4)

# ---------------- DRAW NODES ----------------
for node, (x, y) in positions.items():
    is_exit_active = node == "Exit" and current_step == len(timeline) - 1
    color = "#ff4b4b" if is_exit_active else "#4da6ff"

    ax.scatter(x, y, s=1200, color=color)
    ax.text(x, y - 0.35, node, color="white", ha="center", fontsize=11)

# ---------------- FINAL TOUCHES ----------------
ax.axis("off")
st.pyplot(fig)