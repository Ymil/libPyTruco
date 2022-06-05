from pyTrucoLib.actions.truco_actions import TRUCO_ACTIONS


def actions_truco_filter(action, player, actions):
    """
        Esta funcion filtra las acciones de truco para el equipo que no le
        corresponde.
    """
    truco_quiero_expected = action.GM.truco_manager.quiero_expected
    truco_cantado = action.GM.truco_manager.cantado
    truco_quiero_player = action.GM.truco_manager.quiero_player
    if not truco_quiero_expected and truco_cantado and \
            truco_quiero_player is not player:
        return actions - TRUCO_ACTIONS
    return actions


def actions_to_str(actions):
    return list(map(lambda c: c.name(), actions))


def get_action(action, player) -> None:
    """
        Se reciben las acciones desde los jugadores y se envian a la clase
        con el nombre de la acción.

        Cada accion sabe que puede responder el jugador, y eso limita las
        posibilidades.

        Si el usuario no ingresa un opcion valida se vuelve a solicitar de
            forma recursiva.

        :param action: instancia Action que llama a la funcion
        :param player: jugador que debe responder a la accion
        :rtype: None
    """
    actions = actions_truco_filter(
        action, player, action.get_availables_actions(),
    )
    actions_str = actions_to_str(actions)

    input_ = action.GM.signals.get_action(player, actions_str)
    if ',' in input_:
        action_name, action_value = input_.split(',')
    else:
        action_name, action_value = (input_, None)

    if action_name in actions_str:
        new_action = action.get_action_from_name(action_name)
        action = new_action(action, player)
        return action.execute(action_value)
    else:
        return get_action(action, player)
