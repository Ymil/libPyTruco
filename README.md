# libPyTruco
Motor de truco argentino echo en python

## Instalando localmente

``` pip install -e .```

## Generando la documentación

### Instalar 
```
pip install sphinx-autodoc-typehints sphinx-rtd-theme sphinx-autoapi sphinx
```

### Compilando la documentación

```
cd docs
./make.bat html
```

## Ejecutando test

### Requirimientos

```
pip install coverage unittest
```

### Ejecutando

```
coverage run -m unittest && coverage html
```
## Ejemplos

Se puede observar los ejemplos en la carpeta `example`
