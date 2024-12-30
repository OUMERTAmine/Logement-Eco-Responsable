console.log("Fichier JavaScript chargé !");

fetch("http://127.0.0.1:8000/meteo-5jours")
    .then(response => response.json())
    .then(data => {
        console.log("Données reçues :", data);
        document.getElementById("ville").textContent = `Ville : ${data.ville}`;
        document.getElementById("temperature").textContent = `Température actuelle : ${data.previsions[0].temperature}°C`;
        document.getElementById("humidite").textContent = `Humidité : ${data.previsions[0].humidite}%`;
        document.getElementById("pression").textContent = `Pression : ${data.previsions[0].pression} hPa`;

        const labels = data.previsions.map(p => p.date_heure);
        const temperatures = data.previsions.map(p => p.temperature);

        const ctx = document.getElementById("tempChart").getContext("2d");
        new Chart(ctx, {
            type: "line",
            data: {
                labels: labels,
                datasets: [{
                    label: "Température (°C)",
                    data: temperatures,
                    borderColor: "rgba(75, 192, 192, 1)",
                    backgroundColor: "rgba(75, 192, 192, 0.2)",
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: true,
                        position: "top"
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: "Date et Heure"
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: "Température (°C)"
                        }
                    }
                }
            }
        });
    })
    .catch(error => console.error("Erreur lors du chargement des données météo :", error));
