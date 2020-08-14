"""
A test script to run some of the functions I created. The goal of this script is to run some data
analysis using NHL data and to give me ideas of what to add to my wrapper
"""
import requests
from api_calls import Team, Player, Game


def get_game_ids(season, teamId):
    """
    Obtains all game_ids for a team for a given season
    :param season:
    :param teamId:
    :return:
    """
    r = requests.get(f"https://statsapi.web.nhl.com/api/v1/schedule?teamId={teamId}&season={season}")
    if r.status_code != 200:
        # TODO: Raise some sort of error
        return []
    game_ids = [game["gamePk"] for date in r.json()["dates"] for game in date["games"]]
    return game_ids

def main():
    games20162017 = get_game_ids(season="20172018", teamId=5)
    print(games20162017)
    #print(games20162017)
    # x = 6
    print(Team)

if __name__ == "__main__":
    main()

