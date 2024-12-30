console.log("JavaScript chargé pour la page des capteurs !");

// Extraire l'ID de la pièce depuis l'URL
const urlParams = new URLSearchParams(window.location.search);
const pieceId = urlParams.get("piece_id");

if (pieceId) {
    // Charger les capteurs actionneurs associés à la pièce
    fetch(`http://127.0.0.1:8000/capteur-actionneur-pieces?piece_id=${pieceId}`)
        .then(response => response.json())
        .then(data => {
            console.log("Données récupérées :", data); // Affichez les données récupérées
            if (data.capteurs && Array.isArray(data.capteurs)) {
                const capteursTable = document.getElementById("capteursTable");
                data.capteurs.forEach(capteur => {
                    capteursTable.innerHTML += `
                        <tr>
                            <td>${capteur.id}</td>
                            <td>${capteur.type}</td>
                            <td>${capteur.reference}</td>
                            <td>${capteur.port}</td>
                            <td>${capteur.date_insertion}</td>
                            <button class="btn btn-primary voir-mesures" data-id="${capteur.id}">Voir Mesures</button>
                            <button class="btn btn-primary voir-actions" data-id="${capteur.id}">Voir Actions</button>
                        </tr>
                    `;
                });
                
                document.addEventListener("click", event => {
                    if (event.target && event.target.classList.contains("voir-mesures")) {
                        const capteurId = event.target.getAttribute("data-id");
                        window.location.href = `http://127.0.0.1:8000/mesures?capteur_id=${capteurId}`;
                    }
                });

                document.addEventListener("click", event => {
                    if (event.target && event.target.classList.contains("voir-actions")) {
                        const capteurId = event.target.getAttribute("data-id");
                        window.location.href = `http://127.0.0.1:8000/actions-web?capteur_id=${capteurId}`;
                    }
                });
                
                

            } else {
                console.error("Données inattendues :", data); // Affiche un message d'erreur si la structure est incorrecte
            }
        })
        .catch(error => console.error("Erreur lors du chargement des capteurs actionneurs :", error));
} else {
    console.error("Aucun piece_id trouvé dans l'URL !");
}
