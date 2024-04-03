const express = require('express');
const cors = require('cors');
const { predictionRequest } = require('./pythonCaller');

const app = express();
app.use(cors());

app.get('/prediction', async (req, res) => {
    try {
        const predictionValue = await predictionRequest();
        console.log("Backend sending:", predictionValue); // Add this line

        res.json(predictionValue);
    } catch (error) {
        console.error(error);
        res.status(500).send('Server error');
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
