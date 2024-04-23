export function initStatsScript() {
    let currentStart = 0;
    const limit = 5; // You can adjust the number of records per fetch based on your preference

    document.getElementById('fetchStats').addEventListener('click', function() {
        //currentStart = 0; // Explicitly reset start here
        fetchData(currentStart, limit); // Use the reset start
    });

    document.getElementById('loadMore').addEventListener('click', function() {
        fetchData(currentStart, limit);
    });

    function fetchData(start, limit) {
        const team = document.getElementById('teamSelect3').value;
        const season = document.getElementById('seasonSelect').value;

        console.log(`Fetching data from start: ${start}, limit: ${limit}`); // Debug statemen

        fetch(`http://localhost:3000/stats/fetchData?start=${start}&limit=${limit}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ abbr: team, seasonYear: season })
        })
        .then(response => response.json())
        .then(data => {
            console.log("data below")
            console.log(data)
            displayFormattedJson(data, start === 0);
            currentStart += limit; // Increment by the limit, not data.length
            document.getElementById('loadMore').style.display = data.length < limit ? 'none' : 'block'; // Hide if no more data
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
    }


    function displayFormattedJson(data, clearTable) {
        const resultContainer = document.getElementById('result');
        if (clearTable) {
            resultContainer.innerHTML = '';
            if (currentStart === 0) // Only reset if initial fetch
                currentStart = 0; // Reset start index
        }

        // Append the new data as rows in the existing table or create a new one if none exists
        const existingTable = resultContainer.querySelector('table');
        const table = existingTable || document.createElement('table');
        table.className = 'stats-table';

        if (!existingTable) {
            // Create and append header row if table doesn't exist
            const headerRow = document.createElement('tr');
            Object.keys(data[0]).forEach(key => {
                const headerCell = document.createElement('th');
                headerCell.textContent = key;
                headerRow.appendChild(headerCell);
            });
            table.appendChild(headerRow);
        }

        // Append data rows
        data.forEach(item => {
            const row = document.createElement('tr');
            Object.keys(item).forEach(key => {
                const cell = document.createElement('td');
                cell.textContent = item[key];
                row.appendChild(cell);
            });
            table.appendChild(row);
        });

        if (!existingTable) {
            resultContainer.appendChild(table); // Append only if new table was created
        }
    }
}