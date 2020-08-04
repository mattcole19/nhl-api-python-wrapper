"""
Using this file to get used to the nhl api with Python
Unofficial documentation: https://gitlab.com/dword4/nhlapi
Base URL: https://statsapi.web.nhl.com/api/v1/
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
    teams = {"New Jersey Devils": "1", " ": ""}

    def __init__(self, name):
        self.name = name
        self._id = self.teams[name]

    @property
    def team_url(self):
        return f"{self.base_url}{self._id}"

    def get_team(self):
        pass

    def get_roster(self, season=None):
        """
        Obtains the team roster
        :return:
        """
        if season:
            r = requests.get(f'{self.team_url}?expand=team.roster&season={season}')
        else:
            r = requests.get(f'{self.team_url}?expand=team.roster')

        return r.text

    def get_stats(self, season=None):
        """
        Obtains the team stats
        :return:
        """
        if not season:
            r = requests.get(f'{self.team_url}?expand=team.stats&season={season}')
        else:
            r = requests.get(f'{self.team_url}?expand=team.stats')

        return r.json()

    def get_next_game(self):
        """
        Obtains the details of the next game to be played
        :return:
        """
        r = requests.get(f'{self.team_url}?expand=team.schedule.next')
        return r.text

    def get_prev_game(self):
        """
        Obtains the details of the previous game played
        :return:
        """
        r = requests.get(f'{self.team_url}?expand=team.schedule.previous')
        return r.text

    def get_powerplay_goals(self, season):
        """
        Obtains the powerplay goals for a given season
        :param season:
        :return:
        """
        stats = self.get_stats(season=season)
        print(stats)

    def get_powerplay_percentage(self, season):
        """
        Obtains the powerplay percentage for a given season
        :return:
        """
        pass

    def get_stat(self, stat=None, season=None):
        if not stat:
            # TODO: Raise an error
            print(f'No stat passed in')
        else:
            r = self.get_stats(season=season)
            #print(r)
            desired_stat = r["teams"][0]["teamStats"][0]["splits"][0]["stat"][stat]
            return desired_stat





class Player:
    """
    Obtain player specific data
    """
    base_url = 'https://statsapi.web.nhl.com/api/v1/people/'

    def __init__(self, player_id):
        self._id = player_id

    @property
    def player_url(self):
        return f'{self.base_url}{self._id}'

    def get_stats(self, season=None):
        if season:
            return f'{self.player_url}/stats?season={season}'
        else:
            return f'{self.player_url}/stats'

# Tests
devils = Team(name="New Jersey Devils")
#(devils.get_roster(season="19921993"))
#print(devils.get_stats())

#