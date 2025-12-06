class User:
    def __init__(self, uid: str = '504485', username: str = 'nchskl'):
        self.username = username
        self.uid = uid

    @property
    def username(self) -> str:
        return self.__username

    @username.setter
    def username(self, username: str):
        if not isinstance(username, str):
            raise TypeError("Username must be a string.")
        if username == "":
            raise ValueError("Username cannot be empty.")
        self.__username = username.strip()

    @property
    def uid(self) -> str:
        return self.__uid

    @uid.setter
    def uid(self, uid: str):
        if not isinstance(uid, (int, str)):
            raise TypeError("ID must be a string.")
        if int(uid) < 0 or int(uid) > 999999:
            raise ValueError("ID must be a non-negative integer and less than 999,999")
        self.__uid = str(uid).zfill(6)
