import random, os
import PySimpleGUI as sg


# create the brand class
class Brand:
    # constructor
    def __init__(self, name, men, women):
        self.name = name
        self.men = men
        self.women = women
        self.roster = men + women

    # method to create tag teams
    def createTeams(self, team_number):
        # create variables
        men = self.men
        self.teams = []

        random.shuffle(men)

        # assign teams
        for i in range(0, team_number * 2, 2):
            self.teams.append((men[i], men[i + 1]))
        return self.teams

    def createWomenTeams(self, womens_team_number):
        women = self.women
        self.women_teams = []
        if womens_team_number == 0: return self.women_teams

        random.shuffle(women)

        # assign teams
        for i in range(0, womens_team_number * 2, 2):
            self.women_teams.append((women[i], women[i + 1]))
        return self.women_teams

    # method to assign champions
    def assignChampions(self, teams, second_midcard, womens_midcard):
        male_roster = self.men
        female_roster = self.women

        # randomize order of sections
        random.shuffle(male_roster)
        random.shuffle(female_roster)
        random.shuffle(teams)

        # create variables
        self.champions = []
        second_midcard_champion = None
        womens_midcard_champion = None

        singles_division = Brand.removeTeams(male_roster, teams)

        # assign champions
        world_champion = singles_division[0]
        midcard_champion = singles_division[1]
        womens_champion = female_roster[0]
        tag_champions = teams[0]
        if second_midcard: second_midcard_champion = singles_division[2]
        if womens_midcard: womens_midcard_champion = female_roster[1]

        # put champions in list
        self.champions = [world_champion, midcard_champion, womens_champion, tag_champions,
                          second_midcard_champion, womens_midcard_champion]
        return self.champions

    # method to assign divisions
    def assignDivisions(self, tag_teams, champions, second_midcard, womens_midcard):
        # create the variables
        men = self.men
        women = self.women
        self.divisions = []
        world_division, midcard_division, womens_division, tag_division, second_midcard_division, womens_midcard_division = [], [], [], [], [], []
        male_belt_order = 1
        female_belt_order = 1

        # prepare lists for divisions
        Brand.removeTeams(men, tag_teams)

        # shuffle the lists
        random.shuffle(men)
        random.shuffle(women)
        random.shuffle(tag_teams)

        # Create the men's divisions
        for m in men:

            # World Title
            if male_belt_order == 1:
                world_division.append(m)
                male_belt_order = 2

            # Midcard Title
            elif male_belt_order == 2:
                midcard_division.append(m)
                if second_midcard:
                    male_belt_order = 3
                else:
                    male_belt_order = 1

            # 2nd Midcard Title
            elif male_belt_order == 3:
                second_midcard_division.append(m)
                male_belt_order = 1

        # Women's Division(s)
        for w in women:
            if female_belt_order == 1:
                womens_division.append(w)
                if womens_midcard: female_belt_order = 2

            elif female_belt_order == 2:
                womens_midcard_division.append(w)
                female_belt_order = 1
        tag_division = tag_teams

        self.divisions = [world_division, midcard_division, womens_division, tag_division,
                          second_midcard_division, womens_midcard_division]
        return self.divisions

    @staticmethod
    def removeTeams(roster, teams):
        singles_roster = roster
        for r in singles_roster:
            for t in teams:
                if r == t[0] or r == t[1]:
                    singles_roster.remove(r)
        return singles_roster


# additional functions

# create the rosters
def getRoster(roster_file):
    with open(roster_file) as f:
        roster = f.readlines()
    return roster


# draft the brands
def draftRoster(roster, brands):
    raw_roster, smackdown_roster, nxt_roster, aew_roster, nxt_uk_roster, roh_roster = [], [], [], [], [], []  # Roster lists
    b = 1  # Brand Counter
    random.shuffle(roster)  # Shuffle the roster order

    # Draft the rosters
    for r in roster:

        # Raw Pick
        if b == 1:
            raw_roster.append(r[:-1])
            b = 2
            continue

        # Smackdown Pick
        if b == 2:
            smackdown_roster.append(r[:-1])
            if brands == 2:
                b = 1
                continue
            else:
                b = 3
                continue

        # NXT Pick
        if b == 3:
            nxt_roster.append(r[:-1])
            if brands == 3:
                b = 1
                continue
            else:
                b = 4
                continue

        # AEW Pick
        if b == 4:
            aew_roster.append(r[:-1])
            if brands == 4:
                b = 1
                continue
            else:
                b = 5
                continue

        # NXT UK Pick
        if b == 5:
            nxt_uk_roster.append(r[:-1])
            if brands == 5:
                b = 1
                continue
            else:
                b = 6
                continue

        # ROH Pick
        if b == 6:
            roh_roster.append(r[:-1])
            b = 1

            continue

    brandRosters = [raw_roster, smackdown_roster, nxt_roster, aew_roster, nxt_uk_roster, roh_roster]
    return brandRosters


