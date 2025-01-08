import json
import shutil

from singleton import Singleton


class States(metaclass=Singleton):
    __default_states = "states.json"

    def __init__(self):
        self.__states = {}

    def __call__(self, chat_id: int):
        while chat_id not in self.__states:
            try:
                with open(f'states/{chat_id}.json') as f:
                    self.__states[chat_id] = json.load(f)

            except FileNotFoundError:
                shutil.copy(States.__default_states, f'states/{chat_id}.json')

        return self.__states[chat_id]

    def save(self, chat_id: int):
        if chat_id not in self.__states:
            raise IndexError(f"Wrong chat_id {chat_id}")
        with open(f'states/{chat_id}.json', "w") as f:
            json.dump(self.__states[chat_id], f)
