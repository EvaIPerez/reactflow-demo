import streamlit as st
st.set_page_config(page_title="Bowtie Risk Diagram", layout="wide")
st.title("🎯 Bowtie Risk Diagram Builder")

# --- Default core nodes ---
default_nodes = [
    ("haz1", 400, 80, "Hazard", "hazard"),
    ("top1", 400, 200, "Top Event", "topevent"),
]
default_edges = [("haz1", "top1")]

if "nodes" not in st.session_state:
    st.session_state.nodes = default_nodes.copy()
if "edges" not in st.session_state:
    st.session_state.edges = default_edges.copy()

# --- Sidebar Controls ---
st.sidebar.header("Add Nodes to Bowtie")
node_type = st.sidebar.selectbox(
    "Select Node Type:",
    [
        "Hazard",
        "Threat",
        "Preventive Barrier",
        "Mitigation Barrier",
        "Consequence",
    ],
)
label_input = st.sidebar.text_input("Label:", value=f"New {node_type}")
add_button = st.sidebar.button("➕ Add Node")

# --- Find references ---
hazard_id = [n[0] for n in st.session_state.nodes if n[4] == "hazard"][-1]
top_event_id = [n[0] for n in st.session_state.nodes if n[4] == "topevent"][-1]

# --- Add Logic ---
if add_button:
    nodes = st.session_state.nodes
    edges = st.session_state.edges
    new_id = f"n{len(nodes)+1}"
    label = label_input.strip() if label_input else node_type
    y_offset = 80 * len([n for n in nodes if n[4] == node_type.lower().replace(' ', '')])

    if node_type == "Hazard":
        x, y, cls = 400, 80 + y_offset, "hazard"
        nodes.append((new_id, x, y, label, cls))
        edges.append((new_id, top_event_id))

    elif node_type == "Threat":
        x, y, cls = 100, 120 + y_offset, "threat"
        nodes.append((new_id, x, y, label, cls))
        edges.append((new_id, top_event_id))

    elif node_type == "Preventive Barrier":
        x, y, cls = 250, 120 + y_offset, "barrier"
        nodes.append((new_id, x, y, label, cls))
        # link threat → barrier → top event
        threats = [n for n in nodes if n[4] == "threat"]
        if threats:
            edges.append((threats[-1][0], new_id))
        edges.append((new_id, top_event_id))

    elif node_type == "Mitigation Barrier":
        x, y, cls = 550, 120 + y_offset, "barrier"
        nodes.append((new_id, x, y, label, cls))
        edges.append((top_event_id, new_id))

    elif node_type == "Consequence":
        x, y, cls = 700, 120 + y_offset, "consequence"
        nodes.append((new_id, x, y, label, cls))
        edges.append((top_event_id, new_id))

    st.session_state.nodes = nodes
    st.session_state.edges = edges

# --- Reset ---
if st.button("🔄 Reset Diagram"):
    st.session_state.nodes = default_nodes.copy()
    st.session_state.edges = default_edges.copy()

# --- Legend ---
st.markdown("""
**Legend:**
- 🟨 **Hazard** – at the top (yellow + black border) 
- 🟩 **Top Event** – central event (green) 
- 🟧 **Threats** – potential initiating causes (left) 
- 🟦 **Barriers (Preventive & Mitigation)** – blue 
- 🟥 **Consequences** – possible outcomes (right)
""")

nodes = st.session_state.nodes
edges = st.session_state.edges

# --- JS generation ---
node_js = "\n".join(
    [f"node('{n[0]}', {n[1]}, {n[2]}, '{n[3]}', '{n[4]}');" for n in nodes]
)
edge_js = "\n".join([f"edge('{a}', '{b}');" for (a,b) in edges])

# --- HTML/JS rendering ---
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
        border-radius: 8px;
        font-weight: 500;
        color: #222;
        text-align: center;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
      }}
      .hazard {{
        background: repeating-linear-gradient(
          45deg,
          #fff200,
          #fff200 10px,
          #000 10px,
          #000 20px
        );
        border: 2px solid #000;
        color: #000;
      }}
      .topevent {{
        background: #28a745;
        border: 3px solid #155724;
        color: #fff;
        border-radius: 50%;
        width: 100px;
        height: 100px;
        line-height: 100px;
      }}
      .threat {{
        background: #fff3cd;
        border: 2px solid #ffcc00;
      }}
      .barrier {{
        background: #cce5ff;
        border: 2px solid #007bff;
      }}
      .consequence {{
        background: #f8d7da;
        border: 2px solid #dc3545;
      }}
      .edge {{
        position: absolute;
        height: 3px;
        background: #333;
        transform-origin: 0 0;
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
        el.draggable = true;
        el.ondragend = (e) => {{
          el.style.left = e.pageX - 40 + "px";
          el.style.top = e.pageY - 20 + "px";
          redraw();
        }};
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
st.components.v1.html(html_code, height=800, scrolling=False)


