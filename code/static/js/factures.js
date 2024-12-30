console.log("JavaScript chargé pour la page des factures !");

// Extraire l'ID du logement depuis l'URL
const urlParams = new URLSearchParams(window.location.search);
const logementId = urlParams.get("logement_id");

if (logementId) {
    // Charger les factures associées au logement
    fetch(`http://127.0.0.1:8000/factures-logement?logement_id=${logementId}`)
        .then(response => response.json())
        .then(data => {
            console.log("Données récupérées :", data); // Affichez les données récupérées
            if (Array.isArray(data)) {
                const facturesTable = document.getElementById("facturesTable");
                data.forEach(facture => {
                    facturesTable.innerHTML += `
                        <tr>
                            <td>${facture.id}</td>
                            <td>${facture.type}</td>
                            <td>${facture.date}</td>
                            <td>${facture.montant.toFixed(2)} €</td>
                            <td>${facture.valeur_consomme.toFixed(2)}</td>
                        </tr>
                    `;
                });
            } else {
                console.error("Données inattendues :", data); // Affiche un message d'erreur si la structure est incorrecte
            }
        })
        .catch(error => console.error("Erreur lors du chargement des factures :", error));
} else {
    console.error("Aucun logement_id trouvé dans l'URL !");
}
