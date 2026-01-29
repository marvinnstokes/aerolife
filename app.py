import streamlit as st
import plotly.express as px
import pandas as pd
import streamlit.components.v1 as components

# ---------------- app config ----------------
st.set_page_config(page_title="AeroLife", layout="centered")

st.title("AeroLife")
st.caption("life support mass estimates for human space missions")

# ---------------- inputs ----------------
crew = st.slider("crew size", 1, 10, 3)
days = st.slider("mission duration (days)", 1, 1000, 180)

mission_type = st.selectbox(
    "mission type",
    ["short (leo)", "medium (lunar)", "long (deep space / mars)"]
)

recycling = st.selectbox(
    "recycling level",
    ["none", "partial", "high"]
)

# ---------------- constants ----------------
FOOD = 0.62     # kg/person/day
WATER = 3.5
OXYGEN = 0.84

recycling_map = {
    "none": {"water": 0.0, "oxygen": 0.0},
    "partial": {"water": 0.5, "oxygen": 0.3},
    "high": {"water": 0.85, "oxygen": 0.75},
}

eff = recycling_map[recycling]

# ---------------- math ----------------
food_mass = crew * days * FOOD
water_mass = crew * days * WATER * (1 - eff["water"])
oxygen_mass = crew * days * OXYGEN * (1 - eff["oxygen"])

total = food_mass + water_mass + oxygen_mass
margin = total * 0.2
total_with_margin = total + margin

# ---------------- results ----------------
st.subheader("mass breakdown (kg)")

data = pd.DataFrame({
    "category": ["food", "water", "oxygen", "margin"],
    "mass (kg)": [food_mass, water_mass, oxygen_mass, margin]
})

fig = px.bar(
    data,
    x="category",
    y="mass (kg)",
    text_auto=".2s"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown(f"""
**total life support mass:** `{total_with_margin:,.0f} kg`

- food: `{food_mass:,.0f} kg`  
- water: `{water_mass:,.0f} kg`  
- oxygen: `{oxygen_mass:,.0f} kg`  
- safety margin (20%): `{margin:,.0f} kg`
""")

st.caption("free. early-phase. transparent assumptions.")

st.divider()

# ---------------- assumptions ----------------
st.subheader("notes & assumptions")
st.markdown("""
- early-phase estimates (not flight-certified)
- food is not recyclable
- water & oxygen recycling are approximate
- system hardware mass not included
""")

st.divider()

# ---------------- ko-fi ----------------
st.markdown("""
**this tool is free.**  
optional donations fund more aerospace projects.
""")

components.html(
    """
    <script type='text/javascript' src='https://storage.ko-fi.com/cdn/widget/Widget_2.js'></script>
    <script type='text/javascript'>
      kofiwidget2.init('Ko-fi', '#000000', 'Q5Q21T7WKR');
      kofiwidget2.draw();
    </script>
    """,
    height=100
)
