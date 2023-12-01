from collections import Counter
from imdb import IMDb as MovieAPI
import spotipy.util as util
import spotipy

###############################################################

def GetUserToken(Username, RedirectLink):
    Scope = "user-top-read"
    ClientID = 'f33ea24085634624b58c3622dedf563c'
    ClientSecret = 'af327494a245416baeb06580cf584350'
    RedirectURL = 'https://dexter0-0.github.io/'

    File = open("RedirectLink.txt", "w+")
    File.write(RedirectLink)
    File.close()

    Spotify = spotipy.Spotify(auth=util.prompt_for_user_token(Username, Scope, ClientID, ClientSecret, RedirectURL))
    return Spotify


def GetMusicCompatibility(SpotifyUserOne, SpotifyUserTwo):
    MusicScore = 0
    GenresOne = ""
    GenresTwo = ""
    TopArtistsOne = SpotifyUserOne.current_user_top_artists()
    TopArtistsTwo = SpotifyUserTwo.current_user_top_artists()

    for i in range(len(TopArtistsOne)):
        for j in range(len(TopArtistsOne["items"][i]["genres"])):
            GenresOne = GenresOne + TopArtistsOne["items"][i]["genres"][j] + ","

    for i in range(len(TopArtistsTwo)):
        for j in range(len(TopArtistsTwo["items"][i]["genres"])):
            GenresTwo = GenresTwo + TopArtistsTwo["items"][i]["genres"][j] + ","

    GenresOne = GenresOne.split(",")
    GenresTwo = GenresTwo.split(",")

    for i in range(len(GenresOne)):
        for j in range(len(GenresTwo)):
            if GenresOne[i] == GenresTwo[j]:
                MusicScore = MusicScore + 1

    MusicScore = MusicScore / max(len(GenresOne), len(GenresTwo))
    return MusicScore

###############################################################

def GetMovieCompatibility(MoviesUserOne, MoviesUserTwo):
    MovieScore = 0
    GenresOne = ""
    GenresTwo = ""

    for i in range(len(MoviesUserOne)):
        MovieID = MovieAPI().search_movie(MoviesUserOne[i])[0].movieID
        GenresMovie = MovieAPI().get_movie(MovieID)["genres"]
        for j in range(len(GenresMovie)):
            GenresOne = GenresOne + GenresMovie[j] + ","

    for i in range(len(MoviesUserTwo)):
        MovieID = MovieAPI().search_movie(MoviesUserTwo[i])[0].movieID
        GenresMovie = MovieAPI().get_movie(MovieID)["genres"]
        for j in range(len(GenresMovie)):
            GenresTwo = GenresTwo + GenresMovie[j] + ","

    GenresOne = GenresOne.split(",")
    GenresTwo = GenresTwo.split(",")

    for i in range(len(GenresOne)):
        for j in range(len(GenresTwo)):
            if GenresOne[i] == GenresTwo[j]:
                MovieScore = MovieScore + 1

    MovieScore = MovieScore / max(len(GenresOne), len(GenresTwo))
    return MovieScore

###############################################################

def GetHobbyCompatibility(HobbiesOne, HobbiesTwo):
    HobbyScore = 0

    for i in range(len(HobbiesOne)):
        for j in range(len(HobbiesTwo)):
            if HobbiesOne[i].lower() == HobbiesTwo[j].lower():
                HobbyScore = HobbyScore + 1.5

    return HobbyScore

###############################################################

