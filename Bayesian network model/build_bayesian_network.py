
from pgmpy.models import DiscreteBayesianNetwork
import pandas as pd
from pgmpy.estimators import MaximumLikelihoodEstimator

model = DiscreteBayesianNetwork([
    ('TAVG_CAT', 'WILDFIRE_OCCURRENCE'),
    ('TMAX_CAT', 'WILDFIRE_OCCURRENCE'),
    ('TMIN_CAT', 'WILDFIRE_OCCURRENCE'),
    ('PRCP_CAT', 'WILDFIRE_OCCURRENCE'),
    ('SEASON_weather', 'WILDFIRE_OCCURRENCE')
])

print("Bayesian Network structure defined:")
print(model.edges())

print("\nLoading data and fitting the model...")
data = pd.read_csv('data/processed/model_data.csv')

cols = ['TAVG_CAT', 'TMAX_CAT', 'TMIN_CAT', 'PRCP_CAT', 'SEASON_weather', 'WILDFIRE_OCCURRENCE']
data = data[cols]

model.fit(data, estimator=MaximumLikelihoodEstimator)
print("Model training complete. Learned CPDs:")

for cpd in model.get_cpds():
    print(f"CPD for {cpd.variable}: shape {cpd.values.shape}")

from pgmpy.inference import VariableElimination
inference = VariableElimination(model)
print("\nInference engine initialized. Ready for queries.")

print("\n--- Wildfire Risk Inference Example ---")
evidence = {
    'TMAX_CAT': 'High',
    'PRCP_CAT': 'Dry',
    'SEASON_weather': 'Summer'
}
print(f"Evidence: {evidence}")
result = inference.query(variables=['WILDFIRE_OCCURRENCE'], evidence=evidence)
print("\nProbability of wildfire occurrence given evidence:")
print(result)

state_names = result.state_names['WILDFIRE_OCCURRENCE']
if 1 in state_names:
    idx = list(state_names).index(1)
    prob_wildfire = result.values[idx]
else:
    prob_wildfire = 0.0
print(f"\n[7.1] Probability of wildfire occurrence: {prob_wildfire:.2f}")

low_threshold = 0.3
high_threshold = 0.7
print(f"[7.2] Risk thresholds: Low < {low_threshold}, Medium < {high_threshold}, High >= {high_threshold}")

# Determine risk level
if prob_wildfire < low_threshold:
	risk_level = 'Low'
elif prob_wildfire < high_threshold:
	risk_level = 'Medium'
else:
	risk_level = 'High'
print(f"[7.3] Risk level: {risk_level}")

# Select recommendation message
if risk_level == 'Low':
	recommendation = "Wildfire risk is low. Standard precautions are recommended."
elif risk_level == 'Medium':
	recommendation = "Wildfire risk is moderate. Be alert and avoid unnecessary outdoor burning."
else:
	recommendation = "Wildfire risk is HIGH! Avoid open flames, monitor local alerts, and prepare for possible evacuation."
print(f"[7.4] Recommendation: {recommendation}")

# Display the recommendation to the user
print(f"\n[7.5] FINAL RECOMMENDATION: {recommendation}")
