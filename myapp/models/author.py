class Author:
    def __init__(self, name: str = 'Fedorov V.', group: str = 'P3120'):
        self.name = name
        self.group = group

    @staticmethod
    def _validate_string(value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"'{value}' is not a string.")
        if value == "":
            raise ValueError("String cannot be empty.")
        if len(value) > 100:
            raise ValueError("String length cannot exceed 100 characters.")

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str):
        name = name.strip()
        self._validate_string(name)
        self.__name = name
    @property
    def group(self) -> str:
        return self.__group

    @group.setter
    def group(self, group: str):
        group = group.strip()
        self._validate_string(group)
        self.__group = group
