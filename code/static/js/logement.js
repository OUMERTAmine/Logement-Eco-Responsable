console.log("JavaScript chargé !");

// Charger les logements depuis l'API
fetch("http://127.0.0.1:8000/logement")
    .then(response => response.json())
    .then(data => {
        console.log("Données récupérées :", data); // Affichez les données récupérées
        if (data.logement && Array.isArray(data.logement)) {
            const logementsTable = document.getElementById("logementsTable");
            data.logement.forEach(logement => {
                logementsTable.innerHTML += `
                    <tr>
                        <td>${logement.id}</td>
                        <td>${logement.adresse}</td>
                        <td>${logement.telephone}</td>
                        <td>${logement.ip}</td>
                        <td>${logement.date_insertion}</td>
                        <td>
                            <button class="btn btn-primary voir-pieces" data-id="${logement.id}">Voir Pièces</button>
                            <button class="btn btn-success voir-factures" data-id="${logement.id}">Voir Factures</button>
                        </td>
                    </tr>
                `;
            });

            // Ajouter des gestionnaires d'événements aux boutons
            const boutonsVoirPieces = document.querySelectorAll(".voir-pieces");
            boutonsVoirPieces.forEach(button => {
                button.addEventListener("click", (event) => {
                    const logementId = event.target.dataset.id; // Récupère l'ID du logement
                    //window.location.href = `/pieces.html?logement_id=${logementId}`;
                    window.location.href = `http://127.0.0.1:8000/pieces?logement_id=${logementId}`;
                });
            });

            document.addEventListener("click", event => {
                if (event.target && event.target.classList.contains("voir-factures")) {
                    const logementId = event.target.getAttribute("data-id");
                    window.location.href = `http://127.0.0.1:8000/facture?logement_id=${logementId}`;
                }
            });
            

        } else {
            console.error("Données inattendues :", data); // Affiche un message d'erreur si la structure est incorrecte
        }
    })
    .catch(error => console.error("Erreur lors du chargement des logements :", error));
