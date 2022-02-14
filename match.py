class Match:
    def __init__(self, team1, team2, dateTime, link, campName):
        self.team1 = team1
        self.team2 = team2
        self.dateTime = dateTime
        self.link = link
        self.campName = campName


def has_brazilian_team(match: Match):
    return match.team1.isBrazilian or match.team2.isBrazilian
