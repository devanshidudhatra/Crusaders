from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load the trained models
model_sat = joblib.load('model_satellite.pkl')
model_ast = joblib.load('model_astronaut.pkl')

def predict_damage(wavelength, irradiance):
    X_new = pd.DataFrame({'wavelength': [wavelength], 'irradiance_in_W/m2': [wavelength * irradiance]})
    satellite_damage = int(model_sat.predict(X_new)[0])
    astronaut_harm = int(model_ast.predict(X_new)[0])
    return satellite_damage, astronaut_harm

def generate_precaution_text(satellite_damage, astronaut_harm):
    if satellite_damage:
        satellite_precaution = "The wavelength and irradiance levels detected could be harmful to satellites. Protective shielding or adjusting the satellite's orientation may be necessary."
    else:
        satellite_precaution = "The current wavelength and irradiance levels are within safe limits for satellites."

    if astronaut_harm:
        astronaut_precaution = "The detected levels could pose a risk to astronauts. It is recommended to minimize exposure time and ensure protective gear is worn."
    else:
        astronaut_precaution = "The current conditions are safe for astronaut exposure."

    return satellite_precaution, astronaut_precaution

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    wavelength = float(data["wavelength"])
    irradiance = float(data["irradiance"])
    satellite_damage, astronaut_harm = predict_damage(wavelength, irradiance)
    satellite_precaution, astronaut_precaution = generate_precaution_text(satellite_damage, astronaut_harm)
    return jsonify({
        "satellite_damage": satellite_damage,
        "astronaut_harm": astronaut_harm,
        "satellite_precaution": satellite_precaution,
        "astronaut_precaution": astronaut_precaution
    })

if __name__ == "__main__":
    app.run(debug=True)
