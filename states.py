import json
import logging

from singleton import Singleton
from collections import deque
from db import DB


# class States(metaclass=Singleton):
#     __default_states = "states.json"

#     def __init__(self):
#         self.__states = {}

#     def __call__(self, chat_id: int):
#         while chat_id not in self.__states:
#             try:
#                 with open(f'states/{chat_id}.json') as f:
#                     self.__states[chat_id] = json.load(f)

#             except FileNotFoundError:
#                 shutil.copy(States.__default_states,
#                             f'states/{chat_id}.json')

#         return self.__states[chat_id]

#     def save(self, chat_id: int):
#         if chat_id not in self.__states:
#             raise IndexError(f"Wrong chat_id {chat_id}")
#         with open(f'states/{chat_id}.json', "w") as f:
#             json.dump(self.__states[chat_id], f)


class States(metaclass=Singleton):
    __default_states = "states.json"
    MAX_STATES = 200

    def __init__(self, db: DB):
        self.__states = deque()
        self.db = db

    def __call__(self, chat_id: int):
        if (arr := [s[1] for s in self.__states if s[0] == chat_id]):
            return arr[0]   

        states = self.db.getById("states", chat_id)
        logging.info(f"STATES:: {states}")
        if not states:
            with open(States.__default_states) as f:
                states = json.load(f)
                self.db.setById(chat_id, states=states)
        self.__states.append((chat_id, states))
        if len(self.__states) > States.MAX_STATES:
            self.__states.popleft()
        return states

    def save(self, chat_id: int):
        if chat_id not in [s[0] for s in self.__states]:
            raise IndexError(f"Wrong chat_id {chat_id}")
        self.db.setById(
            chat_id, states=[s[1] for s in self.__states if s[0] == chat_id][0]
        )
