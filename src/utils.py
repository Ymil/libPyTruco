def get_response(actions_maps, callback, *args):
    """
        Ejecuta las consultas hasta que optiene una respuesta correcta
    """
    while 1:
        accion_name, accion_values = callback(*args)
        if accion_name in actions_maps:
            return accion_name, accion_values
