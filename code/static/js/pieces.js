
console.log("JavaScript chargé pour la page des pièces !");

// Extraire l'ID du logement depuis l'URL
const urlParams = new URLSearchParams(window.location.search);
const logementId = urlParams.get("logement_id");

if (logementId) {
    // Charger les pièces associées au logement
    fetch(`http://127.0.0.1:8000/piece?logement_id=${logementId}`)
        .then(response => response.json())
        .then(data => {
            console.log("Données récupérées :", data); // Affichez les données récupérées
            if (data.pieces && Array.isArray(data.pieces)) {
                const piecesTable = document.getElementById("piecesTable");
                data.pieces.forEach(piece => {
                    piecesTable.innerHTML += `
                        <tr>
                            <td>${piece.id}</td>
                            <td>${piece.nom}</td>
                            <td>${piece.coordonnees}</td>
                            
                            <td>
                                <button class="btn btn-primary voir-capteurs" data-id="${piece.id}">Voir Capteurs Actionneurs</button>
                            </td>
                        </tr>
                    `;
                });

                // Ajouter des gestionnaires d'événements aux boutons
                const boutonsVoirCapteurs = document.querySelectorAll(".voir-capteurs");
                boutonsVoirCapteurs.forEach(button => {
                    button.addEventListener("click", (event) => {
                        const pieceId = event.target.dataset.id; // Récupère l'ID de la pièce
                        window.location.href = `http://127.0.0.1:8000/capteurs?piece_id=${pieceId}`;
                    });
                });
            } else {
                console.error("Données inattendues :", data); // Affiche un message d'erreur si la structure est incorrecte
            }
        })
        .catch(error => console.error("Erreur lors du chargement des pièces :", error));
} else {
    console.error("Aucun logement_id trouvé dans l'URL !");
}