def GetPersonalityTypeMatch(PersonalityTypeOne, PersonalityTypeTwo):
    PersonalityScore = 0

    if PersonalityTypeOne == PersonalityTypeTwo:
        PersonalityScore = PersonalityScore + 1

    OppositePersonality = True

    for i in range(len(PersonalityTypeOne)):
        if PersonalityTypeOne[i] == PersonalityTypeTwo[i]:
            OppositePersonality = False

    if OppositePersonality is True:
        PersonalityScore = PersonalityScore + 1

    # INTJ
    if PersonalityTypeOne == "INTJ":
        if "N" in PersonalityTypeTwo:
            PersonalityScore = PersonalityScore + 1
        if "E" in PersonalityTypeTwo or PersonalityTypeTwo == "INTP":
            PersonalityScore = PersonalityScore + 1
        if "P" in PersonalityTypeTwo:
            PersonalityScore = PersonalityScore + 1

    # INTP
    if PersonalityTypeOne == "INTP":
        if "NT" in PersonalityTypeTwo:
            PersonalityScore = PersonalityScore + 1
        if "E" in PersonalityTypeTwo or PersonalityTypeTwo == "INTJ" or PersonalityTypeTwo == "INFP":
            PersonalityScore = PersonalityScore + 1
        if "FP" in PersonalityTypeTwo:
            PersonalityScore = PersonalityScore + 1
        if "IN" in PersonalityTypeTwo:
            PersonalityScore = PersonalityScore + 1

    # ENTJ
    if PersonalityTypeOne == "ENTJ":
        if "TP" in PersonalityTypeTwo:
            PersonalityScore = PersonalityScore + 1
        if "I" in PersonalityTypeTwo:
            PersonalityScore = PersonalityScore + 1
        if PersonalityTypeTwo == "ISFJ":
            PersonalityScore = PersonalityScore + 1

    # ENTP
    if PersonalityTypeOne == "ENTP":
        if "IN" in PersonalityTypeTwo:
            PersonalityScore = PersonalityScore + 1
        if PersonalityTypeTwo == "ISFJ" or PersonalityTypeTwo == "ESFJ":
            PersonalityScore = PersonalityScore + 1
        if "SP" in PersonalityTypeTwo:
            PersonalityScore = PersonalityScore + 1
        if "N" in PersonalityTypeTwo:
            PersonalityScore = PersonalityScore + 1

    # INFJ
    if PersonalityTypeOne == "INFJ":
        if PersonalityTypeTwo == "ENTP" or PersonalityTypeTwo == "ENFP":
            PersonalityScore = PersonalityScore + 1
        if "ESF" in PersonalityTypeTwo:
            PersonalityScore = PersonalityScore + 1
        if "N" in PersonalityTypeTwo:
            PersonalityScore = PersonalityScore + 1

    # INFP
    if PersonalityTypeOne == "INFP":
        if PersonalityTypeTwo == "ENFJ" or PersonalityTypeTwo == "ESFJ":
            PersonalityScore = PersonalityScore + 1
        if PersonalityTypeTwo == "ENTJ":
            PersonalityScore = PersonalityScore + 1
        if PersonalityTypeTwo == "INFJ" or PersonalityTypeTwo == "ISFP":
            PersonalityScore = PersonalityScore + 1

    # ENFJ
    if PersonalityTypeOne == "ENFJ":
        if "INF" in PersonalityTypeTwo:
            PersonalityScore = PersonalityScore + 1
        if "NFP" in PersonalityTypeTwo:
            PersonalityScore = PersonalityScore + 1

    # ENFP
    if PersonalityTypeOne == "ENFP":
        if PersonalityTypeOne == "INTJ" or PersonalityTypeTwo == "INFJ":
            PersonalityScore = PersonalityScore + 1
        if "S" in PersonalityTypeTwo:
            PersonalityScore = PersonalityScore + 1
        if "NJ" in PersonalityTypeTwo:
            PersonalityScore = PersonalityScore + 1

    # ISTJ
    if PersonalityTypeOne == "ISTJ":
        if PersonalityTypeTwo == "ESFP" or PersonalityTypeTwo == "ESTP":
            PersonalityScore = PersonalityScore + 1
        if "E" in PersonalityTypeTwo:
            PersonalityScore = PersonalityScore + 1
        if "S" in PersonalityTypeTwo:
            PersonalityScore = PersonalityScore + 1

    # ISFJ
    if PersonalityTypeOne == "ISFJ":
        if PersonalityTypeTwo == "ENTJ" or PersonalityTypeTwo == "ESPF" or PersonalityTypeTwo == "ESTP":
            PersonalityScore = PersonalityScore + 1
        if "E" in PersonalityTypeTwo:
            PersonalityScore = PersonalityScore + 1
        if "IS" in PersonalityTypeTwo:
            PersonalityScore = PersonalityScore + 1

    # ESTJ
    if PersonalityTypeOne == "ESTJ":
        if PersonalityTypeTwo == "ISTP" or PersonalityTypeTwo == "INTP" or PersonalityTypeTwo == "ISFP":
            PersonalityScore = PersonalityScore + 1
        if "I" in PersonalityTypeTwo:
            PersonalityScore = PersonalityScore + 1

    # ESFJ
    if PersonalityTypeOne == "ESFJ":
        if PersonalityTypeTwo == "ISTJ" or PersonalityTypeTwo == "ESTJ":
            PersonalityScore = PersonalityScore + 1
        if "TP" in PersonalityTypeTwo:
            PersonalityScore = PersonalityScore + 1

    # ISTP
    if PersonalityTypeOne == "ISTP":
        if PersonalityTypeTwo == "ESFJ"	or PersonalityTypeTwo == "ISTJ":
            PersonalityScore = PersonalityScore + 1
        if PersonalityTypeTwo == "ISFJ" or PersonalityTypeTwo == "INTP":
            PersonalityScore = PersonalityScore + 1
        if PersonalityTypeTwo == "ESTJ" or PersonalityTypeTwo == "ESFP":
            PersonalityScore = PersonalityScore + 1

    # ISFP
    if PersonalityTypeOne == "ISFP":
        if PersonalityTypeTwo == "ISFP":
            PersonalityScore = PersonalityScore + 1
        if PersonalityTypeTwo == "ENFP" or PersonalityTypeTwo == "INFP":
            PersonalityScore = PersonalityScore + 1
        if PersonalityTypeTwo == "INFJ":
            PersonalityScore = PersonalityScore + 1

    # ESTP
    if PersonalityTypeOne == "ESTP":
        if PersonalityTypeTwo == "INFJ" or PersonalityTypeTwo == "ESTJ":
            PersonalityScore = PersonalityScore + 1
        if PersonalityTypeTwo == "ISFJ" or PersonalityTypeTwo == "ISTP":
            PersonalityScore = PersonalityScore + 1

    # ESFP
    if PersonalityTypeOne == "ESFP":
        if PersonalityTypeTwo == "ISTJ" or PersonalityTypeTwo == "ISFJ":
            PersonalityScore = PersonalityScore + 1
        if "S" or "J" in PersonalityTypeTwo:
            PersonalityScore = PersonalityScore + 1
        if PersonalityTypeTwo == "ENFP":
            PersonalityScore = PersonalityScore + 1

    return PersonalityScore

