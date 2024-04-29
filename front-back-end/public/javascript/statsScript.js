export function initStatsScript() {
    const start = 0;
    let limit = 5; // Adjust the number of records per fetch based on your preference

    document.getElementById('fetchStats').addEventListener('click', function() {
        //start = 0; // Reset start here for a fresh fetch
        fetchData(start, limit);
    });

    document.getElementById('loadMore').addEventListener('click', function() {
        limit += 5; // Increase the limit here for the next fetch   
        fetchData(start, limit);
    });

    function fetchData(start, limit) {
        const team = document.getElementById('teamSelect3').value;
        const season = document.getElementById('seasonSelect').value;
    
        fetch(`http://localhost:3000/fetchData?start=${start}&limit=${limit}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ abbr: team, seasonYear: season })
        })
        .then(response => {
            return response.text();  // First, get the response as text
        })
        .then(text => {
            console.log("Received text:", text);  // Log the raw text
            return JSON.parse(text);  // Then parse it as JSON
        })
        .then(data => {
            displayFormattedJson(data, start === 0);
            document.getElementById('loadMore').style.display = data.length < limit ? 'none' : 'block';
        })
        .catch(error => {
            console.error('Error parsing JSON data:', error);
        });
    }
    
}

    


function displayFormattedJson(data, isInitialLoad) {
    const resultContainer = document.getElementById('result');
    const excludeColumns = ['SEASON_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 'GAME_ID'];

    let table = resultContainer.querySelector('.table');


    if (typeof data === 'string') {
        try {
            data = JSON.parse(data);
        } catch (error) {
            resultContainer.innerHTML = `<p>Error parsing JSON data: ${error.message}</p>`;
            return;
        }
    }

    // If it's the first load or no table exists, create a new table and headers
    if (isInitialLoad || !table) {
        resultContainer.innerHTML = '';  // Clear previous results if it's the initial load
        table = document.createElement('table');
        table.className = 'table table-striped table-bordered table-hover';
        resultContainer.appendChild(table);

        const headerRow = document.createElement('tr');
        if (data.length > 0) {
            Object.keys(data[0]).forEach(key => {
                if (!excludeColumns.includes(key)) {
                    const headerCell = document.createElement('th');
                    headerCell.textContent = key;
                    headerRow.appendChild(headerCell);
                }
            });
            table.appendChild(headerRow);
        }
    }

    // Append new data rows to the existing table
    data.forEach(item => {
        const row = document.createElement('tr');
        Object.keys(item).forEach(key => {
            if (!excludeColumns.includes(key)) {
                const cell = document.createElement('td');
                cell.textContent = item[key];
                row.appendChild(cell);
            }
        });
        table.appendChild(row);
    });
}
