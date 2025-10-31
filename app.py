import streamlit as st
st.set_page_config(page_title="Bowtie Risk Diagram", layout="wide")
st.title("🎯 Bowtie Risk Diagram – React Flow Auto Layout (Stable Version)")

# --- Sidebar Controls ---
st.sidebar.header("Add / Edit Elements")
node_type = st.sidebar.selectbox(
    "Select Node Type:",
    ["Hazard", "Top Event", "Threat", "Preventive Barrier", "Mitigation Barrier", "Consequence"],
)
label_input = st.sidebar.text_input("Label:", value=f"New {node_type}")
add_button = st.sidebar.button("➕ Add Node")

# --- Initialize default nodes and edges ---
default_nodes = [
    {"id": "haz1", "type": "hazard", "data": {"label": "Hazard"}, "position": {"x": 0, "y": 0}},
    {"id": "top1", "type": "topevent", "data": {"label": "Top Event"}, "position": {"x": 0, "y": 200}},
]
default_edges = [{"id": "e1", "source": "haz1", "target": "top1"}]

if "nodes" not in st.session_state:
    st.session_state.nodes = default_nodes
if "edges" not in st.session_state:
    st.session_state.edges = default_edges

# --- Add Node Logic ---
if add_button:
    new_id = f"n{len(st.session_state.nodes)+1}"
    label = label_input.strip() or node_type
    node = {"id": new_id, "type": node_type.lower().replace(" ", ""), "data": {"label": label}, "position": {"x": 0, "y": 0}}
    st.session_state.nodes.append(node)

    if node_type == "Hazard":
        st.session_state.edges = [e for e in st.session_state.edges if e["source"] != "haz1"]
        st.session_state.edges.append({"id": f"e{len(st.session_state.edges)+1}", "source": "haz1", "target": "top1"})
    elif node_type in ["Threat", "Preventive Barrier"]:
        st.session_state.edges.append({"id": f"e{len(st.session_state.edges)+1}", "source": new_id, "target": "top1"})
    elif node_type in ["Mitigation Barrier", "Consequence"]:
        st.session_state.edges.append({"id": f"e{len(st.session_state.edges)+1}", "source": "top1", "target": new_id})

# --- Convert Python → JS ---
nodes_js = str(st.session_state.nodes).replace("'", '"')
edges_js = str(st.session_state.edges).replace("'", '"')


# --- React Flow HTML (UMD, Streamlit-safe) ---
html_code = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <title>Bowtie Diagram</title>
    <link rel="stylesheet" href="https://unpkg.com/reactflow@11.10.2/dist/style.css" />
    <style>
      html, body, #root {
        width: 100%;
        height: 100%;
        margin: 0;
        background: #f8fafc;
      }
      .react-flow__node-hazard {
        border: 2px solid black;
        background: white;
        background-image: repeating-linear-gradient(
          45deg, #fff200, #fff200 10px, #000 10px, #000 20px
        );
        background-size: 100px 20px;
        color: #000;
        text-align: center;
        font-weight: bold;
      }
      .react-flow__node-topevent {
        background: #28a745;
        border: 3px solid #155724;
        color: white;
        text-align: center;
        font-weight: bold;
      }
      .react-flow__node-threat {
        background: #fff3cd;
        border: 2px solid #ffcc00;
        text-align: center;
      }
      .react-flow__node-preventivebarrier,
      .react-flow__node-mitigationbarrier {
        background: #cce5ff;
        border: 2px solid #007bff;
        text-align: center;
      }
      .react-flow__node-consequence {
        background: #f8d7da;
        border: 2px solid #dc3545;
        text-align: center;
      }
    </style>
  </head>
  <body>
    <div id="root"></div>

    <!-- React Flow + Dagre libraries -->
    <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://unpkg.com/dagre@0.8.5/dist/dagre.min.js"></script>
    <script src="https://unpkg.com/reactflow@11.10.2/dist/reactflow.min.js"></script>

    <script>
      window.onload = function() {
        const nodes = NODE_DATA;
        const edges = EDGE_DATA;
        const nodeWidth = 180;
        const nodeHeight = 60;

        const dagreGraph = new dagre.graphlib.Graph();
        dagreGraph.setDefaultEdgeLabel(() => ({}));
        dagreGraph.setGraph({ rankdir: "TB", nodesep: 100, ranksep: 120 });

        nodes.forEach(node => dagreGraph.setNode(node.id, { width: nodeWidth, height: nodeHeight }));
        edges.forEach(edge => dagreGraph.setEdge(edge.source, edge.target));
        dagre.layout(dagreGraph);

        const layoutedNodes = nodes.map(node => {
          const pos = dagreGraph.node(node.id);
          node.position = { x: pos.x - nodeWidth / 2, y: pos.y - nodeHeight / 2 };
          return node;
        });

        const layoutedEdges = edges.map(e => ({
          ...e,
          markerEnd: { type: "arrowclosed", color: "#333" },
          style: { stroke: "#333", strokeWidth: 2 }
        }));

        const { ReactFlow, Background, Controls, MiniMap } = window.ReactFlow;

        function App() {
          return React.createElement(
            ReactFlow,
            {
              nodes: layoutedNodes,
              edges: layoutedEdges,
              fitView: true,
              proOptions: { hideAttribution: true }
            },
            React.createElement(Background, { variant: "dots" }),
            React.createElement(Controls, null),
            React.createElement(MiniMap, null)
          );
        }

        const root = ReactDOM.createRoot(document.getElementById("root"));
        root.render(React.createElement(App));
      };
    </script>
  </body>
</html>
"""

# --- Safely inject your Streamlit data ---
html_code = html_code.replace("NODE_DATA", str(st.session_state.nodes).replace("'", '"'))
html_code = html_code.replace("EDGE_DATA", str(st.session_state.edges).replace("'", '"'))

# --- Render in sandboxed iframe ---
st.components.v1.html(
    '<iframe srcdoc="' + html_code + '" width="100%" height="850" style="border:none;"></iframe>',
    height=850,
    scrolling=False,
)
 
 
