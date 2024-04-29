export function initFormHandling() {
    const form = document.getElementById('predictionForm');
    const resultDiv = document.getElementById('predictionResult');

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        let errors = [];

        let predictionType;
        try {
            predictionType = document.querySelector('input[name="predictionType"]:checked').value;
        } catch (error) {
            errors.push("Please select a prediction type.");
        }

        const teamSelect1 = document.getElementById('teamSelect1');
        const team1 = teamSelect1.options[teamSelect1.selectedIndex].value;
        if (!team1 || team1 === "Select Team") {
            errors.push("Please select the first team.");
        }

        const teamSelect2 = document.getElementById('teamSelect2');
        const team2 = teamSelect2.options[teamSelect2.selectedIndex].value;
        if (!team2 || team2 === "Select Team") {
            errors.push("Please select the second team.");
        }

        if (errors.length > 0) {
            resultDiv.innerHTML = `<p>${errors.join('<br>')}</p>`;
            return;
        }

        const season = '2023-24';
        const num_seasons = '3';
        const num_past_games = '15';
        const paramsInput = {
            predictionType: predictionType,
            team1: team1,
            team2: team2,
            season: season,
            numSeasons: num_seasons,
            numPastGames: num_past_games
        };

        const paramsInputString = JSON.stringify(paramsInput);

        // Set loading message
        resultDiv.innerHTML = '<p>Loading prediction results...</p>';

        fetchPrediction(paramsInputString, team1, team2);
    });

    function fetchPrediction(paramsInputString, team1, team2) {
        const url = 'https://qr7cldaha9.execute-api.us-east-1.amazonaws.com/';

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(paramsInputString)
        })
        .then(response => response.json())
        .then(data => {
            resultDiv.innerHTML = buildContent(data, team1, team2);
        })
        .catch(error => {
            console.error('Error:', error);
            resultDiv.innerHTML = '<p>Error fetching prediction.</p>';
        });
    }

    function buildContent(data, team1, team2) {
        let content = '<div class="prediction-results">';
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
        return content;
    }
}

