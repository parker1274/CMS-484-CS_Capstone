export function initFormHandling() {
    const form = document.getElementById('predictionForm');
    const resultDiv = document.getElementById('predictionResult');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        // Getting the selected prediction type
        const predictionType = document.querySelector('input[name="predictionType"]:checked').id;

        // Get the selected teams
        const teamSelect1 = document.getElementById('teamSelect1');
        const team1 = teamSelect1.options[teamSelect1.selectedIndex].value;
        const teamSelect2 = document.getElementById('teamSelect2');
        const team2 = teamSelect2.options[teamSelect2.selectedIndex].value;

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
                const content = `
                    <p>Prediction Outcome: ${data.prediction.prediction_outcome}</p>
                    <p>Probability: ${data.prediction.prediction_probability}</p>
                    <p>Win Probability: ${data.prediction.probabilities.win_probability}</p>
                    <p>Loss Probability: ${data.prediction.probabilities.loss_probability}</p>
                `;
                resultDiv.innerHTML = content;
            })
            .catch(error => {
                console.error('Error:', error);
                resultDiv.innerHTML = `<p>Error fetching prediction: ${error}</p>`;
            });
    }





}
