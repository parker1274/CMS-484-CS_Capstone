import { initFormHandling } from './formHandling.js';
import { initStatsScript } from './statsScript.js';
import { populateTeamSelect, getSelectedTeam } from './teamManagement.js';

document.addEventListener('DOMContentLoaded', function() {
    // Initialize form handling logic
    initFormHandling();

    const radios = document.querySelectorAll('input[type="radio"]');
    let selected_prediction;

    radios.forEach(radio => {
        radio.addEventListener('change', function() {
            selected_prediction = this.id;
            console.log(selected_prediction)
        });
    });

    // Populate dropdowns for teams
    populateTeamSelect('teamSelect1');
    populateTeamSelect('teamSelect2');

    // Setup event listeners for team selections
    const teamSelect1 = document.getElementById('teamSelect1');
    const teamSelect2 = document.getElementById('teamSelect2');


    teamSelect1.addEventListener('change', function() {
        const selectedTeam1 = getSelectedTeam(this);
        console.log('Form 1 selected team:', selectedTeam1);
    });

    teamSelect2.addEventListener('change', function() {
        const selectedTeam2 = getSelectedTeam(this);
        console.log('Form 2 selected team:', selectedTeam2);
    });
});

document.addEventListener('DOMContentLoaded', function() {
    initStatsScript()

    populateTeamSelect('teamSelect3');

    // Setup event listeners for team selections

    const teamSelect3 = document.getElementById('teamSelect3');

    teamSelect3.addEventListener('change', function() {
        const selectedTeam3 = getSelectedTeam(this);
        console.log('Form 3 selected team:', selectedTeam3);
    });
});