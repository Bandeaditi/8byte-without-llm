import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from util import process_file
from db import init_db, insert_receipt, get_all_receipts

st.title("🧾 Receipt Analyzer (Simple Version)")

init_db()

uploaded_file = st.file_uploader("Upload receipt (.jpg/.png/.pdf)", type=["jpg", "png", "pdf"])
if uploaded_file:
    with st.spinner("Processing..."):
        data = process_file(uploaded_file)
        insert_receipt(data)
        st.success("Receipt saved!")
        st.write("Parsed Data:", data)

st.write("## 📊 Summary Dashboard")
all_data = get_all_receipts()
df = pd.DataFrame(all_data, columns=["ID", "Vendor", "Date", "Amount", "Category"])
st.dataframe(df)

if not df.empty:
    st.write("### Spend by Vendor")
    st.bar_chart(df.groupby("Vendor")["Amount"].sum())

    st.write("### Monthly Trend")
    df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
    df["Month"] = df["Date"].dt.to_period("M")
    monthly = df.groupby("Month")["Amount"].sum()
    st.line_chart(monthly)
