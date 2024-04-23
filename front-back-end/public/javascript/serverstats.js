const express = require('express');
const path = require('path');
const { exec } = require('child_process');
const app = express();
const PORT = 3000;

const publicPath = path.join(__dirname, 'stats_page');
console.log(publicPath);

app.use(express.json()); // Middleware to parse JSON bodies
app.use(express.static(publicPath)); // Serve static files from the specified directory

app.get('/', (req, res) => {
    res.sendFile(path.join(publicPath, 'stats.html'));
});

// Handle POST request to fetch data with pagination
app.post('/fetchData', (req, res) => {
    
    const { abbr, seasonYear } = req.body;
    const start = req.query.start || '0'; // Default to '0' if not provided
    const limit = req.query.limit || '5'; // Default to '5' if not provided
    const scriptPath = '/Users/augustalexander/CMS-484-CS_Capstone/python-code/team_stats.py'; // Adjust this to your actual Python script path

    // Command to execute the Python script with parameters
    const command = `python ${scriptPath} ${abbr} ${seasonYear} ${start} ${limit}`;

    exec(command, (error, stdout, stderr) => {
        if (error) {
            console.error(`exec error: ${error}`);
            return res.status(500).send(stderr);
        }
        res.send(stdout); // Send back the result of the Python script
    });
});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
