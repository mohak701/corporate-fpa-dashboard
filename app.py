import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Corporate FP&A Dashboard", page_icon="📈", layout="wide")

st.title("📈 Corporate FP&A: Budget vs. Actual (BvA) & EBITDA Bridge")
st.markdown("Interactive management reporting dashboard for variance analysis, EBITDA bridge tracking, and FY27 P&L scenario modeling.")

# Realistic Multi-Region Quarterly P&L Dataset (in $ Millions)
data = [
    {"Quarter": "Q1 FY26", "Region": "India", "Budget_Rev": 42.0, "Actual_Rev": 45.5, "Budget_COGS": 24.0, "Actual_COGS": 25.2, "Budget_OpEx": 10.0, "Actual_OpEx": 10.4},
    {"Quarter": "Q2 FY26", "Region": "India", "Budget_Rev": 44.0, "Actual_Rev": 47.0, "Budget_COGS": 25.0, "Actual_COGS": 26.5, "Budget_OpEx": 10.5, "Actual_OpEx": 10.2},
    {"Quarter": "Q3 FY26", "Region": "India", "Budget_Rev": 48.0, "Actual_Rev": 51.2, "Budget_COGS": 27.0, "Actual_COGS": 28.0, "Budget_OpEx": 11.0, "Actual_OpEx": 11.5},
    {"Quarter": "Q4 FY26", "Region": "India", "Budget_Rev": 52.0, "Actual_Rev": 54.8, "Budget_COGS": 29.0, "Actual_COGS": 30.1, "Budget_OpEx": 11.5, "Actual_OpEx": 11.8},
    {"Quarter": "Q1 FY26", "Region": "Europe", "Budget_Rev": 60.0, "Actual_Rev": 57.5, "Budget_COGS": 35.0, "Actual_COGS": 34.8, "Budget_OpEx": 15.0, "Actual_OpEx": 15.6},
    {"Quarter": "Q2 FY26", "Region": "Europe", "Budget_Rev": 62.0, "Actual_Rev": 60.2, "Budget_COGS": 36.0, "Actual_COGS": 35.9, "Budget_OpEx": 15.2, "Actual_OpEx": 15.4},
    {"Quarter": "Q3 FY26", "Region": "Europe", "Budget_Rev": 65.0, "Actual_Rev": 66.8, "Budget_COGS": 37.5, "Actual_COGS": 38.0, "Budget_OpEx": 15.5, "Actual_OpEx": 15.2},
    {"Quarter": "Q4 FY26", "Region": "Europe", "Budget_Rev": 68.0, "Actual_Rev": 70.5, "Budget_COGS": 39.0, "Actual_COGS": 39.8, "Budget_OpEx": 16.0, "Actual_OpEx": 15.9},
    {"Quarter": "Q1 FY26", "Region": "North America", "Budget_Rev": 85.0, "Actual_Rev": 88.0, "Budget_COGS": 48.0, "Actual_COGS": 49.0, "Budget_OpEx": 22.0, "Actual_OpEx": 21.8},
    {"Quarter": "Q2 FY26", "Region": "North America", "Budget_Rev": 88.0, "Actual_Rev": 91.5, "Budget_COGS": 49.5, "Actual_COGS": 50.8, "Budget_OpEx": 22.5, "Actual_OpEx": 22.9},
    {"Quarter": "Q3 FY26", "Region": "North America", "Budget_Rev": 92.0, "Actual_Rev": 90.0, "Budget_COGS": 51.5, "Actual_COGS": 52.0, "Budget_OpEx": 23.0, "Actual_OpEx": 23.5},
    {"Quarter": "Q4 FY26", "Region": "North America", "Budget_Rev": 98.0, "Actual_Rev": 102.4, "Budget_COGS": 54.0, "Actual_COGS": 55.2, "Budget_OpEx": 24.0, "Actual_OpEx": 23.8},
]

df = pd.DataFrame(data)
df["Budget_EBITDA"] = df["Budget_Rev"] - df["Budget_COGS"] - df["Budget_OpEx"]
df["Actual_EBITDA"] = df["Actual_Rev"] - df["Actual_COGS"] - df["Actual_OpEx"]

# Sidebar Filters & Scenario Simulator
st.sidebar.header("🔍 Filters")
regions = st.sidebar.multiselect("Select Region(s)", options=df["Region"].unique(), default=df["Region"].unique())
filtered_df = df[df["Region"].isin(regions)]

st.sidebar.markdown("---")
st.sidebar.header("🎛️ FY27 Scenario Simulator")
rev_growth = st.sidebar.slider("Projected Revenue Growth (%)", -10.0, 30.0, 12.0, 1.0)
cogs_opt = st.sidebar.slider("COGS Efficiency / Reduction (%)", -5.0, 10.0, 2.0, 0.5)
opex_change = st.sidebar.slider("OpEx Inflation (%)", -5.0, 15.0, 5.0, 0.5)

