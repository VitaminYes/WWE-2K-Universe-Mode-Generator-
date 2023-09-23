from functions import *
import os
from GUI import *

def main():
    inputs = gui()

    # create variables from inputs
    male_roster_file, female_roster_file = inputs[0], inputs[1]  # roster inputs
    brand_number, team_number = inputs[2], inputs[3]  # brand inputs
    women_tag_number, second_midcard, women_midcard = inputs[4], inputs[5], inputs[6]  # optional division inputs
    brand_names, title_names = inputs[7], inputs[8]  # name inputs
    file_type = inputs[9]
    team_roster_file, women_team_roster_file = inputs[10], inputs[11]

    # get the rosters
    male_roster, female_roster = getRoster(male_roster_file), getRoster(female_roster_file)
    team_roster, women_team_roster = None, None
    if team_roster_file: team_roster = getRoster(team_roster_file)
    if women_team_roster_file: women_team_roster = getRoster(women_team_roster_file)

    draft_file = None
    # create the draft text file
    if file_type == "Text":
        draft_file = open("draft.txt", 'w')
        draft_file.close()
        draft_file = open("draft.txt", 'a')

    if file_type == "Spreadsheet":
        # create the draft spreadsheet
        draft_spreadsheet = xl.Workbook()
        rosters_sheet = draft_spreadsheet.create_sheet("Rosters")
        tag_teams_sheet = draft_spreadsheet.create_sheet("Tag Teams")
        champions_sheet = draft_spreadsheet.create_sheet("Champions")
        divisions_sheet = draft_spreadsheet.create_sheet("Divisions")
        feuds_sheet = draft_spreadsheet.create_sheet("Rivalries")
        women_tag_sheet = draft_spreadsheet.create_sheet("Women's Tag Division")



    # draft the rosters
    men, women = draftRoster(male_roster, brand_number), draftRoster(female_roster, brand_number)
    teams, women_teams = None, None
    if team_roster: teams = draftRoster(team_roster, brand_number)
    if women_team_roster: women_teams = draftRoster(women_team_roster, brand_number)

    # create the brands
    brands = []  # list of the brands

    for i in range(0, brand_number):
        b = Brand(brand_names[i], men[i], women[i], title_names[i])
        if not teams and not women_teams: developBrand(b, team_number, women_tag_number, second_midcard, women_midcard, draft_file, file_type, teams, women_teams)
        elif teams and not women_teams: developBrand(b, team_number, women_tag_number, second_midcard, women_midcard, draft_file, file_type, teams[i], women_teams)
        elif not teams and women_teams: developBrand(b, team_number, women_tag_number, second_midcard, women_midcard, draft_file, file_type, teams, women_teams[i])
        else: developBrand(b, team_number, women_tag_number, second_midcard, women_midcard, draft_file, file_type, teams[i], women_teams[i])
        brands.append(b)

    # set womens tag team champions if division exists
    womens_tag_division = createWomenTagDivision(women_tag_number, brands, draft_file, file_type, women_teams)

    # create spreadsheet
    if file_type == "Spreadsheet":
        i = 1  # iterator
        for b in brands:
            createSpreadsheet(b, i, draft_spreadsheet, rosters_sheet, tag_teams_sheet, champions_sheet, divisions_sheet,
                feuds_sheet, women_tag_sheet, womens_tag_division, file_type, team_roster, women_team_roster)
            i += 1

        headers = [rosters_sheet['A1:Z1'], tag_teams_sheet['A1:Z1'], champions_sheet['A1:Z1'], champions_sheet['A2:A20'],
                   divisions_sheet['A1:BA2'], women_tag_sheet['A1:Z1'], feuds_sheet['A1:Z1']]
        bodies = [rosters_sheet['A2:K200'], tag_teams_sheet['A2:K50'], champions_sheet['B2:K50'],
                  divisions_sheet['A3:BA200'], women_tag_sheet['A2:Z50'], feuds_sheet['A2:Z50']]

        for h in headers: formatSpreadsheet(h, "Header")
        for b in bodies: formatSpreadsheet(b, "Body")
        std = draft_spreadsheet['Sheet']
        draft_spreadsheet.remove(std)

        for col in range(1, divisions_sheet.max_column + 1):
            rosters_sheet.column_dimensions[get_column_letter(col)].width = 25
            tag_teams_sheet.column_dimensions[get_column_letter(col)].width = 30
            champions_sheet.column_dimensions[get_column_letter(col)].width = 25
            divisions_sheet.column_dimensions[get_column_letter(col)].width = 25
            women_tag_sheet.column_dimensions[get_column_letter(col)].width = 25
            feuds_sheet.column_dimensions[get_column_letter(col)].width = 30

        if file_type == "Spreadsheet": draft_spreadsheet.save("Draft.xlsx")

    if file_type == "Text": sg.PopupOK("Success", "Your Universe has been successfully generated.\n"
                                                  "Look for the Draft.txt file in the program's directory for the results")
    elif file_type == "Spreadsheet": sg.PopupOK("Success", "Your Universe has been successfully generated.\n"
                                                           "Look for the Draft.xlsx file in the program's directory for the results")


main()
