import re


class App:
    def __init__(self, name: str = "Daily Currencies", version: str = "1.0.0", author: str = "Fedorov V."):
        self.name = name
        self.version = version
        self.author = author

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        if name == "":
            raise ValueError("Name cannot be empty.")
        self.__name = name.strip()

    @property
    def version(self):
        return self.__version

    @version.setter
    def version(self, version: str):
        if not isinstance(version, str):
            raise TypeError("Version must be a string.")
        if version == "":
            raise ValueError("Version cannot be empty.")
        if not re.match(r"^(\d{1,2})\.(\d{1,2})\.(\d{1,2})$", version.strip()):
            raise ValueError("The version must be in the numb.numb.numb format and be between 0 and 99.")
        self.__version = version.strip()

    @property
    def author(self):
        return self.__author

    @author.setter
    def author(self, author: str):
        if not isinstance(author, str):
            raise TypeError("Author must be a string.")
        if author == "":
            raise ValueError("Author cannot be empty.")
        self.__author = author.strip()