# Summary Totals
tot_bud_rev = filtered_df["Budget_Rev"].sum()
tot_act_rev = filtered_df["Actual_Rev"].sum()
tot_bud_cogs = filtered_df["Budget_COGS"].sum()
tot_act_cogs = filtered_df["Actual_COGS"].sum()
tot_bud_opex = filtered_df["Budget_OpEx"].sum()
tot_act_opex = filtered_df["Actual_OpEx"].sum()
tot_bud_ebitda = filtered_df["Budget_EBITDA"].sum()
tot_act_ebitda = filtered_df["Actual_EBITDA"].sum()

rev_var = tot_act_rev - tot_bud_rev
cogs_var = tot_bud_cogs - tot_act_cogs  # Positive = cost savings
opex_var = tot_bud_opex - tot_act_opex  # Positive = cost savings
ebitda_var = tot_act_ebitda - tot_bud_ebitda

# KPI Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Actual Revenue ($M)", f"${tot_act_rev:.1f}M", f"{rev_var:+.1f}M ({(rev_var/tot_bud_rev)*100:+.1f}%)")
col2.metric("Actual EBITDA ($M)", f"${tot_act_ebitda:.1f}M", f"{ebitda_var:+.1f}M ({(ebitda_var/tot_bud_ebitda)*100:+.1f}%)")
act_margin = (tot_act_ebitda / tot_act_rev) * 100
bud_margin = (tot_bud_ebitda / tot_bud_rev) * 100
col3.metric("EBITDA Margin (%)", f"{act_margin:.1f}%", f"{act_margin - bud_margin:+.1f}% vs Budget")

# FY27 Projected EBITDA
proj_rev = tot_act_rev * (1 + rev_growth / 100)
proj_cogs = tot_act_cogs * (1 + rev_growth / 100) * (1 - cogs_opt / 100)
proj_opex = tot_act_opex * (1 + opex_change / 100)
proj_ebitda = proj_rev - proj_cogs - proj_opex
col4.metric("FY27 Projected EBITDA", f"${proj_ebitda:.1f}M", f"{proj_ebitda - tot_act_ebitda:+.1f}M vs FY26")

st.markdown("---")

# Charts Row
c1, c2 = st.columns(2)

with c1:
    st.subheader("EBITDA Variance Bridge ($M)")
    fig_wf = go.Figure(go.Waterfall(
        orientation="v",
        measure=["absolute", "relative", "relative", "relative", "total"],
        x=["Budget EBITDA", "Revenue Var", "COGS Var", "OpEx Var", "Actual EBITDA"],
        y=[tot_bud_ebitda, rev_var, cogs_var, opex_var, tot_act_ebitda],
        text=[f"${tot_bud_ebitda:.1f}M", f"{rev_var:+.1f}M", f"{cogs_var:+.1f}M", f"{opex_var:+.1f}M", f"${tot_act_ebitda:.1f}M"],
        textposition="outside",
        increasing={"marker": {"color": "#2ecc71"}},
        decreasing={"marker": {"color": "#e74c3c"}},
        totals={"marker": {"color": "#3498db"}}
    ))
    fig_wf.update_layout(height=400, margin=dict(t=20, b=20))
    st.plotly_chart(fig_wf, use_container_width=True)

with c2:
    st.subheader("Quarterly EBITDA: Budget vs. Actual ($M)")
    q_df = filtered_df.groupby("Quarter", as_index=False)[["Budget_EBITDA", "Actual_EBITDA"]].sum()
    fig_bar = px.bar(q_df, x="Quarter", y=["Budget_EBITDA", "Actual_EBITDA"], barmode="group",
                     color_discrete_map={"Budget_EBITDA": "#95a5a6", "Actual_EBITDA": "#3498db"})
    fig_bar.update_layout(height=400, margin=dict(t=20, b=20), yaxis_title="EBITDA ($M)", legend_title="")
    st.plotly_chart(fig_bar, use_container_width=True)

# Detailed Variance Table
st.subheader("Regional P&L Variance Summary ($M)")
reg_df = filtered_df.groupby("Region", as_index=False)[["Budget_Rev", "Actual_Rev", "Budget_EBITDA", "Actual_EBITDA"]].sum()
reg_df["Rev_Var ($M)"] = reg_df["Actual_Rev"] - reg_df["Budget_Rev"]
reg_df["EBITDA_Var ($M)"] = reg_df["Actual_EBITDA"] - reg_df["Budget_EBITDA"]
st.dataframe(reg_df.style.format({col: "{:.1f}" for col in reg_df.columns if col != "Region"}), use_container_width=True)
