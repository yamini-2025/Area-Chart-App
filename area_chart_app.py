import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Area Chart Generator", layout="wide")

st.title("Excel to Area Chart")

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, sheet_name=0)
    st.subheader("Preview of Uploaded Data")
    st.dataframe(df.head())

    # Automatically detect potential X (date) and Y (numeric) columns
    date_cols = df.select_dtypes(include=['datetime64[ns]', 'object']).columns.tolist()
    num_cols = df.select_dtypes(include='number').columns.tolist()

    if len(date_cols) > 0 and len(num_cols) > 0:
        st.subheader("🛠️ Choose Columns for Area Chart")

        x_axis = st.selectbox("Select Date/Time Column (X-axis)", date_cols)
        y_axis = st.selectbox("Select Numeric Column (Y-axis)", num_cols)

        try:
            df[x_axis] = pd.to_datetime(df[x_axis])
        except Exception as e:
            st.warning(f"Couldn't parse {x_axis} as datetime. Error: {e}")

        fig = px.area(df, x=x_axis, y=y_axis, title=f"{y_axis} over {x_axis}")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Your Excel file must contain at least one date/time and one numeric column.")
