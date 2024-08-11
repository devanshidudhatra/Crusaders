document.getElementById("prediction-form").addEventListener("submit", function (e) {
    e.preventDefault();
    const wavelength = document.getElementById("wavelength").value;
    const irradiance = document.getElementById("irradiance").value;

    fetch("/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            wavelength: wavelength,
            irradiance: irradiance,
        }),
    })
    .then(response => response.json())
    .then(data => {
        const resultDiv = document.getElementById("result");
        const satelliteMsg = data.satellite_damage ? "Harmful to Satellites" : "Safe for Satellites";
        const astronautMsg = data.astronaut_harm ? "Harmful to Astronauts" : "Safe for Astronauts";
        resultDiv.innerHTML = `
            <p>Satellite Damage: ${satelliteMsg}</p>
            <p>Astronaut Harm: ${astronautMsg}</p>
        `;
    })
    .catch(error => {
        console.error("Error:", error);
    });
});
