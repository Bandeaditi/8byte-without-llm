import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import streamlit as st
from backend.parse import parse_receipt
from backend.database import save_receipt, init_db
import tempfile
import os

test_file = "test.txt"  # Path to your test file
receipt = parse_receipt(test_file)

# Show results
st.write("Vendor:", receipt.vendor)
st.write("Date:", receipt.date)
st.write("Amount:", receipt.amount)
st.write("Category:", receipt.category)
# Initialize database
init_db()

# UI Setup
st.title("Receipt Processor (No LLM)")
st.markdown("Upload receipts to track expenses")

# File uploader
uploaded_file = st.file_uploader(
    "Upload Receipt", 
    type=["jpg", "png", "pdf", "txt"],
    help="Supports JPG, PNG, PDF, and TXT files"
)

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded_file.getvalue())
        try:
            receipt = parse_receipt(tmp.name)
            save_receipt(receipt)
            st.success("✅ Receipt processed successfully!")
            
            # Display results
            st.subheader("Extracted Data")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Vendor", receipt.vendor)
                st.metric("Date", receipt.date)
            with col2:
                st.metric("Amount", f"${receipt.amount:.2f}")
                st.metric("Category", receipt.category)
            
        except Exception as e:
            st.error(f"Error processing receipt: {str(e)}")
        finally:
            os.unlink(tmp.name)

# Show all receipts
if st.button("View All Receipts"):
    import sqlite3
    import pandas as pd
    conn = sqlite3.connect("receipts.db")
    df = pd.read_sql("SELECT * FROM receipts", conn)
    conn.close()
    st.dataframe(df)