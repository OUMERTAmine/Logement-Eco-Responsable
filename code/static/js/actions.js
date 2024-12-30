const params = new URLSearchParams(window.location.search);
const capteurId = params.get("capteur_id");

fetch(`http://127.0.0.1:8000/actions-capteur/${capteurId}`)
    .then(response => response.json())
    .then(data => {
        console.log("Données récupérées :", data);
        const actionsTable = document.getElementById("actionsTable");

        // Ajout des données dans le tableau
        data.actions.forEach(action => {
            actionsTable.innerHTML += `
                <tr>
                    <td>${action.id}</td>
                    <td>${action.type_action}</td>
                    <td>${action.date_insertion}</td>
                </tr>
            `;
        });
    })
    .catch(error => console.error("Erreur lors du chargement des actions :", error));
