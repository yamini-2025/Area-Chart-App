import streamlit as st
import pandas as pd
import plotly.express as px

# Set up the Streamlit app
st.set_page_config(page_title="Area Chart Generator", layout="wide")
st.title("Excel to Area Chart")

# Upload Excel file
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    # Read the first sheet
    df = pd.read_excel(uploaded_file, sheet_name=0)
    st.subheader("Preview of Uploaded Data")
    st.dataframe(df.head())

    # Detect date/time and numeric columns
    date_cols = df.select_dtypes(include=['datetime64[ns]', 'object']).columns.tolist()
    num_cols = df.select_dtypes(include='number').columns.tolist()

    if len(date_cols) > 0 and len(num_cols) > 0:
        st.subheader("Choose Columns for Area Chart")

        x_axis = st.selectbox("Select Date/Time Column (X-axis)", date_cols)
        y_axis = st.selectbox("Select Numeric Column (Y-axis)", num_cols)

        try:
            # Convert selected x-axis column to datetime
            df[x_axis] = pd.to_datetime(df[x_axis])
        except Exception as e:
            st.warning(f"Couldn't parse {x_axis} as datetime. Error: {e}")

        # Format date labels (e.g., Jan-2020)
        df["Date"] = df[x_axis].dt.strftime('%b-%Y')

        # Create smooth area chart with data labels
        fig = px.area(
            df,
            x="Date",
            y=y_axis,
            title=f"{y_axis} Over Time ({x_axis})",
            text=y_axis,
        )

        fig.update_traces(
            mode='lines+markers+text',
            textposition='top center',
            line_shape='spline',  # Smooth curve
            texttemplate='%{text:.0f}'  # Remove decimal from labels
        )

        fig.update_layout(
            xaxis_title=x_axis,
            yaxis_title=y_axis,
            hovermode="x unified",
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Your Excel file must contain at least one date/time and one numeric column.")
