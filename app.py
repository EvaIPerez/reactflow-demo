import streamlit as st
st.set_page_config(page_title="Bowtie Risk Diagram", layout="wide")
st.title("🎯 Bowtie Risk Diagram Builder – Auto Aligned")

# --- Default structure ---
default_nodes = [
    ("haz1", 400, 80, "Hazard", "hazard"),
    ("top1", 400, 220, "Top Event", "topevent"),
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
        "Top Event",
        "Threat",
        "Preventive Barrier",
        "Mitigation Barrier",
        "Consequence",
    ],
)
label_input = st.sidebar.text_input("Label:", value=f"New {node_type}")
add_button = st.sidebar.button("➕ Add Node")

# --- Helpers ---
def get_nodes_of_type(cls):
    return [n for n in st.session_state.nodes if n[4] == cls]

def add_edge(a, b):
    st.session_state.edges.append((a, b))

# --- Find hazard and top event ---
hazards = get_nodes_of_type("hazard")
hazard_id = hazards[0][0] if hazards else None
top_event_nodes = get_nodes_of_type("topevent")
top_event_id = top_event_nodes[0][0] if top_event_nodes else None

# --- Auto add logic ---
if add_button:
    nodes = st.session_state.nodes
    edges = st.session_state.edges
    new_id = f"n{len(nodes)+1}"
    label = label_input.strip() if label_input else node_type

    # define baseline x positions
    x_hazard, x_top = 400, 400
    x_threat, x_barrier_L = 120, 250
    x_barrier_R, x_conseq = 550, 700
    y_spacing = 70

    if node_type == "Hazard":
        y = 80
        nodes.append((new_id, x_hazard, y, label, "hazard"))
        if top_event_id:
            add_edge(new_id, top_event_id)

    elif node_type == "Top Event":
        y = 220
        nodes.append((new_id, x_top, y, label, "topevent"))
        if hazard_id:
            add_edge(hazard_id, new_id)

    elif node_type == "Threat":
        threats = get_nodes_of_type("threat")
        y = 160 + len(threats) * y_spacing
        nodes.append((new_id, x_threat, y, label, "threat"))
        if top_event_id:
            add_edge(new_id, top_event_id)

    elif node_type == "Preventive Barrier":
        barriers = get_nodes_of_type("barrier_L")
        y = 160 + len(barriers) * y_spacing
        nodes.append((new_id, x_barrier_L, y, label, "barrier_L"))
        threats = get_nodes_of_type("threat")
        if threats:
            add_edge(threats[-1][0], new_id)
        if top_event_id:
            add_edge(new_id, top_event_id)

    elif node_type == "Mitigation Barrier":
        barriersR = get_nodes_of_type("barrier_R")
        y = 160 + len(barriersR) * y_spacing
        nodes.append((new_id, x_barrier_R, y, label, "barrier_R"))
        if top_event_id:
            add_edge(top_event_id, new_id)

    elif node_type == "Consequence":
        consequences = get_nodes_of_type("consequence")
        y = 160 + len(consequences) * y_spacing
        nodes.append((new_id, x_conseq, y, label, "consequence"))
        if top_event_id:
            add_edge(top_event_id, new_id)

    st.session_state.nodes = nodes
    st.session_state.edges = edges

# --- Reset ---
if st.button("🔄 Reset Diagram"):
    st.session_state.nodes = default_nodes.copy()
    st.session_state.edges = default_edges.copy()

# --- Legend ---
st.markdown("""
**Legend**
- 🟨 **Hazard** – top (yellow & black header)
- 🟩 **Top Event** – central green square
- 🟧 **Threats** – left side, evenly spaced
- 🟦 **Barriers** – blue, same color for preventive & mitigation
- 🟥 **Consequences** – right side, evenly spaced
""")

nodes = st.session_state.nodes
edges = st.session_state.edges

# --- JS data ---
node_js = "\n".join(
    [f"node('{n[0]}', {n[1]}, {n[2]}, '{n[3]}', '{n[4]}');" for n in nodes]
)
edge_js = "\n".join([f"edge('{a}', '{b}');" for (a,b) in edges])

# --- HTML & JS rendering ---
html_code = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <style>
    html,body {{
      margin:0; height:100%; overflow:hidden;
      background:#f8fafc; font-family:Arial,sans-serif;
    }}
    .node {{
      position:absolute;
      padding:10px 20px;
      border-radius:6px;
      font-weight:500;
      color:#222;
      text-align:center;
      box-shadow:2px 2px 5px rgba(0,0,0,0.2);
    }}
    .hazard {{
      background:white;
      border:2px solid black;
      position:relative;
    }}
    .hazard::before {{
      content:"";
      position:absolute;
      top:0; left:0; right:0; height:15px;
      background:repeating-linear-gradient(
        45deg,
        #fff200,
        #fff200 10px,
        #000 10px,
        #000 20px
      );
      border-bottom:1px solid #000;
      border-top-left-radius:6px;
      border-top-right-radius:6px;
    }}
    .topevent {{
      background:#28a745;
      border:3px solid #155724;
      color:#fff;
      width:120px; height:60px;
      line-height:60px;
    }}
    .threat {{
      background:#fff3cd;
      border:2px solid #ffcc00;
    }}
    .barrier_L, .barrier_R {{
      background:#cce5ff;
      border:2px solid #007bff;
    }}
    .consequence {{
      background:#f8d7da;
      border:2px solid #dc3545;
    }}
    .edge {{
      position:absolute;
      height:2px;
      background:#333;
      transform-origin:0 0;
    }}
    #save {{
      position:absolute;
      bottom:20px;
      right:20px;
      padding:10px 18px;
      background:#0066cc;
      color:white;
      border:none;
      border-radius:6px;
      cursor:pointer;
    }}
  </style>
</head>
<body>
  <div id="diagram"></div>
  <button id="save">💾 Save Diagram as PNG</button>

  <script>
    const diagram=document.getElementById("diagram");

    function node(id,x,y,text,cls){{
      const el=document.createElement("div");
      el.id=id;
      el.className="node "+cls;
      el.textContent=text;
      el.style.left=x+"px";
      el.style.top=y+"px";
      el.draggable=true;
      el.ondragend=(e)=>{{
        el.style.left=e.pageX-40+"px";
        el.style.top=e.pageY-20+"px";
        redraw();
      }};
      diagram.appendChild(el);
    }}

    function edge(aId,bId){{
      const A=document.getElementById(aId).getBoundingClientRect();
      const B=document.getElementById(bId).getBoundingClientRect();
      const line=document.createElement("div");
      line.className="edge";
      const x1=A.left+A.width/2;
      const y1=A.top+A.height;
      const x2=B.left+B.width/2;
      const y2=B.top;
      const dx=x2-x1;
      const dy=y2-y1;
      const len=Math.sqrt(dx*dx+dy*dy);
      const ang=Math.atan2(dy,dx)*180/Math.PI;
      line.style.width=len+"px";
      line.style.left=x1+"px";
      line.style.top=y1+"px";
      line.style.transform="rotate("+ang+"deg)";
      diagram.appendChild(line);
    }}

    function redraw(){{
      document.querySelectorAll(".edge").forEach(e=>e.remove());
      {edge_js}
    }}

    {node_js}
    redraw();

    const s=document.createElement("script");
    s.src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js";
    s.onload=()=>{{
      document.getElementById("save").onclick=()=>{{
        html2canvas(document.body).then(c=>{{
          const a=document.createElement("a");
          a.download="bowtie_diagram.png";
          a.href=c.toDataURL("image/png");
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
