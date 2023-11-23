import nflscraPy
import nfl_data_py as nfl
import sys

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
        nfl_points_dict[team]["points_for"] = []
        nfl_points_dict[team]["points_against"] = []
        nfl_points_dict[team]["avg_points_for"] = []
        nfl_points_dict[team]["avg_points_against"] = []

    return nfl_points_dict


nfl_points_dict = create_team_points_dict(teams)
