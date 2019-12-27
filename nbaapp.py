from sqlalchemy import *
import PySimpleGUI as sg

password = input("MySQL Password: ")

settings = {
    'username': "root",
    'password': password,
    'serverName': "localhost",
    'portNumber': 3306,
    'dbName': "nbadb",
}

conn = create_engine('mysql://{0[username]}:{0[password]}@{0[serverName]}:{0[portNumber]}/{0[dbName]}'.format(settings))
connection = conn.connect()

sg.theme("DarkBlue")

layout = [[sg.Text("NBA Player Stat Lookup", size=(50,1), font=(25))],
          [sg.Text("created by Varun Thakkar", size=(50,2))],
          [sg.Text("Select:", size=(50, 1))],
          [sg.Checkbox("Player Name", enable_events=True, key='name'),
          sg.Checkbox("Team", enable_events=True, key='team'),
          sg.Checkbox("Age", enable_events=True, key='age'),
          sg.Checkbox("Height", enable_events=True, key='height'),
          sg.Checkbox("Weight", enable_events=True, key='weight'),
          sg.Checkbox("College", enable_events=True, key='college'),
          sg.Checkbox("Country", enable_events=True, key='country'),
          sg.Checkbox("Net Rating", enable_events=True, key='net')],
          [sg.Checkbox("Games Played", enable_events=True, key='gp'),
          sg.Checkbox("Points Per Game", enable_events=True, key='ppg'),
          sg.Checkbox("Rebounds Per Game", enable_events=True, key='rpg'),
          sg.Checkbox("Assists Per Game", enable_events=True, key='apg'),
          sg.Checkbox("True Shooting", enable_events=True, key='ts')],
          [sg.Checkbox("Draft Year", enable_events=True, key='draftyear'),
          sg.Checkbox("Draft Round", enable_events=True, key='draftround'),
          sg.Checkbox("Draft Number", enable_events=True, key='draftnumber')],
          [sg.Text("Season: (ex: 2015, enter 'all' for all seasons)"), sg.In(key='season')],
          [sg.Text("")],
          [sg.Checkbox("Add filter?", enable_events=True, key='filter')],
          [sg.Text("Fiter: "), sg.Listbox(values=('Player Name', "Team", "Age", "Height", "Weight", "College",
          "Country", "Draft Year", "Draft Round", "Draft Number", "Games Played", "Points Per Game",
          "Rebounds Per Game", "Assists Per Game", "Net Rating", "True Shooting"), key='field', size=(15, 5)),
          sg.Radio("=", "comparator", default=True, key='='),
          sg.Radio("<", "comparator", key='<'),
          sg.Radio(">", "comparator", key='>'),
          sg.In(key='value')],
          [sg.Text("")],
          [sg.Text("Results:")],
          [sg.Multiline("", key='results', size=(100, 5))],
          [sg.Button("Submit"), sg.Button("Quit")],]

window = sg.Window("NBA Stat Lookup", layout)
while True:

    event, values = window.read()

    def add_string_filter(query):
        if values['=']:
            query = query + "= '{}'".format(values['value'])
        else:
            print("Error")

        return query

    def add_num_filter(query):
        if values['=']:
            query = query + "= {}".format(values['value'])
        elif values['<']:
            query = query + "< {}".format(values['value'])
        elif values['>']:
            query = query + "> {}".format(values['value'])

        return query

    if event in (None, "Quit"):
        break

    if event == "Submit":
        selected = []
        if values['name']:
            selected.append("player_name")
        if values['team']:
            selected.append("team")
        if values['age']:
            selected.append("age")
        if values['height']:
            selected.append("height")
        if values['weight']:
            selected.append("weight")
        if values['college']:
            selected.append("college")
        if values['country']:
            selected.append("country")
        if values['net']:
            selected.append("net_rating")
        if values['gp']:
            selected.append("games_played")
        if values['ppg']:
            selected.append("avg_pts")
        if values['rpg']:
            selected.append("avg_reb")
        if values['apg']:
            selected.append("avg_asts")
        if values['ts']:
            selected.append("true_shooting")
        if values['draftyear']:
            selected.append("draft_year")
        if values['draftround']:
            selected.append("draft_round")
        if values['draftnumber']:
            selected.append("draft_number")

        selected_formatted = ""
        for field in selected:
            if field == selected[len(selected) - 1]:
                selected_formatted = selected_formatted + field
            else:
                selected_formatted = selected_formatted + field + ", "

        query = "SELECT {} FROM stats".format(selected_formatted)
        if values['filter']:
            query = query + " WHERE "

            if values['field'][0] == 'Player Name':

                query = query + "player_name "
                query = add_string_filter(query)

            elif values['field'][0] == "Team":

                query = query + "team "
                query = add_string_filter(query)

            elif values['field'][0] == "Age":

                query = query + "age "
                query = add_num_filter(query)

            elif values['field'][0] == "Height":

                query = query + "height "
                query = add_num_filter(query)

            elif values['field'][0] == "Weight":

                query = query + "weight "
                query = add_num_filter(query)

            elif values['field'][0] == "College":

                query = query + "college "
                query = add_string_filter(query)

            elif values['field'][0] == "Country":

                query = query + "country "
                query = add_string_filter(query)

            elif values['field'][0] == "Draft Year":

                query = query + "draft_year "
                query = add_num_filter(query)

            elif values['field'][0] == "Draft Round":

                query = query + "draft_round "
                query = add_num_filter(query)

            elif values['field'][0] == "Draft Number":

                query = query + "draft_number "
                query = add_num_filter(query)

            elif values['field'][0] == "Games Played":

                query = query + "games_played "
                query = add_num_filter(query)

            elif values['field'][0] == "Points Per Game":

                query = query + "avg_pts "
                query = add_num_filter(query)

            elif values['field'][0] == "Rebounds Per Game":

                query = query + "avg_reb "
                query = add_num_filter(query)

            elif values['field'][0] == "Assists Per Game":

                query = query + "avg_asts "
                query = add_num_filter(query)

            elif values['field'][0] == "True Shooting":

                query = query + "true_shooting "
                query = add_num_filter(query)

            elif values['field'][0] == "Net Rating":

                query = query + "net_rating "
                query = add_num_filter(query)

            if values['season'] != 'all':
                query = query + " and season = '{}'".format(values['season'])
            else:
                query = query[:7] + "season," + query[7:]

        else:

            if values['season'] != 'all':
                query = query + " WHERE season = '{}'".format(values['season'])
            else:
                query = query[:7] + "season," + query[7:]

        results = conn.execute(query)

        output = ""
        for row in results:
            for item in row:
                output = output + str(item) + "   "
            output = output + "\n"

        window['results'].update(output)

        connection.close()
        results.close()

window.close()
