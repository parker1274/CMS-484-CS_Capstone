// Define an array of NBA teams
const teams = [
    { value: "ATL", name: "Atlanta Hawks" },
    { value: "BOS", name: "Boston Celtics" },
    { value: "BKN", name: "Brooklyn Nets" },
    { value: "CHA", name: "Charlotte Hornets" },
    { value: "CHI", name: "Chicago Bulls" },
    { value: "CLE", name: "Cleveland Cavaliers" },
    { value: "DAL", name: "Dallas Mavericks" },
    { value: "DEN", name: "Denver Nuggets" },
    { value: "DET", name: "Detroit Pistons" },
    { value: "GSW", name: "Golden State Warriors" },
    { value: "HOU", name: "Houston Rockets" },
    { value: "IND", name: "Indiana Pacers" },
    { value: "LAC", name: "LA Clippers" },
    { value: "LAL", name: "Los Angeles Lakers" },
    { value: "MEM", name: "Memphis Grizzlies" },
    { value: "MIA", name: "Miami Heat" },
    { value: "MIL", name: "Milwaukee Bucks" },
    { value: "MIN", name: "Minnesota Timberwolves" },
    { value: "NOP", name: "New Orleans Pelicans" },
    { value: "NYK", name: "New York Knicks" },
    { value: "OKC", name: "Oklahoma City Thunder" },
    { value: "ORL", name: "Orlando Magic" },
    { value: "PHI", name: "Philadelphia 76ers" },
    { value: "PHX", name: "Phoenix Suns" },
    { value: "POR", name: "Portland Trail Blazers" },
    { value: "SAC", name: "Sacramento Kings" },
    { value: "SAS", name: "San Antonio Spurs" },
    { value: "TOR", name: "Toronto Raptors" },
    { value: "UTA", name: "Utah Jazz" },
    { value: "WAS", name: "Washington Wizards" }
];


// Function to add teams to a select element
export function populateTeamSelect(selectId) {
    const select = document.getElementById(selectId);
    // Create and add the placeholder option
    const placeholderOption = document.createElement('option');
    placeholderOption.textContent = 'Select a team';
    placeholderOption.value = '';
    placeholderOption.disabled = true;
    placeholderOption.selected = true;
    select.appendChild(placeholderOption);

    // Add team options from the array
    teams.forEach(team => {
        const option = document.createElement('option');
        option.value = team.value;
        option.textContent = team.name;
        select.appendChild(option);
    });
}

// Function to retrieve selected team from form
export function getSelectedTeam(selectElement) {
    const selectedOption = selectElement.options[selectElement.selectedIndex];
    const selectedTeam = {
        value: selectedOption.value,
        name: selectedOption.textContent
    };
    return selectedTeam;
}