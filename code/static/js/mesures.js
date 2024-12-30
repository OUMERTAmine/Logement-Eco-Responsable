const params = new URLSearchParams(window.location.search);
const capteurId = params.get("capteur_id");

fetch(`http://127.0.0.1:8000/mesure-capteur/${capteurId}`)
    .then(response => response.json())
    .then(data => {
        console.log("Données récupérées :", data);
        const mesuresTable = document.getElementById("mesuresTable");

        // Ajout des données dans le tableau
        data.mesures.forEach(mesure => {
            mesuresTable.innerHTML += `
                <tr>
                    <td>${mesure.id}</td>
                    <td>${mesure.valeur}</td>
                    <td>${mesure.date_insertion}</td>
                </tr>
            `;
        });

        // Génération du graphe
        const labels = data.mesures.map(mesure => mesure.date_insertion);
        const valeurs = data.mesures.map(mesure => mesure.valeur);

        const ctx = document.getElementById("mesuresChart").getContext("2d");
        new Chart(ctx, {
            type: "line",
            data: {
                labels: labels,
                datasets: [{
                    label: "Valeurs des Mesures",
                    data: valeurs,
                    borderColor: "rgba(75, 192, 192, 1)",
                    backgroundColor: "rgba(75, 192, 192, 0.2)",
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
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
                            text: "Valeur"
                        }
                    }
                }
            }
        });
    })
    .catch(error => console.error("Erreur lors du chargement des mesures :", error));
