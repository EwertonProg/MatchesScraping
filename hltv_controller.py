from datetime import datetime

import pytz
import requests as requests
from bs4 import BeautifulSoup

from match import Match
from team import Team


class HltvController:
    brazilianTeams = [
        "00Nation",
        "Case",
        "FURIA",
        "GODSENT",
        "Last Dance",
        "Los Grandes",
        "MIBR",
        "paiN",
        "Sharks",
        "TeamOne"]

    def get_all_games(self):
        matches_day = self.__upcoming_matches()
        matches = []

        for match_day in matches_day:
            date = match_day.find("span", {'class': "matchDayHeadline"}).text.split()[-1]
            split_date = date.split("-")
            year = int(split_date[0])
            month = int(split_date[1])
            day = int(split_date[2])
            upcoming_matches = match_day.find_all("div", {'class': "upcomingMatch"})
            matches = matches + self.__build_matches(day, month, year, upcoming_matches)
        return matches

    def get_all_today_games(self):
        for match_day in self.__upcoming_matches():
            date = match_day.find("span", {'class': "matchDayHeadline"}).text.split()[-1]
            split_date = date.split("-")
            year = int(split_date[0])
            month = int(split_date[1])
            day = int(split_date[2])
            today = datetime.today()
            if year == today.year and month == today.month and day == today.day:
                upcoming_matches = match_day.find_all("div", {'class': "upcomingMatch"})
                matches = self.__build_matches(day, month, year, upcoming_matches)
                return matches

    def __upcoming_matches(self):
        url = 'https://www.hltv.org/matches'
        res = requests.get(url)
        html_page = res.text
        soup = BeautifulSoup(html_page, 'html.parser')
        return soup.find_all("div", {'class': "upcomingMatchesSection"})

    def __build_matches(self, day, month, year, upcoming_matches):
        matches = []
        for upcomingMatch in upcoming_matches:
            if "team1" in list(upcomingMatch.attrs.keys()):

                team2 = upcomingMatch.find("div", {'class': "matchTeam team2"})

                team2_name = team2.find("div", {'class': 'matchTeamName'})

                team1 = upcomingMatch.find("div", {'class': "matchTeam team1"})

                team1_name = team1.find("div", {'class': 'matchTeamName'}).text

                if team2_name is None:
                    team2_name = team2.find("div", {'class': 'team'}).text
                else:
                    team2_name = team2_name.text

                link: str = "https://www.hltv.org" + upcomingMatch.find("a", {"class": "match"}).attrs["href"]
                event_name = upcomingMatch.find("div", {"class": "matchEventName"}).text
                split_time = upcomingMatch.find("div", {'class': "matchTime"}).text.split(":")

                hour = int(split_time[0])
                minute = int(split_time[1])
                match = Match(team1=Team(name=team1_name, isBrazilian=team1_name in self.brazilianTeams),
                              team2=Team(name=team2_name, isBrazilian=team2_name in self.brazilianTeams),
                              link=link,
                              campName=event_name,
                              dateTime=datetime(year=year,
                                                month=month,
                                                day=day,
                                                hour=hour,
                                                minute=minute,
                                                tzinfo=pytz.FixedOffset(60)))
                matches.append(match)
        return matches
