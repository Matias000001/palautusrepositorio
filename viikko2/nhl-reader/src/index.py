import requests
from player import Player
from rich.console import Console
from rich.table import Table

def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2023-24/players"
    response = requests.get(url).json()

    players = []

    for player_dict in response:
        player = Player(player_dict)
        players.append(player)

    # Rich console ja taulukko
    console = Console()
    table = Table(title="NHL statistics by nationality")

    # Taulukon sarakkeet
    table.add_column("name", justify="left")
    table.add_column("team", justify="center")
    table.add_column("goals", justify="right")
    table.add_column("assists", justify="right")
    table.add_column("Pisteet", justify="right")

    # Lisätään suomalaiset pelaajat taulukkoon
    for player in players:
        if player.nationality == "FIN":
            table.add_row(player.name, player.team, str(player.goals), str(player.assists), str(player.goals + player.assists))

    # Tulostetaan taulukko
    console.print(table)

if __name__ == "__main__":
    main()
