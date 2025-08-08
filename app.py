import pandas as pd
import streamlit as st
import hashlib
import time

st.title("Apollo → People Import CSV Converter")

def md5_hash(value):
    if pd.isna(value) or not str(value).strip():
        return ""
    return hashlib.md5(value.strip().lower().encode()).hexdigest()

def process_apollo_file(file):
    try:
        df = pd.read_csv(file)

        required = ["First Name", "Last Name", "Email", "City", "Company", "Title"]
        missing = [c for c in required if c not in df.columns]
        if missing:
            return None, f"Missing columns: {', '.join(missing)}"

        out_df = pd.DataFrame()
        out_df["id"] = df["Email"].apply(md5_hash)
        out_df["created_at"] = int(time.time())  # current timestamp
        out_df["email"] = df["Email"]
        out_df["first_name"] = df["First Name"]
        out_df["last_name"] = df["Last Name"]
        out_df["city"] = df["City"]
        out_df["unsubscribed"] = False
        out_df["plan_name"] = df["Company"]
        out_df["role"] = df["Title"]

        return out_df, None

    except Exception as e:
        return None, f"Error: {str(e)}"

uploaded_file = st.file_uploader("Upload Apollo CSV", type=["csv"])

if uploaded_file:
    st.info("Processing file...")
    out_df, error = process_apollo_file(uploaded_file)

    if error:
        st.error(error)
    else:
        st.success("File processed successfully!")
        st.write(f"✅ {len(out_df)} records converted")
        st.write(out_df.head())

        csv_data = out_df.to_csv(index=False).encode("utf-8")
        st.download_button("Download Converted CSV", csv_data, "people-import.csv", "text/csv")
