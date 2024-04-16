export function initFormHandling() {
    const form = document.getElementById('predictionForm');
    const resultDiv = document.getElementById('predictionResult');

    let teamSelect1 = '';
    let team1 = '';
    let teamSelect2 = '';
    let team2 = '';

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        // Getting the selected prediction type
        const predictionType = document.querySelector('input[name="predictionType"]:checked').value;

        // Get the selected teams
        teamSelect1 = document.getElementById('teamSelect1');
        team1 = teamSelect1.options[teamSelect1.selectedIndex].value;
        teamSelect2 = document.getElementById('teamSelect2');
        team2 = teamSelect2.options[teamSelect2.selectedIndex].value;

        // Hard coded for all inputs
        const season = '2023-24'
        const num_seasons = '3'
        const num_past_games = '15'
        

        // Create a JSON object for paramsInput
        const paramsInput = {
            predictionType: predictionType,
            team1: team1,                   
            team2: team2,                   
            season: season,
            numSeasons: num_seasons,
            numPastGames: num_past_games
        };

        console.log(paramsInput);

        // Serialize the object to a JSON string
        const paramsInputString = JSON.stringify(paramsInput);
        fetchPrediction(paramsInputString);
    });


    function fetchPrediction(paramsInput) {
        const url = new URL('http://localhost:3000/prediction');
        url.search = new URLSearchParams({params: paramsInput});

        fetch(url)
            .then(response => response.json())
            .then(data => {
                let content = '';

                switch (data.prediction.prediction_type) {
                    case 'gamePrediction':
                        content = `
                            <p>Prediction Outcome: ${data.prediction.prediction_outcome}</p>
                            <p>Probability: ${data.prediction.prediction_probability}</p>
                            <p>Win Probability: ${data.prediction.probabilities.win_probability}</p>
                            <p>Loss Probability: ${data.prediction.probabilities.loss_probability}</p>
                        `;
                        break;
                        
                    case 'statsPrediction':
                        content = `
                            <p>${team1} Predicted Stats:
                            <p>Points: ${data.prediction.estimated_stats.teamA.points}</p>
                            <p>Assists: ${data.prediction.estimated_stats.teamA.assists}</p>
                            <p>Rebounds: ${data.prediction.estimated_stats.teamA.rebounds}</p>

                            <p>${team2} Predicted Stats:
                            <p>Points: ${data.prediction.estimated_stats.teamB.points}</p>
                            <p>Assists: ${data.prediction.estimated_stats.teamB.assists}</p>
                            <p>Rebounds: ${data.prediction.estimated_stats.teamB.rebounds}</p>
                        `;
                        break;
    
                    default:
                        content += `<p>Unknown prediction type.</p>`;
                }

                resultDiv.innerHTML = content;
            })
            .catch(error => {
                console.error('Error:', error);
                resultDiv.innerHTML = `<p>Error fetching prediction: ${error}</p>`;
            });
    }





}
