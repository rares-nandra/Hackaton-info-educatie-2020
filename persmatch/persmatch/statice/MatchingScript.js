var xhttp = new XMLHttpRequest(); 
const urlParams = new URLSearchParams(window.location.search);
const ids = urlParams.get('ids'); //id_sesiune fetched



function functie() {
    setTimeout(20000);
    window.location.replace("/matchfound?ids=" + ids);

}

functie();