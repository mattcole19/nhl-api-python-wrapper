"""
Unit tests
"""
import unittest
import requests
import random
from .api_calls import Team, Player


class TeamTests(unittest.TestCase):
    """
    Tests api calls for Team using the New Jersey Devils
    """

    def setUp(self):
        """

        :return:
        """
        self.base_url = "https://statsapi.web.nhl.com/api/v1/teams/"
        self.team_name = "New Jersey Devils"
        self.team_id = "1"
        self.team_url = f'{self.base_url}{self.team_id}'
        self.NJD = Team(name=self.team_name)
        self.seasons = ['20102011', '20112012', '20122013, 20152016, 20172018']

    def test_get_team(self):
        """
        Tests the get team function
        :return:
        """
        pass

    def test_get_roster(self):
        """
        Tests the get roster function
        :return:
        """
        r = requests.get(f'{self.team_url}?expand=team.roster')
        self.assertEqual(self.NJD.get_roster(), r.text)

    def test_get_stats(self):
        """
        Tests the get stats function
        :return:
        """

        # All seasons
        r = requests.get(f'{self.team_url}?expand=team.stats')
        self.assertEqual(self.NJD.get_stats(), r.json())

        # For a given season
        season = random.choice(self.seasons)
        r = requests.get(f'{self.team_url}?expand=team.stats&season={season}')
        self.assertEqual(self.NJD.get_stats(season=season), r.json())

    def test_get_stat(self):
        """
        Tests the get_stat function
        :return:
        """

        # Wins
        NJD_20162017_wins = 28
        self.assertEqual(self.NJD.get_stat(stat="wins", season="20162017"), NJD_20162017_wins)

        # Goals Per Game
        NJD_20162017_gpg = 2.195
        self.assertEqual(self.NJD.get_stat(stat="goalsPerGame", season="20162017"), NJD_20162017_gpg)


class PlayerTests(unittest.TestCase):
    """
    Tests api calls for Player using Kris Letang
    """
    def setUp(self):
        self.letang_id = "8471724"
        self.letang = Player(player_id=self.letang_id)
        self.player_url = "https://statsapi.web.nhl.com/api/v1/people/"

    def test_get_info(self):
        """
        Tests the get_info function
        :return:
        """
        r = requests.get(f'{self.player_url}/{self.letang_id}')
        self.assertEqual(self.letang.get_info(), r.json())

    def test_get_stats(self):
        """
        Tests the get_stats function
        :return:
        """
        # 20172018 stats
        r = requests.get(f'{self.player_url}/{self.letang_id}/stats?stats=statsSingleSeason&season=20172018')
        self.assertEqual(self.letang.get_stats(season="20172018"), r.json())

    def test_get_stat(self):
        """
        Tests the get_stat function
        :return:
        """
        letang_20162017_goals = 5
        self.assertEqual(self.letang.get_stat(stat="goals", season="20162017"), letang_20162017_goals)


if __name__ == "__main__":
    unittest.main()
