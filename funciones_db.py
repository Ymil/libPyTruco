def obtener_cartas_jugadoid(jugadorID)
    query = "select nombre, cartas_jugador.cartas from jugador cross join cartas_jugador on cartas_jugador.id = jugador.cartasid where jugador.id = %d" % jugadorID
