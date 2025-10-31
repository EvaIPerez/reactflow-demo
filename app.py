import streamlit as st
st.set_page_config(page_title="Bowtie Risk Diagram", layout="wide")
st.title("🎯 Bowtie Risk Diagram Builder (Aligned & Single Hazard)")

# --- Default structure ---
default_nodes = [
    ("haz1", 400, 60, "Hazard", "hazard"),
    ("top1", 400, 220, "Top Event", "topevent"),
]
default_edges = [("haz1", "top1")]

if "nodes" not in st.session_state:
    st.session_state.nodes = default_nodes.copy()
if "edges" not in st.session_state:
    st.session_state.edges = default_edges.copy()

# --- Sidebar Controls ---
st.sidebar.header("Add / Edit Nodes")

# Find the single Hazard
hazard_node = [n for n in st.session_state.nodes if n[4] == "hazard"][0]
hazard_index = st.session_state.nodes.index(hazard_node)

# Hazard label editing
hazard_label = st.sidebar.text_input("Hazard label:", value=hazard_node[3])
if st.sidebar.button("💾 Update Hazard"):
    st.session_state.nodes[hazard_index] = (
        hazard_node[0],
        hazard_node[1],
        hazard_node[2],
        hazard_label,
        "hazard",
    )

# Add other nodes
node_type = st.sidebar.selectbox(
    "Select Node Type:",
    [
        "Top Event",
        "Threat",
        "Preventive Barrier",
        "Mitigation Barrier",
        "Consequence",
    ],
)
label_input = st.sidebar.text_input("Label for new node:", value=f"New {node_type}")
add_button = st.sidebar.button("➕ Add Node")

# --- Positioning constants ---
X = {
    "hazard": 400,
    "topevent": 400,
    "threat": 120,
    "barrier_L": 250,
    "barrier_R": 550,
    "consequence": 700,
}
Y_BASE = 150
Y_SPACING = 80

# --- Helpers ---
def nodes_of(cls):
    return [n for n in st.session_state.nodes if n[4] == cls]

def add_edge(a, b):
    st.session_state.edges.append((a, b))

# --- Add Logic ---
if add_button:
    new_id = f"n{len(st.session_state.nodes)+1}"
    label = label_input.strip() if label_input else node_type
    y = Y_BASE

    if node_type == "Top Event":
        st.session_state.nodes.append((new_id, X["topevent"], 220, label, "topevent"))
        add_edge("haz1", new_id)

    elif node_type == "Threat":
        threats = nodes_of("threat")
        y = Y_BASE + len(threats) * Y_SPACING
        st.session_state.nodes.append((new_id, X["threat"], y, label, "threat"))
        add_edge(new_id, "top1")

    elif node_type == "Preventive Barrier":
        barriers = nodes_of("barrier_L")
        y = Y_BASE + len(barriers) * Y_SPACING
        st.session_state.nodes.append((new_id, X["barrier_L"], y, label, "barrier_L"))
        threats = nodes_of("threat")
        if threats:
            add_edge(threats[-1][0], new_id)
        add_edge(new_id, "top1")

    elif node_type == "Mitigation Barrier":
        barriers = nodes_of("barrier_R")
        y = Y_BASE + len(barriers) * Y_SPACING
        st.session_state.nodes.append((new_id, X["barrier_R"], y, label, "barrier_R"))
        add_edge("top1", new_id)

    elif node_type == "Consequence":
        cons = nodes_of("consequence")
        y = Y_BASE + len(cons) * Y_SPACING
        st.session_state.nodes.append((new_id, X["consequence"], y, label, "consequence"))
        add_edge("top1", new_id)

# --- Reset Button ---
if st.button("🔄 Reset Diagram"):
    st.session_state.nodes = default_nodes.copy()
    st.session_state.edges = default_edges.copy()

nodes = st.session_state.nodes
edges = st.session_state.edges