def addTeams(roster, teams):
    for t in teams:
        roster.append(t[0])
        roster.append(t[1])
    return roster


def makeTxtFile(f, brand, men, women, teams, champions, divisions, second_midcard_division, womens_midcard_division):
    # Header
    f.write(brand + "\n")
    f.write("=" * 30 + "\n\n")

    full_mens_roster = addTeams(men, teams)
    full_mens_roster.sort()
    women.sort()

    # Men's Roster
    f.write("Men's Roster\n")
    f.write("=" * 30 + "\n")
    for m in full_mens_roster:
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
    f.write("World Champion: " + champions[0] + "\n")
    f.write("Midcard Champion: " + champions[1] + "\n")
    if second_midcard_division: f.write(f"2nd Midcard Champion: {champions[4]}\n")
    f.write("Tag Team Champions: " + champions[3][0] + " & " + champions[3][1] + "\n")
    f.write("Women's Champion: " + champions[2] + "\n")
    if womens_midcard_division: f.write(f"Women's Midcard Champion {champions[5]}")
    f.write("\n\n")

    # Divisions
    f.write("Divisions\n")
    f.write("=" * 30 + "\n\n")

    # World Title
    f.write("World Title\n")
    f.write("=" * 30 + "\n")
    for d in divisions[0]:
        f.write(d + "\n")
    f.write("\n\n")

    # Midcard Title
    f.write("Midcard Title\n")
    f.write("=" * 30 + "\n")
    for d in divisions[1]:
        f.write(d + "\n")
    f.write("\n\n")

    # 2nd Midcard Title
    if second_midcard_division:
        f.write("2nd Midcard Title\n")
        f.write("=" * 30 + "\n")
        for d in divisions[4]:
            f.write(f"{d}\n")
        f.write("\n\n")

    # Tag Title
    f.write("Tag Team Title\n")
    f.write("=" * 30 + "\n")
    for d in divisions[3]:
        f.write(d[0] + " & " + d[1] + "\n")
    f.write("\n\n")

    # Women's Title
    f.write("Women's Title \n")
    f.write("=" * 30 + "\n")
    for d in divisions[2]:
        f.write(d + "\n")
    f.write("\n\n")

    # Women's Midcard Title
    if womens_midcard_division:
        f.write("Women's Midcard Title\n")
        f.write("=" * 30 + "\n")
        for d in divisions[5]:
            f.write(f"{d}\n")
    f.write("\n\n")


def writeWomenTag(f, womens_teams, womens_tag_champions):
    f.write("\n\n")
    f.write("Women's Tag Division\n")
    f.write("=" * 30)
    f.write("\n\n")
    f.write("Women\'s Tag Team Champions: {} & {}".format(womens_tag_champions[0], womens_tag_champions[1]))
    f.write("\n\n")
    for w in womens_teams[1:]:
        f.write(w[0] + " & " + w[1] + "\n")


def gui():
    current_directory = os.getcwd()

    sg.theme("SystemDefault1")
    # GUI Variables
    men = sg.FileBrowse("Men's Roster", file_types=[("TXT Files", "*.txt")], initial_folder=current_directory)
    women = sg.FileBrowse("Women's Roster", file_types=[("TXT Files", "*.txt")], initial_folder=current_directory)

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
            male_roster = values["-FILE_PATH-"]
            female_roster = values["-FILE_PATH2-"]
            brand_number = values["brands"]
            tag_teams = values["teams"]
            womens_tag_team_title = values["wTag"]
            second_midcard_title = values["mid2"]
            womens_midcard_title = values["wMid"]

            # Create list of GUI inputs
            gui_inputs = [male_roster, female_roster, int(brand_number), int(tag_teams),
                         int(womens_tag_team_title), second_midcard_title, womens_midcard_title]

            # If any fields are blank, give an error message, and continue
            if gui_inputs.count("") > 0:
                sg.PopupError(
                    "One or both roster files has not been given. \nPlease give both the men and women rosters.")
                continue
            return gui_inputs

    window.close()


