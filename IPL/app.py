# app.py
import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(page_title="IPL Score Predictor", layout="wide")

st.title("🏏 IPL Score Prediction System")
st.markdown("---")

# Load model
try:
    model = pickle.load(open("linear_regressor.pkl", "rb"))
except:
    st.error("Model not found! Please train the model first using train_model.py")
    st.stop()

# IPL Teams from notebook
teams = [
    'Kolkata Knight Riders',
    'Chennai Super Kings',
    'Rajasthan Royals',
    'Mumbai Indians',
    'Kings XI Punjab',
    'Royal Challengers Bangalore',
    'Delhi Daredevils',
    'Sunrisers Hyderabad'
]

st.header("Input Match Details")

col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox("🏏 Batting Team", teams)

with col2:
    bowling_team = st.selectbox("🎯 Bowling Team", teams)

st.markdown("---")
st.header("Game Progress")

col3, col4, col5 = st.columns(3)

with col3:
    overs = st.slider("Overs Completed", 5.0, 20.0, 10.0, step=0.1)

with col4:
    runs = st.number_input("Current Runs", min_value=0, max_value=300, value=80)

with col5:
    wickets = st.number_input("Wickets Fallen", min_value=0, max_value=10, value=2)

st.markdown("---")
st.header("Last 5 Overs Performance")

col6, col7 = st.columns(2)

with col6:
    runs_last_5 = st.number_input("Runs in Last 5 Overs", min_value=0, max_value=100, value=30)

with col7:
    wickets_last_5 = st.number_input("Wickets in Last 5 Overs", min_value=0, max_value=5, value=1)

st.markdown("---")

if st.button("🔮 Predict Final Score", use_container_width=True):
    # Prepare data for prediction
    input_data = {
        'batting_team_Chennai Super Kings': 1 if batting_team == 'Chennai Super Kings' else 0,
        'batting_team_Delhi Daredevils': 1 if batting_team == 'Delhi Daredevils' else 0,
        'batting_team_Kings XI Punjab': 1 if batting_team == 'Kings XI Punjab' else 0,
        'batting_team_Kolkata Knight Riders': 1 if batting_team == 'Kolkata Knight Riders' else 0,
        'batting_team_Mumbai Indians': 1 if batting_team == 'Mumbai Indians' else 0,
        'batting_team_Rajasthan Royals': 1 if batting_team == 'Rajasthan Royals' else 0,
        'batting_team_Royal Challengers Bangalore': 1 if batting_team == 'Royal Challengers Bangalore' else 0,
        'batting_team_Sunrisers Hyderabad': 1 if batting_team == 'Sunrisers Hyderabad' else 0,
        'bowling_team_Chennai Super Kings': 1 if bowling_team == 'Chennai Super Kings' else 0,
        'bowling_team_Delhi Daredevils': 1 if bowling_team == 'Delhi Daredevils' else 0,
        'bowling_team_Kings XI Punjab': 1 if bowling_team == 'Kings XI Punjab' else 0,
        'bowling_team_Kolkata Knight Riders': 1 if bowling_team == 'Kolkata Knight Riders' else 0,
        'bowling_team_Mumbai Indians': 1 if bowling_team == 'Mumbai Indians' else 0,
        'bowling_team_Rajasthan Royals': 1 if bowling_team == 'Rajasthan Royals' else 0,
        'bowling_team_Royal Challengers Bangalore': 1 if bowling_team == 'Royal Challengers Bangalore' else 0,
        'bowling_team_Sunrisers Hyderabad': 1 if bowling_team == 'Sunrisers Hyderabad' else 0,
        'overs': overs,
        'runs': runs,
        'wickets': wickets,
        'runs_last_5': runs_last_5,
        'wickets_last_5': wickets_last_5
    }

    df = pd.DataFrame([input_data])
    prediction = model.predict(df)[0]

    # Display results
    st.markdown("---")
    col_result1, col_result2 = st.columns(2)
    
    with col_result1:
        st.metric("📊 Current Score", runs)
    
    with col_result2:
        st.metric("🎯 Overs Completed", f"{overs:.1f}/20")

    st.success(f"### 🏆 Predicted Final Score: {round(prediction)} runs")
    
    # Additional info
    runs_required = max(0, round(prediction) - runs)
    remaining_overs = 20 - overs
    
    if remaining_overs > 0:
        run_rate_needed = runs_required / remaining_overs
        st.info(f"📈 Run Rate Required: {run_rate_needed:.2f} per over over the next {remaining_overs:.1f} overs")