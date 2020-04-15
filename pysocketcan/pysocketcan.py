from time import sleep
from enum import Enum
from subprocess import CalledProcessError

from . import scripts


class State(Enum):
    UP = 1
    DOWN = 0


class Mode(Enum):
    ON = 1
    OFF = 0
    LOOP = "LOOPBACK"
    LISTEN = "LISTEN-ONLY"
    TRIPLE = "TRIPLE-SAMPLING"


class Filter:
    pass


class Interface:
    def __init__(self, id="can0"):
        self.id = id

    @property
    def state(self):
        return scripts.get_states(self.id)

    @state.setter
    def state(self, s_name):
        scripts.set(self.id, s_name.name.lower())

    def on(self):
        self.state = State.UP

    def off(self):
        self.state = State.DOWN

    def reset(func):
        def wrapper(self, *args, **kwargs):
            self.off()
            if callable(func):
                func(self, *args, **kwargs)
            self.on()

        return wrapper if callable(func) else wrapper(func)

    @property
    def baud(self):
        return scripts.get_baud(self.id)

    @baud.setter
    @reset
    def baud(self, rate):
        while self.state != "STOPPED":
            sleep(0.25)
        scripts.set_baud(self.id, rate)

    def send(self, can_id, data):
        scripts.send(self.id, can_id, data)

    def receive(self):
        return scripts.candump(self.id)

    def _check_mode(self, mode):
        status = self.status
        return Mode(mode.value in status if status else False)

    @reset
    def _mode(self, m_name, m_state):
        scripts.set(self.id, args_2=f"{m_name.value.lower()} {m_state.name.lower()}")

    @property
    def status(self):
        try:
            return scripts.get_modes(self.id)
        except CalledProcessError:
            return

    @property
    def loopback(self):
        return self._check_mode(Mode.LOOP)

    @loopback.setter
    def loopback(self, b: bool):
        self._mode(Mode.LOOP, Mode(b))

    @property
    def listen_only(self):
        return self._check_mode(Mode.LISTEN)

    @listen_only.setter
    def listen_only(self, b: bool):
        self._mode(Mode.LISTEN, Mode(b))

    @property
    def triple_sampling(self):
        return self._check_mode(Mode.TRIPLE)

    @triple_sampling.setter
    def triple_sampling(self, b: bool):
        self._mode(Mode.TRIPLE, Mode(b))
