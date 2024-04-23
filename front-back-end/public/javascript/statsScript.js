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

        console.log(`Fetching data from start: ${start}, limit: ${limit}`); // Debug statement

        fetch(`http://localhost:3000/fetchData?start=${start}&limit=${limit}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ abbr: team, seasonYear: season })
        })
        .then(response => response.json())
        .then(data => {
            console.log("working")
            displayFormattedJson(data, start === 0);
            currentStart += limit; // Increment by the limit, not data.length
            document.getElementById('loadMore').style.display = data.length < limit ? 'none' : 'block'; // Hide if no more data
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
    }


    function displayFormattedJson(data) {
        const resultContainer = document.getElementById('result');
        resultContainer.innerHTML = ''; // Clear previous results

        // data = JSON.parse(data);
    
        // Check if data is not empty and is an array
        if (!data || !data.length) {
            resultContainer.innerHTML = '<p>No data available.</p>';
            return;
        }
    
        // Create table element
        const table = document.createElement('table');
        table.className = 'stats-table'; // Style this class in your CSS for better appearance
    
        // Create and append header row
        const headerRow = document.createElement('tr');
        Object.keys(data[0]).forEach(key => {
            const headerCell = document.createElement('th');
            headerCell.textContent = key;
            headerRow.appendChild(headerCell);
        });
        table.appendChild(headerRow);
    
        console.log("THIS ONE")

        let newData = JSON.parse(data)
        console.log(newData)
        console.log(Array.isArray(newData));


        // console.log(data)
        // console.log(Array.isArray(data));




        // Append data rows
        newData.forEach(item => {
            const row = document.createElement('tr');
            Object.keys(item).forEach(key => {
                const cell = document.createElement('td');
                cell.textContent = item[key];
                row.appendChild(cell);
            });
            table.appendChild(row);
        });
    
        // Append the table to the result container
        resultContainer.appendChild(table);
    }
}