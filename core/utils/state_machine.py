from aiogram.fsm.state import StatesGroup, State


class SaveSteps(StatesGroup):
    LVL1_TO_2 = State()
    LVL2_TO_3 = State()
    TIME_INTERVAL = State()
    WAIT_DATE = State()
    GET_SEARCH = State()
    SEND_PROBLEM = State()
    GET_TECH_REPLY = State()