# --- JS Data ---
node_js = "\n".join(
    [f"node('{n[0]}', {n[1]}, {n[2]}, '{n[3]}', '{n[4]}');" for n in nodes]
)
edge_js = "\n".join([f"edge('{a}', '{b}');" for (a, b) in edges])

# --- HTML & JS rendering ---
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
      background: #f8fafc;
      font-family: Arial, sans-serif;
    }}
    .node {{
      position: absolute;
      padding: 10px 20px;
      border-radius: 6px;
      font-weight: 500;
      color: #222;
      text-align: center;
      box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
    }}
    .hazard {{
      background: white;
      border: 2px solid black;
      position: relative;
      width: 160px;
    }}
    .hazard::before {{
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 20px;
      background: repeating-linear-gradient(
        45deg,
        #fff200,
        #fff200 10px,
        #000 10px,
        #000 20px
      );
      border-bottom: 1px solid #000;
      border-top-left-radius: 6px;
      border-top-right-radius: 6px;
    }}
    .topevent {{
      background: #28a745;
      border: 3px solid #155724;
      color: #fff;
      width: 120px;
      height: 60px;
      line-height: 60px;
    }}
    .threat {{
      background: #fff3cd;
      border: 2px solid #ffcc00;
      width: 140px;
    }}
    .barrier_L, .barrier_R {{
      background: #cce5ff;
      border: 2px solid #007bff;
      width: 140px;
    }}
    .consequence {{
      background: #f8d7da;
      border: 2px solid #dc3545;
      width: 140px;
    }}
    .edge {{
      position: absolute;
      height: 2px;
      background: #333;
      transform-origin: 0 0;
    }}
    .arrow::after {{
      content: "";
      position: absolute;
      right: 0;
      top: -3px;
      border-top: 5px solid transparent;
      border-bottom: 5px solid transparent;
      border-left: 8px solid #333;
    }}
    #save {{
      position: absolute;
      bottom: 20px;
      right: 20px;
      padding: 10px 18px;
      background: #0066cc;
      color: white;
      border: none;
      border-radius: 6px;
      cursor: pointer;
    }}
  </style>
</head>
<body>
  <div id="diagram"></div>
  <button id="save">💾 Save Diagram as PNG</button>

  <script>
    const diagram = document.getElementById("diagram");

    function node(id, x, y, text, cls) {{
      const el = document.createElement("div");
      el.id = id;
      el.className = "node " + cls;
      el.textContent = text;
      el.style.left = x + "px";
      el.style.top = y + "px";
      diagram.appendChild(el);
    }}

    function edge(aId, bId) {{
      const A = document.getElementById(aId).getBoundingClientRect();
      const B = document.getElementById(bId).getBoundingClientRect();
      const line = document.createElement("div");
      line.className = "edge";
      const x1 = A.left + A.width / 2;
      const y1 = A.top + A.height;
      const x2 = B.left + B.width / 2;
      const y2 = B.top;
      const dx = x2 - x1;
      const dy = y2 - y1;
      const len = Math.sqrt(dx * dx + dy * dy);
      const ang = Math.atan2(dy, dx) * 180 / Math.PI;
      line.style.width = len + "px";
      line.style.left = x1 + "px";
      line.style.top = y1 + "px";
      line.style.transform = "rotate(" + ang + "deg)";
      diagram.appendChild(line);
    }}

    function redraw() {{
      document.querySelectorAll(".edge").forEach(e => e.remove());
      {edge_js}
    }}

    {node_js}
    redraw();

    const s = document.createElement("script");
    s.src = "https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js";
    s.onload = () => {{
      document.getElementById("save").onclick = () => {{
        html2canvas(document.body).then(c => {{
          const a = document.createElement("a");
          a.download = "bowtie_diagram.png";
          a.href = c.toDataURL("image/png");
          a.click();
        }});
      }};
    }};
    document.body.appendChild(s);
  </script>
</body>
</html>
"""
st.components.v1.html(html_code, height=850, scrolling=False)
