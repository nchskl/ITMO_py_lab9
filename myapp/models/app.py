class App:
    def __init__(self, name: str = "Daily Currencies", version: str = "1.0.0", author: str = "Fedorov V."):
        self.name = name
        self.version = version
        self.author = author

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        if name == "":
            raise ValueError("Name cannot be empty.")
        self._name = name.strip()

