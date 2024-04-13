document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('predictionForm');
    const resultDiv = document.getElementById('predictionResult');

    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent form from submitting the traditional way

        const paramsInput = document.getElementById('params').value;

        console.log(paramsInput)
        fetchPrediction(paramsInput);
    });

    function fetchPrediction(paramsInput) {
        // Construct the URL with query parameters
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
});


document.addEventListener('DOMContentLoaded', function() {
  const radios = document.querySelectorAll('input[type="radio"]');
  radios.forEach(radio => {
    radio.addEventListener('change', function() {
        selected_prediction = this.value;
        console.log(selected_prediction)
    });
  });
});


