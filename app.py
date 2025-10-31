import streamlit as st

st.set_page_config(page_title="React Flow Demo", layout="wide")
st.markdown("### 🧠 React Flow Diagram Example")

# Simplified pure JS version (no external blocked modules)
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
        background-color: #f5f5f5;
      }
      .node {
        position: absolute;
        padding: 8px 16px;
        background: white;
        border: 1px solid #999;
        border-radius: 5px;
        text-align: center;
        box-shadow: 2px 2px 4px rgba(0,0,0,0.2);
      }
      .edge {
        position: absolute;
        height: 2px;
        background: #222;
      }
    </style>
  </head>
  <body>
    <div id="diagram"></div>
    <script>
      const diagram = document.getElementById('diagram');

      function createNode(id, x, y, label) {
        const n = document.createElement('div');
        n.className = 'node';
        n.id = id;
        n.style.left = x + 'px';
        n.style.top = y + 'px';
        n.textContent = label;
        diagram.appendChild(n);
        return n;
      }

      function connect(n1, n2) {
        const r1 = n1.getBoundingClientRect();
        const r2 = n2.getBoundingClientRect();
        const line = document.createElement('div');
        line.className = 'edge';
        const x1 = r1.left + r1.width;
        const y1 = r1.top + r1.height/2;
        const x2 = r2.left;
        const y2 = r2.top + r2.height/2;
        const length = Math.sqrt((x2-x1)**2 + (y2-y1)**2);
        line.style.width = length + 'px';
        line.style.left = x1 + 'px';
        line.style.top = y1 + 'px';
        line.style.transformOrigin = '0 0';
        const angle = Math.atan2(y2-y1, x2-x1) * 180 / Math.PI;
        line.style.transform = 'rotate(' + angle + 'deg)';
        diagram.appendChild(line);
      }

      const n1 = createNode('n1', 50, 120, 'Start');
      const n2 = createNode('n2', 250, 120, 'Process');
      const n3 = createNode('n3', 450, 120, 'End');

      connect(n1, n2);
      connect(n2, n3);
    </script>
  </body>
</html>
"""

st.components.v1.html(html_code, height=400, scrolling=False)

 
