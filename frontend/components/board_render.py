import streamlit as st
import streamlit.components.v1 as components
import json
import math

# ----------------------------
# helpers
# ----------------------------
SCALE = 80
OFFSET_X = 300
OFFSET_Y = 260


def to_screen(x, y):
    return OFFSET_X + x * SCALE, OFFSET_Y + y * SCALE


def node_id(pos):
    return f"{pos[0]},{pos[1]}"


def edge_id(a, b):
    return "|".join(sorted([node_id(a), node_id(b)]))


# ----------------------------
# main render
# ----------------------------
def render_board_svg(tiles, edges, nodes):
    # simulăm validări (în realitate vin din backend)
    valid_node_ids = {node_id(n["position"]) for n in nodes}
    valid_edge_ids = {edge_id(e["a"], e["b"]) for e in edges}

    # ----------------------------
    # SVG: tiles (hexes)
    # ----------------------------
    hex_svg = ""
    for t in tiles:
        # axial -> pixel (same logic ca backend)
        x = math.sqrt(3) * (t["q"] + t["r"] / 2)
        y = 1.5 * t["r"]
        cx, cy = to_screen(x, y)

        hex_svg += f"""
        <circle cx="{cx}" cy="{cy}" r="35"
                fill="#1e293b" stroke="#334155" stroke-width="2"/>
        """

        if t["number"] is not None:
            hex_svg += f"""
            <text x="{cx}" y="{cy+6}" text-anchor="middle"
                  fill="white" font-size="14">{t["number"]}</text>
            """

    # ----------------------------
    # SVG: edges
    # ----------------------------
    edges_svg = ""
    for e in edges:
        a = e["a"]
        b = e["b"]
        eid = edge_id(a, b)

        x1, y1 = to_screen(a[0], a[1])
        x2, y2 = to_screen(b[0], b[1])

        is_valid = eid in valid_edge_ids

        edges_svg += f"""
        <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"
              stroke="{ '#22c55e' if is_valid else '#475569' }"
              stroke-width="6"
              stroke-linecap="round"
              opacity="0.85"
              onclick="selectEdge('{eid}')"/>
        """

    # ----------------------------
    # SVG: nodes
    # ----------------------------
    nodes_svg = ""
    for n in nodes:
        x, y = n["position"]
        nid = node_id(n["position"])
        sx, sy = to_screen(x, y)

        is_valid = nid in valid_node_ids

        nodes_svg += f"""
        <circle cx="{sx}" cy="{sy}" r="7"
                fill="{ '#22c55e' if is_valid else '#64748b' }"
                stroke="#020617"
                stroke-width="2"
                onclick="selectNode('{nid}')"/>
        """

    # ----------------------------
    # full SVG
    # ----------------------------
    components.html(
        f"""
        <div style="background:#020617;">
        <svg width="600" height="520">
            {hex_svg}
            {edges_svg}
            {nodes_svg}
        </svg>

        <script>
        function selectNode(id) {{
            window.parent.postMessage(
                {{ type: "NODE", id: id }},
                "*"
            );
        }}

        function selectEdge(id) {{
            window.parent.postMessage(
                {{ type: "EDGE", id: id }},
                "*"
            );
        }}
        </script>
        </div>
        """,
        height=540,
    )
