# Importing the necessary packages
import random
import os
import PySimpleGUI as sg
from sys import exit


# Convert a roster file into a list
def getRoster(rFile):
    with open(rFile) as f:
        roster = f.readlines()
    return roster


# Draft the brands
def draftRoster(roster, brands):
    raw, sd, nxt, aew, uk, roh = [], [], [], [], [], []  # Roster lists
    b = 1  # Brand Counter
    random.shuffle(roster)  # Shuffle the roster order

    # Draft the rosters
    for r in roster:

        # Raw Pick
        if b == 1:
            raw.append(r[:-1])
            b = 2
            continue

        # Smackdown Pick
        if b == 2:
            sd.append(r[:-1])
            if brands == 2:
                b = 1
                continue
            else:
                b = 3
                continue

        # NXT Pick
        if b == 3:
            nxt.append(r[:-1])
            if brands == 3:
                b = 1
                continue
            else:
                b = 4
                continue

        # AEW Pick
        if b == 4:
            aew.append(r[:-1])
            if brands == 4:
                b = 1
                continue
            else:
                b = 5
                continue

        # NXT UK Pick
        if b == 5:
            uk.append(r[:-1])
            if brands == 5:
                b = 1
                continue
            else:
                b = 6
                continue

        # ROH Pick
        if b == 6:
            roh.append(r[:-1])
            b = 1

            continue

    brandRosters = [raw, sd, nxt, aew, uk, roh]
    return brandRosters


# Create the tag teams
def createTagTeams(roster, teamNum):
    random.shuffle(roster)
    tagTeams = []

    for i in range(1, teamNum * 2, 2):
        tagTeams.append((roster[i], roster[i + 1]))

    return tagTeams


# Assign the champions
def assignChampions(men, women, teams, mid2, wMid):
    random.shuffle(men)
    random.shuffle(women)
    random.shuffle(teams)

    worldChamp = men[0]
    midChamp = men[1]
    womenChamp = women[0]
    tagChamp = teams[0]

    # 2nd Midcard Champion
    if mid2:
        mid2Champ = men[2]
    else:
        mid2Champ = None

    # Women's Midcard Champion
    if wMid:
        wMidChamp = women[1]
    else:
        wMidChamp = None

    brandChampions = [worldChamp, midChamp, womenChamp, tagChamp, mid2Champ, wMidChamp]
    return brandChampions


# Assign the divisions
def createDivisions(men, women, teams, champions, mid2, wMid):
    # Remove teams and champions from pools
    for m in men:
        for t in teams:
            if m == t[0] or m == t[1]: men.remove(m)
    for m in men:
        if m in champions: men.remove(m)

    for w in women:
        if w in champions: women.remove(w)

    # Randomize the order
    random.shuffle(men)
    random.shuffle(women)
    random.shuffle(teams)

    belt = 1  # Single's title counter
    wBelt = 1  # Women's title counter

    worldDiv = []
    midDiv = []
    womenDiv = []
    tagDiv = []
    mid2Div = []
    wMidDiv = []

    # Assign the men's divisions
    for m in men:

        # World Title
        if belt == 1:
            worldDiv.append(m)
            belt = 2

        # Midcard Title
        elif belt == 2:
            midDiv.append(m)
            if mid2:
                belt = 3
            else:
                belt = 1

        # 2nd Midcard Title
        elif belt == 3:
            mid2Div.append(m)
            belt = 1

    # Women's Division(s)
    for w in women:

        if wBelt == 1:
            womenDiv.append(w)
            if wMid: wBelt = 2

        elif wBelt == 2:
            wMidDiv.append(w)
            wBelt = 1

    # Tag Team Division
    for t in teams: tagDiv.append(t)

    brandDivs = [worldDiv, midDiv, womenDiv, tagDiv, mid2Div, wMidDiv]
    return brandDivs


def removeWomenTag(women, teams):
    for w in women:
        for t in teams:
            if w == t[0] or w == t[1]: women.remove(w)
            break
    return women


