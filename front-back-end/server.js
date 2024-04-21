const express = require('express');
const path = require('path');
const cors = require('cors');
const app = express();
app.use(cors()); // Enable CORS
app.use(express.json()); // Middleware to parse JSON bodies

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));


// Set up routes for each HTML file
app.get('/predictions', (req, res) => {
    res.sendFile(__dirname + '/public/predictions.html');
});

app.get('/stats', (req, res) => {
    res.sendFile(__dirname + '/public/stats.html');
});

app.get('/about', (req, res) => {
    res.sendFile(__dirname + '/public/about.html');
});




// JS functions to process the users requests -------------------------

// Import outcome prediction function
const { predictionRequest } = require('./python-request');

// Import actionable data function
const { actionableDataRequest } = require('./python-request');

// Import team performance insight (tpi) function
const { tpiRequest } = require('./python-request');




// Prediction function call
app.get('/prediction', async (req, res) => {
    console.log("Prediction endpoint hit", req.query);
    console.log(JSON.parse(req.query.params));

    try {
        const predictionArgs = JSON.parse(req.query.params);

        console.log()

        const prediction = await predictionRequest(predictionArgs);

        console.log("Prediction values (server): ")
        console.log(prediction);

        res.json({ prediction });
    } catch (error) {
        res.status(500).json({ error: error.message });
        console.log("Error relating to prediction function call on the server")
    }
});

// Actionable data function call
app.get('/actionable-data', async (req, res) => {
    console.log("Actionable-data endpoint hit", req.query);

    try {
        actionableArgs = JSON.parse(req.query.params);

        console.log()

        const actionableData = await actionableDataRequest(actionableArgs);

        console.log("Actionable data values (server): ")
        console.log(actionableData);

        res.json({ actionableData });
    } catch (error) {
        res.status(500).json({ error: error.message });
        console.log("Error relating to actionable data function call on the server")
    }
});

// Team Performance Insight function call
app.get('/team-performance-insight', async (req, res) => {
    console.log("TPI endpoint hit", req.query);

    try {
        tpiArgs = JSON.parse(req.query.params);

        console.log()

        const tpiData = await tpiRequest(actionableArgs);

        console.log("TPI values (server): ")
        console.log(tpiData);

        res.json({ tpiData });
    } catch (error) {
        res.status(500).json({ error: error.message });
        console.log("Error relating to TPI function call on the server")
    }
});



const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));