var UsernameElement = document.getElementById("Username")
var AgeElement = document.getElementById("Age")
var InstagramElement = document.getElementById("Instagram")
var ButtonElement = document.getElementById("MatchingButton")
var xmlhttp = new XMLHttpRequest(); 
const urlParams = new URLSearchParams(window.location.search);
const ids = urlParams.get('ids'); //id_sesiune fetched
var myArr = "f";

xmlhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        myArr = JSON.parse(this.responseText);
    }
};
xmlhttp.open("GET", "/searchmatch?ids=" + ids , true);
xmlhttp.send();

document.getElementById('ProfileImage').src=("avatar?ids=" + ids)
// document.getElementById('ProfileImageTwo').src=("avatar?ids=" + myArr["otherIDS"])

var UserUsername = myArr["myUser"]
var UserAge = myArr[""]
var UserInstagram = "nandra._.rares"

var UsernameElementTwo = document.getElementById("UsernameTwo")
var AgeElementTwo = document.getElementById("AgeTwo")
var InstagramElementTwo = document.getElementById("InstagramTwo")
var ButtonElementTwo = document.getElementById("MatchingButtonTwo")

var MatchUsername = "tuddyftw"
var MatchAge = "16"
var MatchInstagram = "tuddyftw"

var InstagramLink = "https://www.instagram.com/" + String(UserInstagram) + "/"
var InstagramLinkMatch = "https://www.instagram.com/" + String(MatchInstagram) + "/"

var ScoreElement = document.getElementById("Scor")
var Score = "Scor compatibilitate: " + myArr["score"]

UsernameElement.textContent = UserUsername;
AgeElement.textContent = UserAge;
InstagramElement.textContent = UserInstagram;
InstagramElement.setAttribute('href', InstagramLink);

UsernameElementTwo.textContent = MatchUsername;
AgeElementTwo.textContent = MatchAge;
InstagramElementTwo.textContent = MatchInstagram;
InstagramElementTwo.setAttribute('href', InstagramLinkMatch);

ScoreElement.textContent = Score;

ButtonElement.setAttribute("href", InstagramLinkMatch)