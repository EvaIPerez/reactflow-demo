import streamlit as st

st.set_page_config(page_title="React Flow Interactive", layout="wide")
st.markdown("### 🧠 Interactive React Flow Diagram (Offline Build)")

html_code = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <style>
      html, body {
        margin: 0;
        height: 100%;
        overflow: hidden;
        background-color: #f7f9fc;
        font-family: Arial, sans-serif;
      }
      .node {
        position: absolute;
        padding: 10px 20px;
        border-radius: 8px;
        color: #222;
        font-weight: 500;
        box-shadow: 2px 2px 4px rgba(0,0,0,0.2);
      }
      .hazard { background: #ffcccc; border: 2px solid #cc0000; }
      .threat { background: #fff3cd; border: 2px solid #ffcc00; }
      .barrier { background: #e6ffe6; border: 2px solid #009900; }
      .consequence { background: #e0ecff; border: 2px solid #0066cc; }
      .edge {
        position: absolute;
        height: 3px;
        background: #444;
        transform-origin: 0 0;
      }
    </style>
  </head>
  <body>
    <div id="diagram"></div>

    <script>
      const diagram = document.getElementById("diagram");

      function node(id, x, y, text, cls) {
        const el = document.createElement("div");
        el.id = id;
        el.className = "node " + cls;
        el.textContent = text;
        el.style.left = x + "px";
        el.style.top = y + "px";
        el.draggable = true;
        el.ondragstart = (e) => {
          e.dataTransfer.setData("text/plain", id);
        };
        el.ondragend = (e) => {
          el.style.left = e.pageX - 40 + "px";
          el.style.top = e.pageY - 20 + "px";
          redraw();
        };
        diagram.appendChild(el);
        return el;
      }

      function edge(id1, id2) {
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
      }

      function redraw() {
        document.querySelectorAll(".edge").forEach(e => e.remove());
        edge("t1", "b1");
        edge("b1", "h");
        edge("h", "b2");
        edge("b2", "c1");
      }

      // Create nodes
      node("t1", 80, 200, "Threat A", "threat");
      node("b1", 220, 200, "Barrier A", "barrier");
      node("h", 360, 200, "Hazard", "hazard");
      node("b2", 520, 200, "Barrier B", "barrier");
      node("c1", 660, 200, "Consequence", "consequence");

      redraw();
    </script>
  </body>
</html>
"""

st.components.v1.html(html_code, height=500, scrolling=False)
