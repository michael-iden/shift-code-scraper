from dataclasses import dataclass
from os import listdir, path
from os.path import isfile, join


DIRNAME = path.dirname(__file__)
CREDENTIALS_PATH = path.join(DIRNAME, '../creds/')


def build_users():
    users = []

    users_files = [join(CREDENTIALS_PATH, f) for f in listdir(CREDENTIALS_PATH) if isfile(join(CREDENTIALS_PATH, f)) and '.txt' in f]
    for user_file in users_files:
        with open(user_file) as user_reader:
            file_lines = user_reader.read().splitlines()
            users.append(User(file_lines[0], file_lines[1], file_lines[2]))

    return users


@dataclass
class User:
    name: str
    email: str
    password: str
