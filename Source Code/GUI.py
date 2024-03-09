import os, PySimpleGUI as sg
from functions import *
def gui():
    current_directory = os.getcwd()
    sg.theme("Reddit")

    # creates list of default championship names
    title_names = [
        ["World Heavyweight", "Intercontinental", "Women's World", "Raw Tag Team", "24/7", "Women's Intercontinental"],  # Raw
        ["WWE Universal", "United States", "WWE Women's", "Smackdown Tag Team", "European",
         "Women's United States"],  # Smackdown
        ["NXT", "North American", "NXT Women's", "NXT Tag Team", "Cruiserweight", "Women's North American"],  # NXT
        ["AEW World", "TNT", "AEW Women's", "AEW Tag Team", "International", "TBS"],  # AEW
        ["NXT UK", "Heritage Cup", "NXT UK Women's", "NXT UK Tag Team", "NXT UK Cruiserweight", "Women's Heritage Cup"],
        # NXT UK
        ["ROH World", "Television", "ROH Women's", "ROH Tag Team", "Pure", "Women's Television"]  # ROH
    ]

    # creates list of key names
    key_names = [
        ["raw_world", "raw_mid", "raw_women", "raw_tag", "raw_mid2", "raw_womens_mid"],  # Raw
        ["sd_world", "sd_mid", "sd_women", "sd_tag", "sd_mid2", "sd_womens_mid"],  # Smackdown
        ["nxt_world", "nxt_mid", "nxt_women", "nxt_tag", "nxt_mid2", "nxt_womens_mid"],  # NXT
        ["aew_world", "aew_mid", "aew_women", "aew_tag", "aew_mid2", "aew_womens_mid"],  # AEW
        ["uk_world", "uk_mid", "uk_women", "uk_tag", "uk_mid2", "uk_womens_mid"],  # NXT UK
        ["roh_world", "roh_mid", "roh_women", "roh_tag", "roh_mid2", "roh_womens_mid"]  # ROH
    ]

    # GUI Variables
    men = sg.FileBrowse("Men's Roster", file_types=[("TXT Files", "*.txt")], initial_folder=current_directory)
    women = sg.FileBrowse("Women's Roster", file_types=[("TXT Files", "*.txt")], initial_folder=current_directory)
    team_roster = sg.FileBrowse("Men's Teams Roster", file_types=[("TXT Files", "*.txt")], initial_folder=current_directory, visible=False)
    women_team_roster = sg.FileBrowse("Women's Teams Roster", file_types=[("TXT Files", "*.txt")], initial_folder=current_directory, visible=False)

    brands = [i for i in range(1, 7)]
    teams = [i for i in range(1, 21)]
    women_teams = [i for i in range(0, 11)]

    # GUI Layout
    main_layout = [
        [sg.Text("Select Your Male and Female Roster Files")],  # Title
        [sg.InputText(key="-FILE_PATH-"), men],  # Men's Roster Input
        [sg.InputText(key="-FILE_PATH2-"), women],  # Women's Roster Input
        [sg.InputText(key='-FILE_PATH3-', visible=False), team_roster], # Tag Roster Input
        [sg.InputText(key='-FILE_PATH4-', visible=False), women_team_roster],
        [sg.Text("Select the number of brands"),  # Brand Number
         sg.Spin(brands, initial_value=2, key='brands', size=4, enable_events=True)],
        [sg.Text("Select the number of tag teams per brand"),  # Team Number
         sg.Spin(teams, key='teams', initial_value=4, size=4)],
        [sg.Text("Select the number of Women's Tag Teams you want per brand"),  # Women's Team Number
         sg.Spin(women_teams, initial_value="0", key='wTag', size=4, enable_events=True)],
        [sg.Checkbox("2nd Midcard Title", key='mid2')],
        [sg.Checkbox("Women's Midcard Title", key='wMid')],
        [sg.Checkbox("Separate Team Roster", key='team_roster', enable_events=True),
         sg.Checkbox("Separate Women Team Roster", key='women_team_roster', enable_events=True)],
        [sg.Text("Which file type?"), sg.Combo(["Text", "Spreadsheet"], default_value="Text", key='file_type')]
    ]

    raw_layout = makeTabLayout("Raw", "raw_name", title_names[0], key_names[0])
    sd_layout = makeTabLayout("Smackdown", "sd_name", title_names[1], key_names[1])
    nxt_layout = makeTabLayout("NXT", "nxt_name", title_names[2], key_names[2])
    aew_layout = makeTabLayout("AEW", "aew_name", title_names[3], key_names[3])
    uk_layout = makeTabLayout("NXT UK", "uk_name", title_names[4], key_names[4])
    roh_layout = makeTabLayout("ROH", "roh_name", title_names[5], key_names[5])

    layout = [[sg.TabGroup([
        [sg.Tab('General', main_layout),
         sg.Tab('Raw', raw_layout, key='raw_tab'),
         sg.Tab('Smackdown', sd_layout, key='sd_tab'),
         sg.Tab('NXT', nxt_layout, key='nxt_tab', visible=False),
         sg.Tab('AEW', aew_layout, key='aew_tab', visible=False),
         sg.Tab('NXT UK', uk_layout, key='uk_tab', visible=False),
         sg.Tab('ROH', roh_layout, key='roh_tab', visible=False)
         ]])],
        [sg.Button("Generate"), sg.Exit()]
    ]

    # Create the window
    window = sg.Window("2K Universe Generator", layout)

    # Create the event loop
    while True:
        event, values = window.read()

        # a list of events to cause a refresh
        refresh = ["brands", "raw_name", "sd_name", "nxt_name", "aew_name", "uk_name", "roh_name"]

        # If Window closed or exit button pressed, end the program
        if event in (sg.WIN_CLOSED, 'Exit'):
            sys.exit()

        # If the Submit button is pressed
        elif event == "Generate":

            if values["-FILE_PATH4-"] and values["wTag"] == 0: values["wTag"] = 1

            # Create variables for GUI inputs
            male_roster, female_roster = values["-FILE_PATH-"], values["-FILE_PATH2-"]
            brand_number, tag_teams = values["brands"], values["teams"]
            womens_tag_team_title = values["wTag"]
            second_midcard_title, womens_midcard_title = values["mid2"], values["wMid"]
            file_type = values["file_type"]

            # handle case when excel file is already open
            if file_type == "Spreadsheet":
                try:
                    draft_file = open("Draft.xlsx", 'w')
                    draft_file.close()
                    draft_file = open("Draft.xlsx", 'a')
                except IOError:
                    sg.PopupError("The Draft.xlsx file is already open.\nPlease close the file")
                    continue

            # list of the brand names
            brand_names = [values["raw_name"], values["sd_name"], values["nxt_name"],
                           values["aew_name"], values["uk_name"], values["roh_name"]]

            # list of the title names
            title_names = [
                [values["raw_world"], values["raw_mid"], values["raw_women"], values["raw_tag"], values["raw_mid2"],
                 values["raw_womens_mid"]],
                [values["sd_world"], values["sd_mid"], values["sd_women"], values["sd_tag"], values["sd_mid2"],
                 values["sd_womens_mid"]],
                [values["nxt_world"], values["nxt_mid"], values["nxt_women"], values["nxt_tag"], values["nxt_mid2"],
                 values["nxt_womens_mid"]],
                [values["aew_world"], values["aew_mid"], values["aew_women"], values["aew_tag"], values["aew_mid2"],
                 values["aew_womens_mid"]],
                [values["uk_world"], values["uk_mid"], values["uk_women"], values["uk_tag"], values["uk_mid2"],
                 values["uk_womens_mid"]],
                [values["roh_world"], values["roh_mid"], values["roh_women"], values["roh_tag"], values["roh_mid2"],
                 values["roh_womens_mid"]]
            ]

            sep_team, sep_wteam = values["team_roster"], values["women_team_roster"]

            team_roster, women_team_roster = False, False
            if sep_team: team_roster = values["-FILE_PATH3-"]
            if sep_wteam: women_team_roster = values["-FILE_PATH4-"]
            # Create list of GUI inputs
            gui_inputs = [male_roster, female_roster, int(brand_number), int(tag_teams),
                          int(womens_tag_team_title), second_midcard_title, womens_midcard_title,
                          brand_names, title_names, file_type, team_roster, women_team_roster]

            # Check if brand number has exceeded the limit
            if int(brand_number) > 6: gui_inputs[2] = brand_number = 6

            # Check if tag team number has exceeded the limit
            if int(tag_teams) > 20: gui_inputs[3] = tag_teams = 20

            # Check if women's tag team number has exceeded the limit
            if int(womens_tag_team_title) > 10: gui_inputs[4] = womens_tag_team_title = 10

            # Check if a roster file is missing
            if not bool(male_roster) or not bool(female_roster):
                sg.PopupError(
                    "Missing Roster File", "One or both roster files has not been given. \n"
                                           "Please give both the men and women rosters.")
                continue

            # Check if a roster file is empty
            if len(getRoster(male_roster)) == 0 or len(getRoster(female_roster)) == 0:
                sg.PopupError("Empty Roster File", "One or both roster files is empty. \n"
                                                   "Please use a file with a list of participants")
                continue

            # Check if there are enough men/women to have as many tag teams as requested
            if len(getRoster(male_roster)) < int(tag_teams) * int(brand_number) * 2:
                sg.PopupError("Your men's roster is not big enough to support this many tag teams")
                continue

            if len(getRoster(female_roster)) < int(womens_tag_team_title) * int(brand_number) * 2:
                sg.PopupError("Your women's roster is not big enough to support this many tag teams.")
                continue
            # If any fields are blank, give an error message, and continue

            return gui_inputs

        # if a refresh event happens
        elif event in refresh:
            brand_number = values["brands"]
            window['raw_tab'].update(title=values["raw_name"])

            if brand_number == 1: window['sd_tab'].update(visible=False)
            else: window['sd_tab'].update(visible=True, title=values["sd_name"])

            if brand_number > 2: window['nxt_tab'].update(visible=True, title=values["nxt_name"])
            else: window['nxt_tab'].update(visible=False)

            if brand_number > 3: window['aew_tab'].update(visible=True, title=values["aew_name"])
            else: window['aew_tab'].update(visible=False)

            if brand_number > 4: window['uk_tab'].update(visible=True, title=values["uk_name"])
            else: window['uk_tab'].update(visible=False)

            if brand_number == 6: window['roh_tab'].update(visible=True, title=values["roh_name"])
            else: window['roh_tab'].update(visible=False)

        if values['team_roster']: window['-FILE_PATH3-'].update(visible=True); team_roster.update(visible=True)
        else: window['-FILE_PATH3-'].update(visible=False); team_roster.update(visible=False)
        if values['women_team_roster']: window['-FILE_PATH4-'].update(visible=True); women_team_roster.update(visible=True)
        else: window['-FILE_PATH4-'].update(visible=False); women_team_roster.update(visible=False)

    window.close()