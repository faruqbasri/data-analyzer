import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io

# ------------------ Page Config ------------------
st.set_page_config(
    page_title="Analyze Your Data",
    page_icon="🌈",
    layout="wide"
)

st.title("🌈 Analyze Your Data")
st.write("📁 Upload your **CSV** or **Excel** file")

# ------------------ File Upload ------------------
uploaded_file = st.file_uploader(
    "Upload a CSV or Excel File",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:
    try:
        file_ext = uploaded_file.name.lower().split(".")[-1]

        if file_ext == "csv":
            data = pd.read_csv(uploaded_file)
        elif file_ext == "xlsx":
            data = pd.read_excel(uploaded_file, engine="openpyxl")
        else:
            st.error("☠️ Unsupported file format")
            st.stop()

        # Convert boolean columns to string for display safety
        bool_cols = data.select_dtypes(include="bool").columns
        data[bool_cols] = data[bool_cols].astype(str)

    except Exception as e:
        st.error("😵‍💫 Could not read the file")
        st.exception(e)
        st.stop()

    st.success("✅ File uploaded successfully")

    # ------------------ Preview ------------------
    st.subheader("👀 Data Preview")
    st.dataframe(data.head(), use_container_width=True)

    # ------------------ Overview ------------------
    st.subheader("📊 Data Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Rows", data.shape[0])
    col2.metric("Columns", data.shape[1])
    col3.metric("Missing Values", data.isnull().sum().sum())
    col4.metric("Duplicate Rows", data.duplicated().sum())

    # ------------------ Info Summary ------------------
    st.subheader("📄 Dataset Info")
    buffer = io.StringIO()
    data.info(buf=buffer)
    st.text(buffer.getvalue())

    # ------------------ Statistical Summary ------------------
    st.subheader("📈 Statistical Summary (Numeric)")
    st.dataframe(data.describe(), use_container_width=True)

    non_numeric_cols = data.select_dtypes(include=["object", "bool"]).columns
    if len(non_numeric_cols) > 0:
        st.subheader("📈 Statistical Summary (Categorical)")
        st.dataframe(data.describe(include=["object", "bool"]), use_container_width=True)

    # ------------------ Column Selection ------------------
    st.subheader("🛠️ Select Columns for Analysis")
    selected_cols = st.multiselect("Choose Columns", data.columns.tolist())

    if selected_cols:
        st.dataframe(data[selected_cols].head(), use_container_width=True)
    else:
        st.info("No columns selected — showing full dataset")

    # ------------------ Visualization ------------------
    st.subheader("📊 Data Visualization")

    numeric_cols = data.select_dtypes(include=np.number).columns.tolist()
    all_cols = data.columns.tolist()

    if not numeric_cols:
        st.warning("No numeric columns available for plotting")
    else:
        x_axis = st.selectbox("Select X-axis", all_cols)
        y_axis = st.selectbox("Select Y-axis (numeric)", numeric_cols)

        col1, col2, col3 = st.columns(3)

        with col1:
            line_btn = st.button("📈 Line Chart")
            bar_btn = st.button("📊 Bar Chart")

        with col2:
            scatter_btn = st.button("🔵 Scatter Plot")
            hist_btn = st.button("📉 Histogram")

        with col3:
            pie_btn = st.button("🥧 Pie Chart")
            heatmap_btn = st.button("🔥 Heatmap")

        # Line Chart
        if line_btn:
            fig, ax = plt.subplots()
            ax.plot(data[x_axis], data[y_axis])
            ax.set_title("Line Chart")
            st.pyplot(fig)

        # Scatter Plot
        if scatter_btn:
            fig, ax = plt.subplots()
            ax.scatter(data[x_axis], data[y_axis])
            ax.set_title("Scatter Plot")
            st.pyplot(fig)

        # Bar Chart
        if bar_btn:
            fig, ax = plt.subplots()
            data.groupby(x_axis)[y_axis].mean().plot(kind="bar", ax=ax)
            ax.set_title("Bar Chart (Mean)")
            st.pyplot(fig)

        # Histogram
        if hist_btn:
            fig, ax = plt.subplots()
            ax.hist(data[y_axis].dropna(), bins=20)
            ax.set_title("Histogram")
            st.pyplot(fig)

        # Pie Chart
        if pie_btn:
            fig, ax = plt.subplots()
            pie_data = data[x_axis].value_counts().head(10)
            ax.pie(pie_data, labels=pie_data.index, autopct="%1.1f%%")
            ax.set_title("Pie Chart (Top 10)")
            st.pyplot(fig)

        # Heatmap
        if heatmap_btn:
            if len(numeric_cols) > 1:
                fig, ax = plt.subplots()
                corr = data[numeric_cols].corr()
                im = ax.imshow(corr)
                ax.set_xticks(range(len(corr.columns)))
                ax.set_yticks(range(len(corr.columns)))
                ax.set_xticklabels(corr.columns, rotation=90)
                ax.set_yticklabels(corr.columns)
                fig.colorbar(im)
                ax.set_title("Correlation Heatmap")
                st.pyplot(fig)
            else:
                st.warning("Need at least 2 numeric columns for heatmap")

    # ------------------ Dashboard ------------------
    st.subheader("📊 Dashboard")

    k1, k2, k3 = st.columns(3)
    k1.metric("Rows", data.shape[0])
    k2.metric("Columns", data.shape[1])
    k3.metric("Missing Values", data.isnull().sum().sum())

    if numeric_cols:
        fig, ax = plt.subplots()
        data[numeric_cols].mean().plot(kind="bar", ax=ax)
        ax.set_title("Average of Numeric Columns")
        st.pyplot(fig)

else:
    st.info("👆 Upload a CSV or Excel file to get started")
