document.addEventListener('DOMContentLoaded', function() {
    const fetchBtn = document.getElementById('fetchPrediction');
    const resultDiv = document.getElementById('predictionResult');

    fetchBtn.addEventListener('click', function() {
        resultDiv.textContent = 'Loading...';

        fetch('http://localhost:3000/prediction')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.prediction !== undefined) {
                    resultDiv.textContent = `Prediction: ${data.prediction}, Probability: ${data.probability}, Team: ${data.team}`;
                } else {
                    throw new Error('Prediction data is missing');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                resultDiv.textContent = 'Failed to fetch prediction.';
            });
    });
});


