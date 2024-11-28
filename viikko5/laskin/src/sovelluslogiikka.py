class Sovelluslogiikka:
    def __init__(self, arvo=0):
        self._arvo = arvo
        self._edellinen_arvo = arvo  # Tallennetaan edellinen arvo

    def miinus(self, operandi):
        self._edellinen_arvo = self._arvo  # Päivitetään edellinen arvo ennen laskentaa
        self._arvo = self._arvo - operandi

    def plus(self, operandi):
        self._edellinen_arvo = self._arvo  # Päivitetään edellinen arvo ennen laskentaa
        self._arvo = self._arvo + operandi

    def nollaa(self):
        self._edellinen_arvo = self._arvo  # Päivitetään edellinen arvo ennen nollaamista
        self._arvo = 0

    def aseta_arvo(self, arvo):
        self._edellinen_arvo = self._arvo  # Tallennetaan nykyinen arvo ennen päivitystä
        self._arvo = arvo

    def arvo(self):
        return self._arvo

    def edellinen_arvo(self):
        return self._edellinen_arvo  # Palautetaan edellinen arvo
