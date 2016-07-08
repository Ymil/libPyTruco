import logging
class debugDecorate:
    def __captureReturn__(self,func, *args, **kwargs):
        logging.debug("Ejecutando funcion %s" % func.__name__)
        returnFuncion = "Retorno", func
        logging.debug(returnFuncion)
