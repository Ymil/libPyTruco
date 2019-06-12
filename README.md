# libPyTruco
Motor de truco argentino echo en python


-------------------- 24/08/2016 ------------------------


*Se añadio la busqueda de un equipo ganador al finalizar cada ronda en juego.py

*Se arregla el bug de las cartas repetidas con prepararMaso en la clase cartas.

*Se agregar mensajes de debug y info en accionesJuego.py para poder analizar las simulaciones

*Se crea el directorio langs para cargar los distintos lenguajes

*Se verifica el correcto funcionamiento y se libera como version estable v0.1 sin cantos (envido y truco)

----- 
* Para realizar un ejemplo del funcionamiento, ejecutar python example.py
* El archivo accionesJuego.py es la interface entre el servidor y los usuarios, desde este lugar se deberian ejecutar los comandos a enviar al cliente.
* El archivo accionesJuego.py tiene configurado un randm a la hora de solicitar una carta al jugador.