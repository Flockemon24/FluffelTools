import streamlit as st
import matplotlib.pyplot as plt

def run_chart_generator():
    st.title("Chart Generator")
    st.write("This tool allows you to generate simple charts.")

    # Input data for the chart
    data_input = st.text_area("Enter your data (comma-separated values)", "1, 2, 3, 4, 5")
    data = [float(x.strip()) for x in data_input.split(",")]

    # Select chart type
    chart_type = st.selectbox("Select chart type", ["Line Chart", "Bar Chart", "Scatter Plot"])

    # Generate and display the chart based on selected type
    if chart_type == "Line Chart":
        plt.plot(data)
        plt.title("Line Chart")
        plt.xlabel("Index")
        plt.ylabel("Value")
        st.pyplot(plt)
    elif chart_type == "Bar Chart":
        plt.bar(range(len(data)), data)
        plt.title("Bar Chart")
        plt.xlabel("Index")
        plt.ylabel("Value")
        st.pyplot(plt)
    elif chart_type == "Scatter Plot":
        plt.scatter(range(len(data)), data)
        plt.title("Scatter Plot")
        plt.xlabel("Index")
        plt.ylabel("Value")
        st.pyplot(plt)