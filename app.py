import streamlit as st

st.set_page_config(page_title="Interactive Bowtie Diagram", layout="wide")
st.title("🧠 Interactive Bowtie Diagram")

# --- Session state for nodes ---
if "nodes" not in st.session_state:
    st.session_state.nodes = [
        ("t1", 80, 200, "Threat A", "threat"),
        ("b1", 220, 200, "Barrier A", "barrier"),
        ("h", 360, 200, "Hazard", "hazard"),
        ("b2", 520, 200, "Barrier B", "barrier"),
        ("c1", 660, 200, "Consequence", "consequence"),
    ]

# --- Buttons ---
col1, col2 = st.columns([1, 1])
with col1:
   if st.button("➕ Add Node"):
    new_index = len(st.session_state.nodes) + 1
    new_id = f"n{new_index}"
    st.session_state.nodes.append(
        (new_id, 150 + new_index * 80, 350, f"Node {new_index}", "barrier")
    )        
with col2:
    if st.button("🔄 Reset Diagram"):
        st.session_state.nodes = [
            ("t1", 80, 200, "Threat A", "threat"),
            ("b1", 220, 200, "Barrier A", "barrier"),
            ("h", 360, 200, "Hazard", "hazard"),
            ("b2", 520, 200, "Barrier B", "barrier"),
            ("c1", 660, 200, "Consequence", "consequence"),
        ]

nodes = st.session_state.nodes

# --- Build HTML dynamically ---
node_js_array = "\n".join(
    [f"node('{n[0]}', {n[1]}, {n[2]}, '{n[3]}', '{n[4]}');" for n in nodes]
)

html_code = f"""
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <style>
      html, body {{
        margin: 0;
        height: 100%;
        overflow: hidden;
        background-color: #f7f9fc;
        font-family: Arial, sans-serif;
      }}
      .node {{
        position: absolute;
        padding: 10px 20px;
        border-radius: 8px;
        color: #222;
        font-weight: 500;
        box-shadow: 2px 2px 4px rgba(0,0,0,0.2);
      }}
      .hazard {{ background: #ffcccc; border: 2px solid #cc0000; }}
      .threat {{ background: #fff3cd; border: 2px solid #ffcc00; }}
      .barrier {{ background: #e6ffe6; border: 2px solid #009900; }}
      .consequence {{ background: #e0ecff; border: 2px solid #0066cc; }}
      .edge {{
        position: absolute;
        height: 3px;
        background: #444;
        transform-origin: 0 0;
      }}
    </style>
  </head>
  <body>
    <div id="diagram"></div>
    <script>
      const diagram = document.getElementById("diagram");

      function node(id, x, y, text, cls) {{
        const el = document.createElement("div");
        el.id = id;
        el.className = "node " + cls;
        el.textContent = text;
        el.style.left = x + "px";
        el.style.top = y + "px";
        el.draggable = true;
        el.ondragend = (e) => {{
          el.style.left = e.pageX - 40 + "px";
          el.style.top = e.pageY - 20 + "px";
          redraw();
        }};
        diagram.appendChild(el);
        return el;
      }}

      function edge(id1, id2) {{
        const a = document.getElementById(id1).getBoundingClientRect();
        const b = document.getElementById(id2).getBoundingClientRect();
        const line = document.createElement("div");
        line.className = "edge";
        const x1 = a.left + a.width;
        const y1 = a.top + a.height / 2;
        const x2 = b.left;
        const y2 = b.top + b.height / 2;
        const dx = x2 - x1;
        const dy = y2 - y1;
        const length = Math.sqrt(dx * dx + dy * dy);
        const angle = Math.atan2(dy, dx) * 180 / Math.PI;
        line.style.width = length + "px";
        line.style.left = x1 + "px";
        line.style.top = y1 + "px";
        line.style.transform = "rotate(" + angle + "deg)";
        diagram.appendChild(line);
      }}

      function redraw() {{
        document.querySelectorAll(".edge").forEach(e => e.remove());
        if (document.getElementById("t1") && document.getElementById("b1")) edge("t1", "b1");
        if (document.getElementById("b1") && document.getElementById("h")) edge("b1", "h");
        if (document.getElementById("h") && document.getElementById("b2")) edge("h", "b2");
        if (document.getElementById("b2") && document.getElementById("c1")) edge("b2", "c1");
      }}

      // --- Build nodes dynamically from Python ---
      {node_js_array}

      redraw();
    </script>
  </body>
</html>
"""

st.components.v1.html(html_code, height=500, scrolling=False)
