# Wildfire Prediction Using Bayesian Networks

## Overview
This project predicts wildfire risk using a **Bayesian Network** based on weather conditions and seasonal information. It combines historical wildfire and weather data, preprocesses the data, trains a probabilistic model, and provides predictions through a **Streamlit web application**.

The goal of the project is to estimate wildfire risk in an interpretable way using probabilistic reasoning rather than only black-box machine learning models.

---

## Features
- Predicts wildfire risk from weather and seasonal inputs
- Uses a **Bayesian Network** for probabilistic modeling
- Includes data preprocessing and model-building scripts
- Provides a **Streamlit-based web app** for user interaction
- Supports **live weather fetching** for real-time prediction inputs
- Includes test files for model inference and weather API functionality

---

## Project Structure

### App
Contains the Streamlit web app:
- `app.py` – User interface for entering weather and season details and viewing wildfire risk predictions

### Bayesian Network Model
Contains the scripts for data processing, training, and visualization:
- `build_bayesian_network.py` – Builds and trains the Bayesian Network model
- `preprocess_data.py` – Cleans and prepares raw weather and wildfire data
- `model_data.py` – Merges and prepares the final dataset for modeling
- `draw_bayesian_network.py` – Visualizes the Bayesian Network structure
- `fetch_live_weather.py` – Fetches live weather data from an online API for real-time predictions

### Data
Stores project datasets:
- `raw/` – Original weather and wildfire data files (for example, NOAA and CalFire sources)
- `processed/` – Cleaned and categorized data ready for modeling

### Tests
Contains test files:
- `test_bayesian_network.py` – Tests Bayesian Network inference
- `test_fetch_live_weather.py` – Tests live weather API behavior for valid and invalid city names

### Other Files
- `requirements.txt` – Python dependencies required to run the project

---

## How It Works
1. Raw wildfire and weather data are collected
2. The data is cleaned and transformed into a modeling-friendly format
3. A Bayesian Network is built to represent dependencies between variables
4. The trained model is used to estimate wildfire risk probabilities
5. Users can interact with the model through the Streamlit app
6. Optionally, live weather data can be fetched and used for prediction

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/bandish1304/wildfire_prediction_using_Bayesian_networks.git
cd wildfire_prediction_using_Bayesian_networks
```

### 2. Create a virtual environment
```bash
python -m venv venv
```

Activate it:

**Windows**
```bash
venv\Scripts\activate
```

**macOS/Linux**
```bash
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## Running the Project

### Run the Streamlit app
```bash
streamlit run App/app.py
```

If your app file is located somewhere else, update the path accordingly.

---

## Running Tests
To run the test files:

```bash
pytest
```

Or run specific tests:

```bash
pytest test_bayesian_network.py
pytest test_fetch_live_weather.py
```

---

## Example Use Case
A user enters:
- temperature
- humidity
- wind conditions
- season

The system then uses the Bayesian Network to estimate wildfire risk and displays the predicted result in the web app.

---

## Technologies Used
- Python
- Streamlit
- Bayesian Networks
- Pandas / NumPy
- PyTest
- Weather API integration

---

## Future Improvements
- Improve prediction accuracy with more data
- Add more environmental features
- Deploy the Streamlit app online
- Add maps and regional wildfire visualization
- Support batch predictions for multiple locations

