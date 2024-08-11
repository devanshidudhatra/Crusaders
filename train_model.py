import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE
import joblib

# Define helper functions
def Harmful_for_Satellites(row):
    return int(row["wavelength"] < 300 and row["irradiance_in_W/m2"] > 15)

def Harmful_for_Astronauts(row):
    return int(row["wavelength"] < 350 and row["irradiance_in_W/m2"] > 150)

def categorize_wavelength(wavelength):
    if 320 <= wavelength <= 400:
        return 'UVA'
    elif 280 <= wavelength < 320:
        return 'UVB'
    elif 100 <= wavelength < 280:
        return 'UVC'
    elif 400 <= wavelength <= 700:
        return 'Visible'
    elif 700 < wavelength <= 1400:
        return 'NIR'
    elif 1400 < wavelength <= 3000:
        return 'SWIR'
    else:
        return 'Other'

# Load and process the data
raw_data = pd.read_csv("solarcurrent.csv")
selected_columns = raw_data[['date', 'wavelength', 'irradiance']]
selected_columns.to_csv('required_data.csv', index=False)
required_data = pd.read_csv("required_data.csv")
required_data["irradiance_in_W/m2"] = required_data["wavelength"] * required_data["irradiance"]
required_data['Band'] = required_data['wavelength'].apply(categorize_wavelength)
required_data["Harmful_for_Satellites"] = required_data.apply(Harmful_for_Satellites, axis=1)
required_data["Harmful_for_Astronauts"] = required_data.apply(Harmful_for_Astronauts, axis=1)

# Save the processed data
required_data.to_csv("required_data.csv", index=False)

X = required_data[['wavelength', 'irradiance_in_W/m2']]
y_satellite = required_data['Harmful_for_Satellites']
y_astronaut = required_data['Harmful_for_Astronauts']

# Split the data
X_train_sat, X_test_sat, y_train_sat, y_test_sat = train_test_split(X, y_satellite, test_size=0.2, random_state=42)
X_train_ast, X_test_ast, y_train_ast, y_test_ast = train_test_split(X, y_astronaut, test_size=0.2, random_state=42)

# Train the models
model_sat = LogisticRegression()
model_sat.fit(X_train_sat, y_train_sat)
joblib.dump(model_sat, 'model_satellite.pkl')

model_ast = LogisticRegression()
model_ast.fit(X_train_ast, y_train_ast)
joblib.dump(model_ast, 'model_astronaut.pkl')

# Evaluate the models
y_pred_sat = model_sat.predict(X_test_sat)
y_pred_ast = model_ast.predict(X_test_ast)

print("Evaluating Satellite Model")
print("Accuracy: ", accuracy_score(y_pred_sat, y_test_sat))
print("Confusion Matrix: \n", confusion_matrix(y_pred_sat, y_test_sat))
print("Classification Report: \n", classification_report(y_pred_sat, y_test_sat))

print("\nEvaluating Astronaut Model")
print("Accuracy: ", accuracy_score(y_pred_ast, y_test_ast))
print("Confusion Matrix: \n", confusion_matrix(y_pred_ast, y_test_ast))
print("Classification Report: \n", classification_report(y_pred_ast, y_test_ast))

# Determine safe irradiance ranges
safe_satellite_data = required_data[(required_data['wavelength'] >= 280) & (required_data['irradiance_in_W/m2'] <= 10)]
satellite_safe_irradiance_range = (safe_satellite_data['irradiance_in_W/m2'].min(), safe_satellite_data['irradiance_in_W/m2'].max())

safe_astronaut_data = required_data[(required_data['wavelength'] >= 320) & (required_data['irradiance_in_W/m2'] <= 120)]
astronaut_safe_irradiance_range = (safe_astronaut_data['irradiance_in_W/m2'].min(), safe_astronaut_data['irradiance_in_W/m2'].max())

print(f"Satellite safe irradiance range: {satellite_safe_irradiance_range}")
print(f"Astronaut safe irradiance range: {astronaut_safe_irradiance_range}")
