:py:mod:`pyTrucoLib.state`
==========================

.. py:module:: pyTrucoLib.state


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pyTrucoLib.state.State




.. py:class:: State

   Bases: :py:obj:`abc.ABC`

   Helper class that provides a standard way to create an ABC using
   inheritance.

   .. py:attribute:: _state
      :annotation: = 0

      

   .. py:attribute:: _state_end
      

      

   .. py:attribute:: _freeze
      :annotation: = False

      

   .. py:method:: change_status_condicional(self, new_state)

      Se define la condicion para cambiar de status


   .. py:method:: freeze(self)


   .. py:method:: state(self)
      :property:



