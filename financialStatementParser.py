import streamlit as st
import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")  
BASE_URL = "https://financialmodelingprep.com/stable/"

st.set_page_config(page_title="Financial Statement Parser", layout="wide")

st.title("Fundamental Analysis Dashboard")
st.sidebar.header("Search Parameters")

# Sidebar Inputs
ticker = st.sidebar.text_input("Enter Ticker").upper()
statement_choice = st.sidebar.selectbox(
    "Select Statement Type",
    options=["Income Statement", "Balance Sheet", "Cash Flow"]
)

statement_map = {
    "Income Statement": "income-statement",
    "Balance Sheet": "balance-sheet-statement",
    "Cash Flow": "cash-flow-statement"
}

@st.cache_data  
def get_financial_data(ticker, statement_type):
    url = f"{BASE_URL}{statement_type}?symbol={ticker}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data:
            df = pd.DataFrame(data)
            df = df.set_index('date').transpose()
            return df
    return None

if ticker:
    st.subheader(f"{statement_choice} for {ticker}")
    
    with st.spinner(f"Fetching {statement_choice}..."):
        df = get_financial_data(ticker, statement_map[statement_choice])
        
        if df is not None:
            
            st.dataframe(df, use_container_width=True)
            
            csv = df.to_csv().encode('utf-8')
            st.download_button(
                label="Download as CSV",
                data=csv,
                file_name=f"{ticker}_{statement_map[statement_choice]}.csv",
                mime="text/csv",
            )
        else:
            st.error("No data found. Please check the ticker symbol or your API key.")
else:
    st.info("Enter a ticker symbol in the sidebar to get started.")