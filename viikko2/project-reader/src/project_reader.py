from urllib import request
from project import Project
import tomli

class ProjectReader:
    def __init__(self, url):
        self._url = url

    def get_project(self):

        # Hae TOML-tiedoston sisältö URL:sta
        content = request.urlopen(self._url).read().decode("utf-8")

        # Parsitaan TOML-data Pythonin tietorakenteeksi
        toml_data = tomli.loads(content)

        # Poimitaan tarvittavat tiedot
        name = toml_data["tool"]["poetry"]["name"]
        description = toml_data["tool"]["poetry"].get("description", "")
        license = toml_data["tool"]["poetry"].get("license", "N/A")
        authors = toml_data["tool"]["poetry"].get("authors", [])
        dependencies = list(toml_data["tool"]["poetry"]["dependencies"].keys())
        dev_dependencies = list(toml_data["tool"]["poetry"]["group"]["dev"]["dependencies"].keys())

        # Luodaan Project-olio
        project = Project(name, description, dependencies, dev_dependencies, license, authors)

        return project
