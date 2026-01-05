import streamlit.components.v1 as components

RESOURCE_ICONS = {
    "sheep": "🐑",
    "wheat": "🌾",
    "clay": "🧱",
    "forest": "🌲",
}


def render_players_rows(players, current_player):
    html = ""

    for p in players:
        name = p.get("name")
        vp = p.get("victory_points", 0)
        resources = p.get("resources", {}) or {}
        resource_count = sum(resources.values())
        longest_road = p.get("longest_road", 0)
        last_roll = p.get("last_dice_roll")

        is_current = name == current_player
        is_human = name.lower() == "human"

        bg = "#1f2937" if is_current else "#020617"
        border = "#22c55e" if is_current else "#334155"
        title = "#22c55e" if is_current else "#e5e7eb"

        # ----------------------------
        # 🎒 RESOURCES
        # ----------------------------
        if is_human:
            resources_html = (
                "<div style='margin-top:6px; font-size:18px; color:#ffffff;'>"
            )
            for res in ["sheep", "wheat", "clay", "forest"]:
                value = resources.get(res, 0)
                icon = RESOURCE_ICONS[res]
                resources_html += f"""
                <span style="margin-right:14px;">
                    {icon} <b>{value}</b>
                </span>
                """
            resources_html += "</div>"
        else:
            resources_html = f"""
            <div style="margin-top:6px; color:#93c5fd;">
                🎒 Resources: <b>{resource_count}</b>
            </div>
            """

        # ----------------------------
        # 🎲 LAST ROLL (same height)
        # ----------------------------
        roll_html = ""
        if last_roll is not None:
            roll_html = f"""
            <div style="
                width:110px;
                height:100%;
                background:#ffffff;
                border:2px solid #64748b;
                border-radius:12px;
                display:flex;
                flex-direction:column;
                justify-content:center;
                align-items:center;
                margin-left:12px;
                padding:12px;
                box-sizing:border-box;
            ">
                <div style="font-size:32px; font-weight:bold;">
                    {last_roll}
                </div>
                <div style="font-size:12px; color:#64748b;">
                    Last Roll
                </div>
            </div>
            """

        # ----------------------------
        # 🧱 ROW
        # ----------------------------
        html += f"""
        <div style="
            display:flex;
            align-items:stretch;
            margin-bottom:14px;
            font-family: Arial, sans-serif;
        ">
            <div style="
                flex:1;
                background:{bg};
                border:2px solid {border};
                border-radius:14px;
                padding:12px;
                box-sizing:border-box;
            ">
                <div style="font-size:18px; font-weight:bold; color:{title};">
                    {name} {"🟢" if is_current else ""}
                </div>

                <div style="
                    margin-top:4px;
                    display:flex;
                    justify-content:space-between;
                    color:#facc15;
                ">
                    <div>🏆 VP: <b>{vp}</b></div>
                    <div>🛣️ LR: <b>{longest_road}</b></div>
                </div>

                {resources_html}
            </div>

            {roll_html}
        </div>
        """

    components.html(html, height=150 + len(players) * 120)
