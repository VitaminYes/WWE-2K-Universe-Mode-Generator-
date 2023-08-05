from functions import *


def main():
    inputs = gui()

    # create variables from inputs
    male_roster_file, female_roster_file = inputs[0], inputs[1]  # roster inputs
    brand_number, team_number = inputs[2], inputs[3]  # brand inputs
    women_tag_number, second_midcard, women_midcard = inputs[4], inputs[5], inputs[6]  # optional division inputs
    brand_names, title_names = inputs[7], inputs[8]  # name inputs

    # get the rosters
    male_roster, female_roster = getRoster(male_roster_file), getRoster(female_roster_file)

    # create the draft text file
    draft_file = open("draft.txt", 'w')
    draft_file.close()
    draft_file = open("draft.txt", 'a')

    # create the draft spreadsheet
    draft_spreadsheet = xl.Workbook()
    rosters_sheet = draft_spreadsheet.create_sheet("Rosters")
    tag_teams_sheet = draft_spreadsheet.create_sheet("Tag Teams")
    champions_sheet = draft_spreadsheet.create_sheet("Champions")
    divisions_sheet = draft_spreadsheet.create_sheet("Divisions")
    feuds_sheet = draft_spreadsheet.create_sheet("Rivalries")
    women_tag_sheet = draft_spreadsheet.create_sheet("Women's Tag Division")

    # format the spreadsheet

    # draft the rosters
    men, women = draftRoster(male_roster, brand_number), draftRoster(female_roster, brand_number)

    # create the brands
    brands = []  # list of the brands

    # create first brand
    Raw = Brand(brand_names[0], men[0], women[0], title_names[0])
    developBrand(Raw, team_number, women_tag_number, second_midcard, women_midcard, draft_file)
    brands.append(Raw)

    # create second brand
    if brand_number > 1:
        Smackdown = Brand(brand_names[1], men[1], women[1], title_names[1])
        developBrand(Smackdown, team_number, women_tag_number, second_midcard, women_midcard, draft_file)
        brands.append(Smackdown)

    # create third brand
    if brand_number > 2:
        NXT = Brand(brand_names[2], men[2], women[2], title_names[2])
        developBrand(NXT, team_number, women_tag_number, second_midcard, women_midcard, draft_file)
        brands.append(NXT)

    # create fourth brand
    if brand_number > 3:
        AEW = Brand(brand_names[3], men[3], women[3], title_names[3])
        developBrand(AEW, team_number, women_tag_number, second_midcard, women_midcard, draft_file)
        brands.append(AEW)

    # create fifth brand
    if brand_number > 4:
        UK = Brand(brand_names[4], men[4], women[4], title_names[4])
        developBrand(UK, team_number, women_tag_number, second_midcard, women_midcard, draft_file)
        brands.append(UK)

    # create sixth brand
    if brand_number > 5:
        ROH = Brand(brand_names[5], men[5], women[5], title_names[5])
        developBrand(ROH, team_number, women_tag_number, second_midcard, women_midcard, draft_file)
        brands.append(ROH)

    # set womens tag team champions if division exists
    womens_tag_division = createWomenTagDivision(women_tag_number, brands, draft_file)

    # create spreadsheet
    i = 1  # iterator
    for b in brands:
        createSpreadsheet(b, i, draft_spreadsheet, rosters_sheet, tag_teams_sheet, champions_sheet, divisions_sheet,
                          feuds_sheet,
                          women_tag_sheet, womens_tag_division)
        i += 1

    draft_file.close()  # close the file handler

    headers = [rosters_sheet['A1:Z1'], tag_teams_sheet['A1:Z1'], champions_sheet['A1:Z1'], champions_sheet['A2:A20'],
               divisions_sheet['A1:BA2'], women_tag_sheet['A1:Z1'], feuds_sheet['A1:Z1']]
    bodies = [rosters_sheet['A2:K200'], tag_teams_sheet['A2:K50'], champions_sheet['B2:K50'],
              divisions_sheet['A3:BA200'], women_tag_sheet['A2:Z50'], feuds_sheet['A2:Z50']]

    for h in headers:
        formatSpreadsheet(h, "Header")

    for b in bodies:
        formatSpreadsheet(b, "Body")
    std = draft_spreadsheet['Sheet']
    draft_spreadsheet.remove(std)

    for col in range(1, divisions_sheet.max_column + 1):
        rosters_sheet.column_dimensions[get_column_letter(col)].width = 25
        tag_teams_sheet.column_dimensions[get_column_letter(col)].width = 30
        champions_sheet.column_dimensions[get_column_letter(col)].width = 25
        divisions_sheet.column_dimensions[get_column_letter(col)].width = 25
        women_tag_sheet.column_dimensions[get_column_letter(col)].width = 25
        feuds_sheet.column_dimensions[get_column_letter(col)].width = 30

    draft_spreadsheet.save("Draft.xlsx")
    sg.PopupOK("Success", "Your Universe has been successfully generated.\n"
                          "Look for the Draft.txt and Draft.xlsx files in the program's directory for the results")


main()
