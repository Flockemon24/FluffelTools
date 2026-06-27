import streamlit as st

def run_calculator():
    st.title("Calculator")
    st.write("This is a simple calculator tool.")

    # Select operation
    operation = st.selectbox("Select an operation", ["Add", "Subtract", "Multiply", "Divide"])

    # Perform calculation based on selected operation
    if operation == "Add":
        # Input fields for the two numbers
        num1 = st.number_input("Enter the first number", value=0.0)
        num2 = st.number_input("Enter the second number", value=0.0)
        result = num1 + num2
    elif operation == "Subtract":
        num1 = st.number_input("Enter the first number", value=0.0)
        num2 = st.number_input("Enter the second number", value=0.0)
        result = num1 - num2
    elif operation == "Multiply":
        num1 = st.number_input("Enter the first number", value=0.0)
        num2 = st.number_input("Enter the second number", value=0.0)
        result = num1 * num2
    elif operation == "Divide":
        num1 = st.number_input("Enter the first number", value=0.0)
        num2 = st.number_input("Enter the second number", value=0.0)
        if num2 != 0:
            result = num1 / num2
        else:
            result = "Error: Division by zero"

    # Display the result
    st.success(f"The result of {operation.lower()}ing {num1} and {num2} is: {result}")