###############################################################

def main():
    CompatibilityScore = 0

    SpotifyUserOne = GetUserToken("Dexter", "")
    SpotifyUserTwo = GetUserToken("Tudor", "")

    MoviesUserOne = ["titanic", "the wizard of oz", "the lion king"]
    MoviesUserTwo = ["jurassic park", "fight club", "pulp fiction"]

    HobbiesUserOne = ["Fotbal", "Programare", "cantat"]
    HobbiesUserTwo = ["Baschet", "Cantat", "Programare"]

    PersonalityTypeUserOne = "INTP"
    PersonalityTypeUserTwo = "INFP"

    CompatibilityScore = CompatibilityScore + GetMusicCompatibility(SpotifyUserOne, SpotifyUserTwo)
    CompatibilityScore = CompatibilityScore + GetMovieCompatibility(MoviesUserOne, MoviesUserTwo)
    CompatibilityScore = CompatibilityScore + GetHobbyCompatibility(HobbiesUserOne, HobbiesUserTwo)
    CompatibilityScore = CompatibilityScore + max(GetPersonalityTypeMatch(PersonalityTypeUserOne, PersonalityTypeUserTwo), GetPersonalityTypeMatch(PersonalityTypeUserTwo, PersonalityTypeUserOne))

    print(CompatibilityScore)


if __name__ == '__main__':
    main()
