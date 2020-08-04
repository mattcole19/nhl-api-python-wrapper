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
        self.assertEqual(self.NJD.get_stats(), r.text)

        # For a given season
        season = random.choice(self.seasons)
        r = requests.get(f'{self.team_url}?expand=team.stats&season={season}')
        self.assertEqual(self.NJD.get_stats(season=season), r.text)

    # def test_get_powerplay_goals(self):
    #     """
    #     Tests the get_powerplay_goals function
    #     :return:
    #     """
    #     NJD_20162017_ppg = 44
    #     self.assertEqual(self.NJD.get_powerplay_goals(season="20162017"), NJD_20162017_ppg)
    #
    # def test_get_powerplay_percentage(self):
    #     """
    #     Tests the get_powerplay function
    #     :return:
    #     """
    #     NJD_20162017_ppp = 17.53  # New Jersey Devil's powerplay percentage for the 2016-2017 season
    #     self.assertAlmostEqual(self.NJD.get_powerplay_percentage(season="20162017"), NJD_20162017_ppp)

    def test_get_stat(self):
        """
        Tests the get_stat function
        :return:
        """
        NJD_20162017_wins = 28
        self.assertEqual(self.NJD.get_stat(stat="wins", season="20162017"), NJD_20162017_wins)


class PlayerTests(unittest.TestCase):
    """
    Tests api calls for Player using Sidney Crosby
    """
    def setUp(self):
        self.crosby_id = "8471724"
        self.crosby = Player(player_id=self.crosby_id)
        self.player_url = "https://statsapi.web.nhl.com/api/v1/people/"

    def test_get_stats(self):
        """
        Tests the get stats function
        :return:
        """
        pass




if __name__ == "__main__":
    unittest.main()
