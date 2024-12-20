class Or:
   def __init__(self, *matchers):
        self._matchers = matchers

   def test(self, player):
        for matcher in self._matchers:
            if matcher.test(player):
                return True
        return False

class And:
    def __init__(self, *matchers):
        self._matchers = matchers

    def test(self, player):
        for matcher in self._matchers:
            if not matcher.test(player):
                return False
        return True

class HasFewerThan:
    def __init__(self, value, attr):
        self._value = value
        self._attr = attr

    def test(self, player):
        player_value = getattr(player, self._attr)
        return player_value < self._value

class Not:
    def __init__(self, matcher):
        self._matcher = matcher

    def test(self, player):
        return not self._matcher.test(player)

class All:
    def __init__(self, *matchers):
        self._matchers = matchers

    def test(self, player):
        return all(matcher.test(player) for matcher in self._matchers)

class PlaysIn:
    def __init__(self, team):
        self._team = team.lower().strip()

    def test(self, player):
        player_teams = [t.lower().strip() for t in player.team.split(",")]
        return self._team in player_teams

class HasAtLeast:
    def __init__(self, value, attr):
        self._value = value
        self._attr = attr

    def test(self, player):
        player_value = getattr(player, self._attr)

        return player_value >= self._value
