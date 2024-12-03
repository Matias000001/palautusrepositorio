from statistics import Statistics
from player_reader import PlayerReader
from matchers import And, HasAtLeast, PlaysIn, Not, All, HasFewerThan, Or

class QueryBuilder:
    def __init__(self, matcher=All()):
        self._matcher = matcher

    def plays_in(self, team):
        # Lisää PlaysIn-matcher nykyiseen ehtoon And-operaatiolla
        return QueryBuilder(And(self._matcher, PlaysIn(team)))

    def has_at_least(self, value, attr):
        # Lisää HasAtLeast-matcher nykyiseen ehtoon And-operaatiolla
        return QueryBuilder(And(self._matcher, HasAtLeast(value, attr)))

    def has_fewer_than(self, value, attr):
        # Lisää HasFewerThan-matcher nykyiseen ehtoon And-operaatiolla
        return QueryBuilder(And(self._matcher, HasFewerThan(value, attr)))

    def one_of(self, *matchers):
        # Luo Or-matcher annetuista matchereista
        return QueryBuilder(Or(*matchers))

    def build(self):
        # Palauttaa lopullisen matcher-objektin
        return self._matcher


def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2023-24/players.txt"
    reader = PlayerReader(url)
    stats = Statistics(reader)

    query = QueryBuilder()

    matcher = (
    query
      .one_of(
        query.plays_in("PHI")
            .has_at_least(10, "assists")
            .has_fewer_than(10, "goals")
            .build(),
        query.plays_in("EDM")
            .has_at_least(50, "points")
            .build()
      )
      .build()
    )

    for player in stats.matches(matcher):
       print(player)

if __name__ == "__main__":
    main()
