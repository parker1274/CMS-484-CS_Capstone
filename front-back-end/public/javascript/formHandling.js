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
                let content = '<div class="prediction-results">';
                console.log(data.prediction)

                switch (data.prediction.prediction_type) {
                    case 'gamePrediction':
                        content += `
                            <h2>Game Prediction</h2>
                            <p><strong>Prediction Outcome:</strong> ${data.prediction.prediction_outcome}</p>
                            <p><strong>Probability:</strong> ${data.prediction.prediction_probability}</p>
                            <p><strong>Win Probability:</strong> ${data.prediction.probabilities.win_probability}</p>
                            <p><strong>Loss Probability:</strong> ${data.prediction.probabilities.loss_probability}</p>
                        `;
                        break;
                        
                    case 'statsPrediction':
                        content += `
                            <h2>Stats Prediction</h2>
                            <div class="team-stats">
                                <h3>${team1} Predicted Stats:</h3>
                                <p>Points: ${data.prediction.estimated_stats.teamA.points}</p>
                                <p>Assists: ${data.prediction.estimated_stats.teamA.assists}</p>
                                <p>Rebounds: ${data.prediction.estimated_stats.teamA.rebounds}</p>
                            </div>
                            <div class="team-stats">
                                <h3>${team2} Predicted Stats:</h3>
                                <p>Points: ${data.prediction.estimated_stats.teamB.points}</p>
                                <p>Assists: ${data.prediction.estimated_stats.teamB.assists}</p>
                                <p>Rebounds: ${data.prediction.estimated_stats.teamB.rebounds}</p>
                            </div>
                        `;
                        break;

                    case 'controllablesPrediction':
                        content += `<h2>Controllables Prediction</h2>`;
                        content += `<div class="team-strategies"><h3>${team1} Strategies:</h3>`;
                        data.prediction.team_strategies.strategies.forEach(strategy => {
                            content += `<p>${strategy.feature} ${strategy.operator} ${strategy.threshold}</p>`;
                        });
                        content += `</div>`;
                        content += `<div class="team-strategies"><h3>${team2} Strategies:</h3>`;
                        data.prediction.opponent_strategies.strategies.forEach(strategy => {
                            content += `<p>${strategy.feature} ${strategy.operator} ${strategy.threshold}</p>`;
                        });
                        content += `</div>`;
                        break;

                    default:
                        content += `<p>Unknown prediction type.</p>`;
                }

                content += '</div>';
                resultDiv.innerHTML = content;
            })
            .catch(error => {
                console.error('Error:', error);
                resultDiv.innerHTML = `<p>Error fetching prediction: ${error}</p>`;
            });
    }
}

