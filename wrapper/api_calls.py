"""
Using this file to get used to the nhl api with Python
Unofficial documentation: https://gitlab.com/dword4/nhlapi
Base URL: https://statsapi.web.nhl.com/api/v1/
Some NHL data analyses examples: https://hockey-graphs.com/category/data-analysis/
Kaggle Data: https://www.kaggle.com/martinellis/nhl-game-data?select=team_info.csv
"""
import requests
import json


# url = "https://statsapi.web.nhl.com"
# r = requests.get("https://statsapi.web.nhl.com/api/v1/teams")

class Team:
    """
    Obtain team specific data
    """

    base_url = "https://statsapi.web.nhl.com/api/v1/teams/"

    def __init__(self, team_id):
        self._id = team_id

    @property
    def team_url(self):
        return f"{self.base_url}{self._id}"

    @property
    def team_id(self):
        return self._id

    def get_info(self):
        r = requests.get(f'{self.team_url}')
        return r.json()

    def get_name(self):
        data = self.get_info()["teams"][0]["name"]
        return data

    def get_roster(self, season=None):
        """
        Obtains the team roster
        :return:
        """
        if season:
            r = requests.get(f'{self.team_url}?expand=team.roster&season={season}')
        else:
            r = requests.get(f'{self.team_url}?expand=team.roster')

        return r.json()

    def get_stats(self, season=None):
        """
        Obtains the team stats
        :return:
        """
        if season:
            r = requests.get(f'{self.team_url}?expand=team.stats&season={season}')
        else:
            r = requests.get(f'{self.team_url}?expand=team.stats')

        return r.json()

    def get_game_ids(self, season):
        """
        Obtains all game_ids for a team for a given season
        :param season:
        :param teamId:
        :return:
        """
        r = requests.get(f"https://statsapi.web.nhl.com/api/v1/schedule?teamId={self._id}&season={season}")
        if r.status_code != 200:
            # TODO: Raise some sort of error
            return []
        game_ids = [game["gamePk"] for date in r.json()["dates"] for game in date["games"]]
        return game_ids

    def get_games_against(self, opposing_teamID, season):
        """
        Obtains all game ids for games against another specified team for a given season
        :param opposing_teamID:
        :param season:
        :return:
        """
        game_ids = []
        for game_id in self.get_game_ids(season=season):
            game = Game(game_id=game_id)
            teams = game.get_teams()
            away_team = teams["away"]["team"]["id"]
            home_team = teams["home"]["team"]["id"]

            if (away_team == opposing_teamID) or (home_team == opposing_teamID):
                game_ids.append(game_id)

        return game_ids

    def get_next_game(self):
        """
        Obtains the details of the next game to be played
        :return:
        """
        r = requests.get(f'{self.team_url}?expand=team.schedule.next')
        return r.json()

    def get_prev_game(self):
        """
        Obtains the details of the previous game played
        :return:
        """
        r = requests.get(f'{self.team_url}?expand=team.schedule.previous')
        return r.json()

    def get_powerplay_percentage(self, season):
        """
        Obtains the powerplay percentage for a given season
        :return:
        """
        pass

    def get_stat(self, stat=None, season=None):
        """
        Obtains a specific stat for a specific season
        :param stat: Choose one of the following: ['gamesPlayed', 'wins', 'losses', 'ot', 'pts', 'ptPctg', 'goalsPerGame', 'goalsAgainstPerGame', 'evGGARatio', 'powerPlayPercentage', 'powerPlayGoals', 'powerPlayGoalsAgainst', 'powerPlayOpportunities', 'penaltyKillPercentage', 'shotsPerGame', 'shotsAllowed', 'winScoreFirst', 'winOppScoreFirst', 'winLeadFirstPer', 'winLeadSecondPer', 'winOutshootOpp', 'winOutshotByOpp', 'faceOffsTaken', 'faceOffsWon', 'faceOffsLost', 'faceOffWinPercentage', 'shootingPctg', 'savePctg']
        :param season:
        :return:
        """
        if not stat:
            # TODO: Raise an error
            print(f'No stat passed in')
        else:
            r = self.get_stats(season=season)
            desired_stat = r["teams"][0]["teamStats"][0]["splits"][0]["stat"][stat]
            return desired_stat


class Player:
    """
    Obtain player specific data
    """
    base_url = 'https://statsapi.web.nhl.com/api/v1/people/'
    players = {"Letang": "8471724"}

    def __init__(self, player_id):
        self._id = player_id

    @property
    def player_url(self):
        return f'{self.base_url}{self._id}'

    def get_info(self):
        """
        Obtains basic information on the player
        :return:
        """
        r = requests.get(f'{self.player_url}')
        return r.json()

    def get_stats(self, season=None, split="statsSingleSeason"):
        """
        Obtains statistics for the player on a given split. If a season is not specified, it gives the statistics for all seasons
        :param season:
        :param split: Choose one of the following: [statsSingleSeason, homeAndAway, winLoss, byMonth, byDayOfWeek, vsDivision, vsConference, vsTeam, gameLog, regularSeasonStatRankings, goalsByGameSituation]
        :return:
        """
        if season:
            modifier = f'?stats={split}'
            r = requests.get(f'{self.player_url}/stats{modifier}&season={season}')
        else:
            r = requests.get(f'{self.player_url}/stats?stats=yearByYear')

        return r.json()

    def get_stat(self, stat, season):
        """
        Obtains a specific stat for the player for a given season
        :param stat:
        :param season:
        :return:
        """
        r = self.get_stats(season=season)
        return r["stats"][0]["splits"][0]["stat"][stat]


class Game:
    """ 
    Obtain statistics for a particular game
    """

    base_url = 'https://statsapi.web.nhl.com/api/v1/game/'

    def __init__(self, game_id):
        self._game_id = game_id

    @property
    def game_url(self):
        return f'{self.base_url}{self._game_id}'

    def get_boxscore(self):
        """
        Obtains the boxscore for a given game
        """
        r = requests.get(f'{self.game_url}/boxscore')
        return r.json()

    def get_teams(self):
        """
        Obtains the home and away team for the game
        """
        data = self.get_boxscore()
        return data["teams"]

    def get_players(self, home=True):
        """
        Obtains the players that played in the game
        :param home: boolean
        """
        if home:
            return self.get_teams()["home"]["players"]
        else:
            return self.get_teams()["away"]["players"]

    def get_coaches(self, home=True):
        """
        Obtains the coaches for the game
        """
        if home:
            return self.get_teams()["home"]["coaches"]
        else:
            return self.get_teams()["away"]["coaches"]


NJD = Team(team_id=1)
NYI = Team(team_id=2)
games = NJD.get_games_against(opposing_teamID=NYI.team_id, season="20172018")
print(games)


