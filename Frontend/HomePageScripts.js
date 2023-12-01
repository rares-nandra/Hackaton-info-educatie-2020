var UsernameElement = document.getElementById("Username")
var AgeElement = document.getElementById("Age")
var InstagramElement = document.getElementById("Instagram")
var ButtonElement = document.getElementById("MatchingButton")

var UserUsername = "Lmao Androginescu"
var UserAge = "69"
var UserInstagram = "nandra._.rares"

var InstagramLink = "https://www.instagram.com/" + String(UserInstagram) + "/"

var MatchState = "false" // true daca e matched false daca trb sa caute match

if(MatchState == "true")
{
    var UsernameMatch = "user la gagica"
    var ButtonMatch = "Continua conversatia cu " + String(UsernameMatch)
    var RedirectLink = "chat.html"
}
else
{
    var ButtonMatch = "Cauta Match"
    var RedirectLink = "matching.html"
}

UsernameElement.textContent = UserUsername;
AgeElement.textContent = UserAge;
InstagramElement.textContent = UserInstagram;
InstagramElement.setAttribute('href', InstagramLink);
ButtonElement.textContent = ButtonMatch;
ButtonElement.setAttribute("href", RedirectLink)