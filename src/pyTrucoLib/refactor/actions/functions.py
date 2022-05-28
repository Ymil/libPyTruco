from pyTrucoLib.refactor.actions.truco_actions import TRUCO_ACTIONS


def actions_truco_filter(action, player, actions):
    truco_quiero_expected = action.truco_manager.quiero_expected
    truco_cantado = action.truco_manager.cantado
    truco_quiero_player = action.truco_manager.quiero_player
    if not truco_quiero_expected and truco_cantado and \
         truco_quiero_player is not player:
            return actions - TRUCO_ACTIONS
    return actions


def actions_to_str(actions):
    return list(map(lambda c: c.name(), actions))


def get_action(action , player) -> None:
    actions = actions_truco_filter(action, player, action.get_availables_actions())
    actions_str = actions_to_str(actions)

    input_ = action.signals.getActionPlayer(player, actions_str)
    if "," in input_:
        action_name, action_value = input_.split(",")
    else:
        action_name, action_value = (input_, None)

    if action_name in actions_str:
        new_action = action.get_action_from_name(action_name)
        action = new_action(action, player)
        return action.execute(action_value)
    else:
        return get_action(action, player)
