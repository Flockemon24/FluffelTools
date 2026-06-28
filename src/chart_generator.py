import streamlit as st
import matplotlib.pyplot as plt

def average(data):
    if len(data) == 0:
        return 0
    return sum(data) / len(data)

def run_chart_generator():
    st.title("Chart Generator")
    st.write("This tool allows you to generate simple charts.")

    # Input data for the chart
    data_input = st.text_area("Enter your data (comma-separated values)", "1, 2, 3, 4, 5")
    data = [float(x.strip()) for x in data_input.split(",")]

    # Select chart type
    chart_type = st.selectbox("Select chart type", ["Line Chart", "Bar Chart", "Scatter Plot"])

    # Input chart title
    chart_title = st.text_input("Chart Title", "My Chart")
    # Input axis labels
    x_label = st.text_input("X-Axis Label", "Index")
    y_label = st.text_input("Y-Axis Label", "Value")

    # Display average
    selected_average = st.checkbox("Display Average")

    # Generate and display the chart based on selected type
    if chart_type == "Line Chart":
        plt.plot(data)
        plt.title(chart_title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.axhline(y=average(data), color='yellow', linestyle='--', label='Average') if selected_average else None
        plt.legend()
        st.pyplot(plt)
    elif chart_type == "Bar Chart":
        plt.bar(range(len(data)), data)
        plt.title(chart_title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.axhline(y=average(data), color='yellow', linestyle='--', label='Average') if selected_average else None
        plt.legend()
        st.pyplot(plt)
    elif chart_type == "Scatter Plot":
        plt.scatter(range(len(data)), data)
        plt.title(chart_title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.axhline(y=average(data), color='yellow', linestyle='--', label='Average') if selected_average else None
        plt.legend()
        st.pyplot(plt)