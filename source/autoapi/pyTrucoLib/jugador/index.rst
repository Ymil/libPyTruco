:py:mod:`pyTrucoLib.jugador`
============================

.. py:module:: pyTrucoLib.jugador


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pyTrucoLib.jugador.Jugador




Attributes
~~~~~~~~~~

.. autoapisummary::

   pyTrucoLib.jugador.__author__
   pyTrucoLib.jugador.__email__
   pyTrucoLib.jugador.__status__


.. py:data:: __author__
   :annotation: = Lautaro Linquiman

   

.. py:data:: __email__
   :annotation: = acc.limayyo@gmail.com

   

.. py:data:: __status__
   :annotation: = Developing

   

.. py:class:: Jugador(id)

   .. py:method:: setTeam(self, teamObject)

      :param teamObject:


   .. py:method:: getTeam(self)

      :return: equipo del jugador
      :rtype: teamObject 


   .. py:method:: getTeamID(self)

      :return: ID del equipo del jugador
      :rtype: int 


   .. py:method:: setName(self, nombre)

      Asgina el nombre del jugador
      :param nombre: str 


   .. py:method:: getName(self)

      Devuelve el nombre del jugador
      :rtype: str


   .. py:method:: getID(self)

      :return: ID del jugador
      :rtype: int


   .. py:method:: setCards(self, cartas)

      Se ingresan la cartas que les da el juego
      :param cartas: list cardObjects


   .. py:method:: resetCards(self)

      Se borran todas las cartas y variables cargadas que tenia el jugador
              


   .. py:method:: playingCardInRound(self, cartaID)

      Corrobora que las cartas del jugador sea valida y la juega
      :param cartaID: int
      :rtype: bool


   .. py:method:: getCardsPlayer(self)

      Esta funcion devuelve todas las cartas del jugador en forma de areglo
      :return: lista de cardObject
      :rtype: list


   .. py:method:: getCardTheNumberHand(self, roundNumber)

      Devuelve la carta jugada en la mano x
      :param roundNumber: int
      :rtype: cardObject


   .. py:method:: getNameCardPlayed(self)

      Devuelve el nombre completa de la ultima carta jugada
      :return: Nombre completo de la carta
      :rtype: str


   .. py:method:: getMaxCard(self)

      group: player, envido
      Esta funcion devuelve la carta mayor del jugador (Para el envido)
      :return: points
      :rtype: int


   .. py:method:: getCardByStick(self, stick)

      group: player, envido
      Agrupa las cartas de un palo determinado
      :param stick: str
      :return: lista de cartas
      :rtype: list


   .. py:method:: getPointsEnvido(self)

      group: player, envido
      Esta funcion devuelve los puntos que tiene el jugador para el envido
      :return: points
      :rtype: int


   .. py:method:: setStatus(self, valor)

      Obsoleto ? 


   .. py:method:: getStatus(self)

      Obsoleto ? 



