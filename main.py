import streamlit as st
import src

with st.sidebar:
    st.title("FluffelTools")
    selected_tool = st.radio("Select a tool you want to use", ["Calculator", "Interest Calculator", "Chart Generator", "Vocabulary Trainer", "Unit Converter", "Password Generator", "Weather App"])

if selected_tool == "Calculator":
    src.calculator.run_calculator()
elif selected_tool == "Interest Calculator":
    src.interest_calculator.run_interest_calculator()
elif selected_tool == "Chart Generator":
    src.chart_generator.run_chart_generator()
elif selected_tool == "Vocabulary Trainer":
    src.vocabulary_trainer.run_vocabulary_trainer()
elif selected_tool == "Unit Converter":
    src.unit_converter.run_unit_converter()
elif selected_tool == "Password Generator":
    src.password_generator.run_password_generator()
elif selected_tool == "Weather App":
    src.weather_app.run_weather_app()