def main():
    inputs = gui()  # Get GUI inputs

    mRoster, wRoster = getRoster(inputs[0]), getRoster(inputs[1])  # Create the roster lists
    brands = int(inputs[2])  # Get the number of brands
    womenTagDivision = int(inputs[4])
    mid2, wMid = inputs[5], inputs[6]

    # Draft the rosters
    men, women = draftRoster(mRoster, brands), draftRoster(wRoster, brands)

    # Raw
    rawM, rawW = men[0], women[0]  # Create variables for rosters
    rMen, rWomen = rawM, rawW  # Variables to hold original values of roster list, as it will be modified later

    # Smackdown
    sdM, sdW = men[1], women[1]
    sMen, sWomen = sdM, sdW

    # Check if there are 3 brands
    if brands > 2:
        nxtM, nxtW = men[2], women[2]
        nMen, nWomen = nxtM, nxtW

    # Check if there are 4 brands
    if brands > 3:
        aewM, aewW = men[3], women[3]
        aMen, aWomen = aewM, aewW

    # Check if there are 5 brands
    if brands > 4:
        ukM, ukW = men[4], women[4]
        uMen, uWomen = ukM, ukW

    # Check if there are 6 brands
    if brands > 5:
        rohM, rohW = men[5], women[5]
        rMen, rWomen = rohM, rohW

    # Make the men's tag teams
    teamNum = int(inputs[3])  # Get the number of tag teams
    rawTeams = createTagTeams(rawM, teamNum)
    sdTeams = createTagTeams(sdM, teamNum)
    if brands > 2: nxtTeams = createTagTeams(nxtM, teamNum)
    if brands > 3: aewTeams = createTagTeams(aewM, teamNum)
    if brands > 4: ukTeams = createTagTeams(ukM, teamNum)
    if brands > 5: rohTeams = createTagTeams(rohM, teamNum)

    # Make the women's tag teams if requested
    if womenTagDivision:  # Check if Women's Tag Teams was selected
        rawWTeams, sdWTeams = createTagTeams(rawW, womenTagDivision), createTagTeams(sdW, womenTagDivision)
        if brands > 2: nxtWTeams = createTagTeams(nxtW, womenTagDivision)
        if brands > 3: aewWTeams = createTagTeams(aewW, womenTagDivision)
        if brands > 4: ukWTeams = createTagTeams(ukW, womenTagDivision)
        if brands > 5: rohWTeams = createTagTeams(rohW, womenTagDivision)

        womenTeams = rawWTeams + sdWTeams
        rawW = removeWomenTag(rawW, rawWTeams)
        sdW = removeWomenTag(sdW, sdWTeams)
        if brands > 2:
            womenTeams += nxtWTeams
            nxtW = removeWomenTag(nxtW, nxtWTeams)
        if brands > 3:
            womenTeams += aewWTeams
            aewW = removeWomenTag(aewW, aewWTeams)
        if brands > 4:
            womenTeams += ukWTeams
            ukW = removeWomenTag(ukW, ukWTeams)
        if brands > 5:
            womenTeams += rohWTeams
            rohW = removeWomenTag(rohW, rohWTeams)

        # Assign the Champion and Division Order
        random.shuffle(womenTeams)

    # Make the champions
    rawChamps = assignChampions(rawM, rawW, rawTeams, mid2, wMid)
    sdChamps = assignChampions(sdM, sdW, sdTeams, mid2, wMid)
    if brands > 2: nxtChamps = assignChampions(nxtM, nxtW, nxtTeams, mid2, wMid)
    if brands > 3: aewChamps = assignChampions(aewM, aewW, aewTeams, mid2, wMid)
    if brands > 4: ukChamps = assignChampions(ukM, ukW, ukTeams, mid2, wMid)
    if brands > 5: rohChamps = assignChampions(rohM, rohW, rohTeams, mid2, wMid)

    # Make the divisions
    rawDivs = createDivisions(rawM, rawW, rawTeams, rawChamps, mid2, wMid)
    sdDivs = createDivisions(sdM, sdW, sdTeams, sdChamps, mid2, wMid)
    if brands > 2: nxtDivs = createDivisions(nxtM, nxtW, nxtTeams, nxtChamps, mid2, wMid)
    if brands > 3: aewDivs = createDivisions(aewM, aewW, aewTeams, aewChamps, mid2, wMid)
    if brands > 4: ukDivs = createDivisions(ukM, ukW, ukTeams, ukChamps, mid2, wMid)
    if brands > 5: rohDivs = createDivisions(rohM, rohW, rohTeams, rohChamps, mid2, wMid)

    # Output to a txt file

    # Clear the file if it exists
    f = open("draft.txt", 'w')
    f.close()
    f = open("draft.txt", 'a')

    # Add the Header
    f.write("WWE 2K22 Random Roster Draft\n")
    f.write("=" * 30 + "\n\n")

    # Add the brand information
    makeTxtFile(f, "Raw", rMen, rWomen, rawTeams, rawChamps, rawDivs, mid2, wMid)
    makeTxtFile(f, "Smackdown", sMen, sWomen, sdTeams, sdChamps, sdDivs, mid2, wMid)
    if brands > 2: makeTxtFile(f, "NXT", nMen, nWomen, nxtTeams, nxtChamps, nxtDivs, mid2, wMid)
    if brands > 3: makeTxtFile(f, "AEW", aMen, aWomen, aewTeams, aewChamps, aewDivs, mid2, wMid)
    if brands > 4: makeTxtFile(f, "NXT UK", uMen, uWomen, ukTeams, ukChamps, ukDivs, mid2, wMid)
    if brands > 5: makeTxtFile(f, "ROH", rMen, rWomen, rohTeams, rohChamps, rohDivs, mid2, wMid)
    if womenTagDivision: writeWomenTag(f, womenTeams)

    # Open the draft file
    os.startfile("draft.txt")


