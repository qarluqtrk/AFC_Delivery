from aiogram.dispatcher.filters import state


class MenuState(state.StatesGroup):
    categories = state.State()
    product = state.State()
    booking = state.State()


class Checkout(state.StatesGroup):
    cart = state.State()
    service_type = state.State()
    location = state.State()
    location_check = state.State()
    location_comment = state.State()
    payment = state.State()


