from abc import ABC


class State(ABC):
    _state = 0
    _state_end = None

    def _last_state_eq_new_state(self, new_state):
        return self._state == new_state

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        if self._state == self._state_end:
            raise KeyError("No se puede cambiar de estatus")
        if new_state >= self._state:
            self._state = new_state
        else:
            raise ValueError("No se puede cantar ahora")