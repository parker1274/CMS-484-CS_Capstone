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
const { statsRequest } = require('./python-request');




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

const { exec } = require('child_process');
 
// Handle POST request to fetch data with pagination
app.post('/fetchData', (req, res) => {
    
    const { abbr, seasonYear } = req.body;
    const start = req.query.start || '0'; // Default to '0' if not provided
    const limit = req.query.limit || '5'; // Default to '5' if not provided
    const scriptPath = '/Users/jkran/code/school/CMS-484-CS_Capstone/python-code/team_stats.py'; // Adjust this to your actual Python script path

    // Command to execute the Python script with parameters
    const command = `python3 ${scriptPath} ${abbr} ${seasonYear} ${start} ${limit}`;

    exec(command, (error, stdout, stderr) => {
        if (error) {
            console.error(`exec error: ${error}`);
            return res.status(500).send(stderr);
        }

        formatOutput = JSON.stringify(stdout)
        // console.log("Server output")
        // console.log(formatOutput)
        res.send(formatOutput); // Send back the result of the Python script
    });
});

// // Handle POST request to fetch data with pagination
// app.post('/stats/fetchData', async (req, res) => {
//     console.log("Stats endpoint hit", req.body);

//     // console.log(JSON.parse(req.query));

//     try {
//         console.log("Working")

//         const statsQuery = JSON.parse(req.query.start);
//         const statsParams = JSON.parse(req.body)

//         const statArgs = { ...statsQuery, ...statsParams };

//         console.log(statArgs);


//         console.log();

//         const stats = await statsRequest(statArgs);

//         console.log("Stat values (server): ")
//         console.log(stats);

//         res.json({ stats });
//     } catch (error) {
//         res.status(500).json({ error: error.message });
//         console.log("Error relating to stat function call on the server")
//     }
// });

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));