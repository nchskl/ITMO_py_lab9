class Author:
    def __init__(self, name: str = 'Fedorov V.', group: str = 'P3120'):
        self.name = name
        self.group = group

    @staticmethod
    def _validate_string(value: str) -> bool:
        if not isinstance(value, str):
            raise TypeError(f"'{value}' is not a string.")
        if value == "":
            raise ValueError("String cannot be empty.")
        if len(value) > 100:
            raise ValueError("String length cannot exceed 100 characters.")
        return True

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        name = name.strip()
        if self._validate_string(name):
            self._name = name

    @property
    def group(self) -> str:
        return self._group

    @group.setter
    def group(self, group: str):
        group = group.strip()
        if self._validate_string(group):
            self._group = group


a = Author()
print(a.name, a.group)
a.name = " Ivanov I. "
a.group = " P1234 "
print(a.name, a.group)