def main():
    inputs = gui()

    male_roster_file = inputs[0]
    female_roster_file = inputs[1]
    brand_number = inputs[2]
    team_number = inputs[3]
    women_tag_number = inputs[4]
    second_mid_card = inputs[5]
    women_midcard = inputs[6]

    # get the rosters
    male_roster = getRoster(male_roster_file)
    female_roster = getRoster(female_roster_file)

    # create the draft text file
    draft_file = open("draft.txt", 'w')
    draft_file.close()
    draft_file = open("draft.txt", 'a')

    # draft the rosters
    men, women = draftRoster(male_roster, brand_number), draftRoster(female_roster, brand_number)

    # create the brands

    # create Raw
    Raw = Brand("Raw", men[0], women[0])
    Raw.createTeams(team_number)
    Raw.createWomenTeams(women_tag_number)
    Raw.assignChampions(Raw.teams, second_mid_card, women_midcard)
    Raw.assignDivisions(Raw.teams, Raw.champions, second_mid_card, women_midcard)
    makeTxtFile(draft_file, "Raw", Raw.men, Raw.women, Raw.teams, Raw.champions, Raw.divisions,
                second_mid_card, women_midcard)

    # create Smackdown
    if brand_number > 1:
        Smackdown = Brand("Smackdown", men[1], women[1])
        Smackdown.createTeams(team_number)
        Smackdown.createWomenTeams(women_tag_number)
        Smackdown.assignChampions(Smackdown.teams, second_mid_card, women_midcard)
        Smackdown.assignDivisions(Smackdown.teams, Smackdown.champions, second_mid_card, women_midcard)
        makeTxtFile(draft_file, "Smackdown", Smackdown.men, Smackdown.women, Smackdown.teams, Smackdown.champions,
                    Smackdown.divisions,
                    second_mid_card, women_midcard)

    # create NXT
    if brand_number > 2:
        NXT = Brand("NXT", men[2], women[2])
        NXT.createTeams(team_number)
        NXT.createWomenTeams(women_tag_number)
        NXT.assignChampions(NXT.teams, second_mid_card, women_midcard)
        NXT.assignDivisions(NXT.teams, NXT.champions, second_mid_card, women_midcard)
        makeTxtFile(draft_file, "NXT", NXT.men, NXT.women, NXT.teams, NXT.champions, NXT.divisions,
                    second_mid_card, women_midcard)

    # create AEW
    if brand_number > 3:
        AEW = Brand("AEW", men[3], women[3])
        AEW.createTeams(team_number)
        AEW.createWomenTeams(women_tag_number)
        AEW.assignChampions(AEW.teams, second_mid_card, women_midcard)
        AEW.assignDivisions(AEW.teams, AEW.champions, second_mid_card, women_midcard)
        makeTxtFile(draft_file, "AEW", AEW.men, AEW.women, AEW.teams, AEW.champions, AEW.divisions,
                    second_mid_card, women_midcard)

    # create NXT UK
    if brand_number > 4:
        UK = Brand("NXT UK", men[4], women[4])
        UK.createTeams(team_number)
        UK.createWomenTeams(women_tag_number)
        UK.assignChampions(UK.teams, second_mid_card, women_midcard)
        UK.assignDivisions(UK.teams, UK.champions, second_mid_card, women_midcard)
        makeTxtFile(draft_file, "NXT UK", UK.men, UK.women, UK.teams, UK.champions, UK.divisions,
                    second_mid_card, women_midcard)

    # create ROH
    if brand_number > 5:
        ROH = Brand("ROH", men[5], women[5])
        ROH.createTeams(team_number)
        ROH.createWomenTeams(women_tag_number)
        ROH.assignChampions(ROH.teams, second_mid_card, women_midcard)
        ROH.assignDivisions(ROH.teams, ROH.champions, second_mid_card, women_midcard)
        makeTxtFile(draft_file, "ROH", ROH.men, ROH.women, ROH.teams, ROH.champions, ROH.divisions,
                    second_mid_card, women_midcard)

    # set womens tag team champions if division exists
    if women_tag_number > 0:
        if women_tag_number == 1:
            womens_tag_division = Raw.women_teams
        elif women_tag_number == 2:
            womens_tag_division = Raw.women_teams + Smackdown.women_teams
        elif women_tag_number == 3:
            womens_tag_division = Raw.women_teams + Smackdown.women_teams + NXT.women_teams
        elif women_tag_number == 4:
            womens_tag_division = Raw.women_teams + Smackdown.women_teams + NXT.women_teams + AEW.women_teams
        elif women_tag_number == 5:
            womens_tag_division = Raw.women_teams + Smackdown.women_teams + NXT.women_teams + AEW.women_teams + UK.women_teams
        elif women_tag_number == 6:
            womens_tag_division = Raw.women_teams + Smackdown.women_teams + NXT.women_teams + AEW.women_teams + UK.women_teams + ROH.women_teams
        random.shuffle(womens_tag_division)
        womens_tag_champions = womens_tag_division[0]
        writeWomenTag(draft_file, womens_tag_division, womens_tag_champions)

    draft_file.close()  # close the file handler
    os.startfile("draft.txt")  # open the draft file


main()