# Create the draft .txt file
def makeTxtFile(f, brand, men, women, teams, champs, divs, mid2, wMid):
    # Header
    f.write(brand + "\n")
    f.write("=" * 30 + "\n\n")

    # Men's Roster
    f.write("Men's Roster\n")
    f.write("=" * 30 + "\n")
    for m in men:
        f.write(m + "\n")
    f.write("\n")

    # Women's Roster
    f.write("Women's Roster\n")
    f.write("=" * 30 + "\n")
    for w in women:
        f.write(w + "\n")
    f.write("\n")

    # Tag Teams
    f.write("" + "Tag Teams\n")
    f.write("=" * 30 + "\n")
    for t in teams:
        f.write(t[0] + " & " + t[1] + "\n")
    f.write("\n")

    # Champions
    f.write("Champions\n")
    f.write("=" * 30 + "\n")
    f.write("World Champion: " + champs[0] + "\n")
    f.write("Midcard Champion: " + champs[1] + "\n")
    if mid2: f.write("2nd Midcard Champion: " + champs[4] + "\n")
    f.write("Tag Team Champions: " + champs[3][0] + " & " + champs[3][1] + "\n")
    f.write("Women's Champion: " + champs[2] + "\n")
    if wMid: f.write("Women's Midcard Champion: " + champs[5] + "\n")
    f.write("\n")

    # Divisions
    f.write("Divisions\n")
    f.write("=" * 30 + "\n\n")

    # World Title
    f.write("World Title\n")
    f.write("=" * 30 + "\n")
    for d in divs[0]:
        f.write(d + "\n")
    f.write("\n\n")

    # Midcard Title
    f.write("Midcard Title\n")
    f.write("=" * 30 + "\n")
    for d in divs[1]:
        f.write(d + "\n")
    f.write("\n\n")

    # 2nd Midcard Title
    if mid2:
        f.write("2nd Midcard Title\n")
        f.write("=" * 30 + "\n")
        for d in divs[4]:
            f.write(d + "\n")
        f.write("\n\n")

    # Tag Team Title
    f.write("Tag Team Title\n")
    f.write("=" * 30 + "\n")
    for d in divs[3]:
        f.write(d[0] + " & " + d[1] + "\n")
    f.write("\n\n")

    # Women's Title
    f.write("Women's Title \n")
    f.write("=" * 30 + "\n")
    for d in divs[2]:
        f.write(d + "\n")
    f.write("\n\n")

    # Women's Midcard Title
    if wMid:
        f.write("Women's Midcard Title\n")
        f.write("=" * 30 + "\n")
        for d in divs[5]:
            f.write(d + "\n")
        f.write("\n\n")


def writeWomenTag(f, womenTeams):
    f.write("\n\n")
    f.write("Women's Tag Division\n")
    f.write("=" * 30)
    f.write("\n\n")
    f.write("Women\'s Tag Team Champions: {} & {}".format(womenTeams[0][0], womenTeams[0][1]))
    f.write("\n\n")
    for w in womenTeams[1:]:
        f.write(w[0] + " & " + w[1] + "\n")


# User Interface for the program
def gui():
    curr = os.getcwd()

    sg.theme("SystemDefault1")
    # GUI Variables
    men = sg.FileBrowse("Men's Roster", file_types=[("TXT Files", "*.txt")], initial_folder=curr)
    women = sg.FileBrowse("Women's Roster", file_types=[("TXT Files", "*.txt")], initial_folder=curr)

    # GUI Layout
    layout = [
        [sg.Text("Select Your Male and Female Roster Files")],  # Title
        [sg.InputText(key="-FILE_PATH-"), men],  # Men's Roster Input
        [sg.InputText(key="-FILE_PATH2-"), women],  # Women's Roster Input
        [sg.Text("Select the number of brands"),  # Brand Number
         sg.Combo(["2", "3", "4", "5", "6"], default_value="2", key='brands')],
        [sg.Text("Select the number of tag teams per brand"),  # Team Number
         sg.Combo(["2", "3", "4", "5", "6", "7", "8"], default_value="4", key='teams')],
        [sg.Text("Select the number of Women's Tag Teams you want per brand"),  # Women's Team Number
         sg.Combo(["0", "1", "2", "3", "4"], default_value="0", key='wTag')],
        [sg.Checkbox("2nd Midcard Title", key='mid2')],
        [sg.Checkbox("Women's Midcard Title", key='wMid')],
        [sg.Button("Generate"), sg.Exit()]
    ]

    # Create the window
    window = sg.Window("2K Universe Generator", layout)

    # Create the event loop
    while True:
        event, values = window.read()

        # If Window closed or exit button pressed, end the program
        if event in (sg.WIN_CLOSED, 'Exit'):
            exit()

        # If the Submit button is pressed
        elif event == "Generate":
            # Create variables for GUI inputs
            maleRoster = values["-FILE_PATH-"]
            femaleRoster = values["-FILE_PATH2-"]
            brands = values["brands"]
            teams = values["teams"]
            wTag = values["wTag"]
            mid2 = values["mid2"]
            wMid = values["wMid"]

            guiInputs = [maleRoster, femaleRoster, brands, teams, wTag, mid2, wMid]  # Create list of GUI inputs

            # If any fields are blank, give an error message, and continue
            if guiInputs.count("") > 0:
                sg.PopupError(
                    "One or both roster files has not been given. \nPlease give both the men and women rosters.")
                continue
            print(mid2)
            return guiInputs

    window.close()


main()
