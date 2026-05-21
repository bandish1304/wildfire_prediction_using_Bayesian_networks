import pandas as pd
from sklearn.naive_bayes import CategoricalNB
import joblib
import numpy as np

df = pd.read_csv('data/processed/model_data.csv')
features = ['TAVG_CAT', 'TMAX_CAT', 'TMIN_CAT', 'PRCP_CAT', 'SEASON_weather']
target = 'WILDFIRE_OCCURRENCE'

X = df[features].apply(lambda col: col.astype('category').cat.codes)
y = df[target].astype(int)

model = CategoricalNB()
model.fit(X, y)
joblib.dump(model, 'models/naive_bayes_model.pkl')

example = {
    'TAVG_CAT': 'High',
    'TMAX_CAT': 'High',
    'TMIN_CAT': 'Medium',
    'PRCP_CAT': 'Dry',
    'SEASON_weather': 'Summer'
}
example_df = pd.DataFrame([{k: v for k, v in example.items()}])
for col in features:
    cats = df[col].astype('category').cat.categories
    example_df[col] = pd.Categorical(example_df[col], categories=cats).codes

proba = model.predict_proba(example_df)[0][1]
print(f"Wildfire probability for scenario {example}: {proba*100:.1f}%")
