import streamlit as st

def run_interest_calculator():
    st.title("Interest Calculator")
    st.write("This tool allows you to calculate simple and compound interest.")

    # Input principal amount
    principal = st.number_input("Enter the principal amount", min_value=0.0, value=1000.0)

    # Input annual interest rate
    rate = st.number_input("Enter the annual interest rate (in %)", min_value=0.0, value=5.0)

    # Input time in years
    time = st.number_input("Enter the time in years", min_value=0.0, value=1.0)

    # Select interest type
    interest_type = st.selectbox("Select interest type", ["Simple Interest", "Compound Interest"])

    if interest_type == "Simple Interest":
        interest = (principal * rate * time) / 100
        total_amount = principal + interest
        st.write(f"Simple Interest: {interest:.2f}")
        st.success(f"Total Amount after {time} years: {total_amount:.2f}")
    else:
        n = st.number_input("Enter the number of times interest is compounded per year", min_value=1, value=1)
        total_amount = principal * (1 + (rate / (n * 100))) ** (n * time)
        interest = total_amount - principal
        st.write(f"Compound Interest: {interest:.2f}")
        st.success(f"Total Amount after {time} years: {total_amount:.2f}")