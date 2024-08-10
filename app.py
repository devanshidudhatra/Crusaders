from flask import Flask, render_template, request
from modules.RadiationPredictor import predict_damage  # Correct import statement

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        wavelength = float(request.form["wavelength"])
        irradiance = float(request.form["irradiance"])
        satellite_damage, astronaut_harm = predict_damage(wavelength, irradiance)
        return render_template("index.html", result_satellite=satellite_damage, result_astronaut=astronaut_harm)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)-