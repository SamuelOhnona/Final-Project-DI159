import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from app.database import get_simulated_ads, get_prompts

st.set_page_config(page_title="Lead Generator Ads", page_icon="📈", layout="wide")
st.title("Lead Generator Ads — Dashboard")
st.caption("Client-friendly view: filter campaigns, inspect performance, and explore KPIs.")

df = get_simulated_ads()
if df.empty:
    st.warning("No simulated data found. Please run `python simulate_data.py` first.")
    st.stop()

# Filters
col1, col2, col3 = st.columns(3)
categories = sorted(df["category"].unique())
platforms = sorted(df["platform"].unique())
with col1:
    category = st.selectbox("Category", options=["All"] + categories, index=0)
with col2:
    platform = st.selectbox("Platform", options=["All"] + platforms, index=0)
with col3:
    campaigns = sorted(df["campaign_name"].unique())
    campaign = st.selectbox("Campaign", options=["All"] + campaigns, index=0)

data = df.copy()
if category != "All":
    data = data[data["category"] == category]
if platform != "All":
    data = data[data["platform"] == platform]
if campaign != "All":
    data = data[data["campaign_name"] == campaign]

st.subheader("Monthly KPIs")
# Leads over time
fig1, ax1 = plt.subplots()
(data.groupby("month")[["leads"]].sum()
     .plot(ax=ax1, marker="o"))
ax1.set_title("Leads per Month")
ax1.set_xlabel("Month")
ax1.set_ylabel("Leads")
st.pyplot(fig1)

# CPC over time
fig2, ax2 = plt.subplots()
(data.groupby("month")[["cpc"]].mean()
     .plot(ax=ax2, marker="o"))
ax2.set_title("Average CPC per Month")
ax2.set_xlabel("Month")
ax2.set_ylabel("CPC ($)")
st.pyplot(fig2)

# CPL over time
fig3, ax3 = plt.subplots()
(data.groupby("month")[["cpl"]].mean()
     .plot(ax=ax3, marker="o"))
ax3.set_title("Average CPL per Month")
ax3.set_xlabel("Month")
ax3.set_ylabel("CPL ($)")
st.pyplot(fig3)

st.subheader("Raw Data (filtered)")
st.dataframe(data, use_container_width=True, hide_index=True)

st.subheader("Prompts History")
prompts = get_prompts()
if not prompts.empty:
    st.dataframe(prompts.sort_values("timestamp", ascending=False), use_container_width=True, hide_index=True)
else:
    st.info("No prompts yet — submit one via the API or SupervisorAgent.")
