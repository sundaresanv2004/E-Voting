import json

loc_path = '.'


def read_file(path_file: str) -> dict:
    with open(loc_path + rf"/assets{path_file}", "r") as file:
        file_data: dict = json.load(file)
        file.close()
    return file_data


enc_data = read_file(r"/data/enc_data.json")
file_path = read_file(r"/data/file_path.json")
default_setting_data = read_file(r"/data/default_setting.json")
warnings = read_file(r"/messages/warning.json")
error_data = read_file(r"/messages/error.json")
messages = read_file(r"/messages/message.json")


# default_election_settings = read_file(r"/data/default_election_settings.json")


def read_txt_files(path_file: str) -> str:
    with open(loc_path + rf'/assets{path_file}', 'r') as file:
        file_data = file.read()
        file.close()

    return file_data


all_done_message = read_txt_files(r'/messages/all_done.txt')
firebase_project = read_txt_files(r'/messages/firebase_project.txt')
