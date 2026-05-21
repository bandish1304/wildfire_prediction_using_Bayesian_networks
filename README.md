Layout of the code

App
Contains the Streamlit web app (app.py). This is the user interface where you enter weather and season details and get wildfire risk predictions.

Bayesian network model
This folder has all the main scripts for data processing, model training, and running the Bayesian Network.
build_bayesian_network.py: Builds and trains the Bayesian Network model using the processed data.
preprocess_data.py: Cleans and prepares the raw weather and wildfire data for modeling.
model_data.py: Handles merging and final preparation of the dataset for the model.
draw_bayesian_network.py: Visualizes the structure of the Bayesian Network.

# added after presentation
fetch_live_weather.py: Fetches live weather data from an online API so you can use real-time info in predictions. (New)

Data
This folder is for all the data files.
raw: The original weather and wildfire data files.(from NOAA and calFire)
processed: Cleaned and categorized data, ready for modeling.


Tests
Contains test files to check that the main scripts and functions work as expected.
test_bayesian_network.py: Tests the Bayesian Network inference.

# Added after presentation
test_fetch_live_weather.py: Tests the live weather API code, including both valid and invalid city names. (New)


requirements.txt
Lists all the Python libraries you need to install to run the project.