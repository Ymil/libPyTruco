#/usr/bin/sh
echo "" > logs/accionGame.log
python example.py -m pdb 2> logs/erros.logs
cat logs/accionGame.log | tee >(grep -i debug > logs/accionGame.debug) >(grep -i info > logs/accionGame.info) "$@" > /dev/null
