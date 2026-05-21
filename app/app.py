
import streamlit as st
import pandas as pd
import joblib
from pgmpy.inference import VariableElimination

st.title('California Wildfire Risk Prediction')
st.write('Enter weather and season details to get a wildfire risk prediction.')

@st.cache_resource
def load_bn_model():
    return joblib.load('models/bayesian_network_model.pkl')

model = load_bn_model()
inference = VariableElimination(model)

col1, col2 = st.columns(2)
with col1:
    tmax_cat = st.selectbox('Max Temp Category', ['Low', 'Medium', 'High'])
    prcp_cat = st.selectbox('Precipitation Category', ['Dry', 'Light', 'Wet'])
with col2:
    tmin_cat = st.selectbox('Min Temp Category', ['Low', 'Medium', 'High'])
    season_weather = st.selectbox('Season', ['Spring', 'Summer', 'Fall', 'Winter'])

if st.button('Predict Wildfire Risk'):
    evidence = {
        'TMAX_CAT': tmax_cat,
        'TMIN_CAT': tmin_cat,
        'PRCP_CAT': prcp_cat,
        'SEASON_weather': season_weather
    }
    try:
        result = inference.query(variables=['WILDFIRE_OCCURRENCE'], evidence=evidence)
        state_names = result.state_names['WILDFIRE_OCCURRENCE']
        if 1 in state_names:
            idx = list(state_names).index(1)
            prob = result.values[idx]
        else:
            prob = 0.0
        if prob >= 0.7:
            st.error(f'High wildfire risk! Probability: {prob*100:.1f}%')
        elif prob >= 0.4:
            st.warning(f'Medium wildfire risk. Probability: {prob*100:.1f}%')
        else:
            st.success(f'Low wildfire risk. Probability: {prob*100:.1f}%')
        st.caption(f'Calculation based on: {evidence}')
    except Exception as e:
        st.error(f'Could not calculate risk: {e}')
