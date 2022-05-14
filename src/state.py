from abc import ABC


class State(ABC):
    _state = 0
    _state_end = None
    _freeze = False

    def change_status_condicional(self, new_state):
        """
            Se define la condicion para cambiar de status
        """
        return new_state >= self._state

    def freeze(self):
        # Imposibilita los cambios de estado
        self._freeze = True

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        if self._state == self._state_end or self._freeze:
            raise KeyError('No se puede cambiar de estatus')
        if self.change_status_condicional(new_state):
            self._state = new_state
        else:
            raise ValueError('No se puede cantar ahora')
