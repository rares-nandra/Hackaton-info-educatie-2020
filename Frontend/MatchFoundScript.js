var UsernameElement = document.getElementById("Username")
var AgeElement = document.getElementById("Age")
var InstagramElement = document.getElementById("Instagram")
var ButtonElement = document.getElementById("MatchingButton")

var UserUsername = "Lmao Androginescu"
var UserAge = "69"
var UserInstagram = "nandra._.rares"

var UsernameElementTwo = document.getElementById("UsernameTwo")
var AgeElementTwo = document.getElementById("AgeTwo")
var InstagramElementTwo = document.getElementById("InstagramTwo")
var ButtonElementTwo = document.getElementById("MatchingButtonTwo")

var MatchUsername = "Lmao Androgineasca"
var MatchAge = "56"
var MatchInstagram = "tudyftw"

var InstagramLink = "https://www.instagram.com/" + String(UserInstagram) + "/"
var InstagramLinkMatch = "https://www.instagram.com/" + String(MatchInstagram) + "/"

var ScoreElement = document.getElementById("Scor")
var Score = "Scor compatibilitate: 10"

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