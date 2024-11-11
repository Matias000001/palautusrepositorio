class Project:
    def __init__(self, name, description, dependencies, dev_dependencies, license="N/A", authors=[]):
        self.name = name
        self.description = description
        self.dependencies = dependencies
        self.dev_dependencies = dev_dependencies
        self.license = license
        self.authors = authors

    def _stringify_dependencies(self, dependencies):
        return "\n".join(f"- {dep}" for dep in dependencies) if len(dependencies) > 0 else "-"

    def __str__(self):
        authors_str =  "\n".join(f"- {author}" for author in self.authors) if self.authors else "-"

        return (
            f"Name: {self.name}\n"
            f"Description: {self.description or '-'}\n"
            f"License: {self.license}\n\n" 
            f"Author:\n{authors_str}\n\n"
            f"Dependencies:\n{self._stringify_dependencies(self.dependencies)}\n\n"
            f"Development dependencies:\n{self._stringify_dependencies(self.dev_dependencies)}"
        )
