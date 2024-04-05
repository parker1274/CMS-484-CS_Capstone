const express = require('express');
const cors = require('cors');
const app = express();
app.use(cors()); // Enable CORS
app.use(express.json()); // Middleware to parse JSON bodies

app.get('/example', (req, res) => {
    res.json({ message: "This is data from the backend." });
});




// JS functions to process the users requests -------------------------

// Outcome prediction function
const { predictionRequest } = require('./python-request');

// Actionable data function
// const { actionableDataRequest } = require();

// 




app.get('/prediction', async (req, res) => {
    console.log("Prediction endpoint hit", req.query);

    try {
        const predictionArgs = req.query.params ? JSON.parse(req.query.params) : ['Game Outcome', 'BOS', 'NYK', '2023-24', '3', '14'];

        console.log()

        const prediction = await predictionRequest(predictionArgs);

        console.log("Prediction values (server): ")
        console.log(prediction);

        res.json({ prediction });
    } catch (error) {
        res.status(500).json({ error: error.message });
        console.log("Error!")
    }
});

// app.get('/actionable-data', async (req, res) => {
//     console.log("Actionable-data endpoint hit", req.query);

//     try {
//         actionableArgs = JSON.parse(req.query.params);

//         console.log()

//         const actionableData = await predictionRequest(predictionArgs);

//         console.log("Prediction values (server): ")
//         console.log(prediction);

//         res.json({ prediction });
//     } catch (error) {
//         res.status(500).json({ error: error.message });
//         console.log("Error!")
//     }
// });





const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));