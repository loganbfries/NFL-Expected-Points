import nflscraPy
import nfl_data_py as nfl
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

week = sys.argv[1]

# Load in the boxscore data for completed games.
season_gamelogs = nflscraPy._gamelogs(2023)
completed_games = season_gamelogs[season_gamelogs["status"] == "closed"]

# Cut the data down to <= the specified week.
completed_games = completed_games[completed_games["week"] <= int(week)]

# Create a list of all team names.
teams = season_gamelogs["tm_name"].unique()


# Create a dictionary storing points for and points against data per team.
def create_team_points_dict(teams):
    nfl_points_dict = {}

    for team in teams:
        nfl_points_dict[team] = {}
        nfl_points_dict[team]["points_for"] = {}
        nfl_points_dict[team]["points_against"] = {}
        nfl_points_dict[team]["avg_points_for"] = []
        nfl_points_dict[team]["avg_points_against"] = []

    return nfl_points_dict


# Goes through each team and calculates their average points for and points against across all weeks.
def calculate_avg_points(teams, nfl_points_dict):
    for team in teams:
        weeks = list(nfl_points_dict[team]["points_for"].keys())

        points_for = []
        points_against = []

        for week in weeks:
            points_for.append(nfl_points_dict[team]["points_for"][week])
            points_against.append(nfl_points_dict[team]["points_against"][week])

        nfl_points_dict[team]["avg_points_for"] = np.average(points_for)
        nfl_points_dict[team]["avg_points_against"] = np.average(points_against)


# Calculates the median points for and points against across the league.
def calculate_league_medians(teams, nfl_points_dict):
    for team in teams:
        weeks = list(nfl_points_dict[team]["points_for"].keys())

        avg_points_for = []
        avg_points_against = []

        for week in weeks:
            avg_points_for.append(nfl_points_dict[team]["avg_points_for"][week])
            avg_points_against.append(nfl_points_dict[team]["avg_points_against"][week])

    return np.median(avg_points_for), np.median(avg_points_against)


def images(dict, xcol, ycol, graph_name):
    for team in dict.keys():
        arr_img = plt.imread(
            "/Users/loganfries/iCloud/SportsAnalytics/NFL/Logos/{team}.png".format(
                team=team
            )
        )
        imagebox = OffsetImage(arr_img, zoom=0.04)
        ab = AnnotationBbox(
            imagebox, (dict[team][xcol], dict[team][ycol]), frameon=False
        )
        graph_name.add_artist(ab)


nfl_points_dict = create_team_points_dict(teams)

# Iterate through each game and add the points for and points against data to the dictionary.

for indx, game in completed_games.iterrows():
    # Creates variables for the names of the listed team and their opponent.
    team_name = game["tm_name"]
    opponent_team_name = game["opp_name"]

    week = game["week"]

    # Creates variables for the listed teams score and their opponents scores.
    team_score = game["tm_score"]
    opponent_score = game["opp_score"]

    # Adds the points for and points against data to the dictionary.
    nfl_points_dict[team_name]["points_for"][
        "Week {week}".format(week=week)
    ] = team_score
    nfl_points_dict[team_name]["points_against"][
        "Week {week}".format(week=week)
    ] = opponent_score

    nfl_points_dict[opponent_team_name]["points_for"][
        "Week {week}".format(week=week)
    ] = opponent_score
    nfl_points_dict[opponent_team_name]["points_against"][
        "Week {week}".format(week=week)
    ] = team_score

calculate_avg_points(teams, nfl_points_dict)

dimensions = (7, 7)
fig, ax = plt.subplots(figsize=dimensions)

for team in teams:
    ax.scatter(
        nfl_points_dict[team]["avg_points_for"],
        nfl_points_dict[team]["avg_points_against"],
        label=team,
    )
