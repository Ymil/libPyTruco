#/usr/bin/sh
echo "" > logs/accionGame.log
python example.py -m pdb 2> logs/erros.logs
cat logs/accionGame.log | grep -i debug > logs/accionGameDebug.log
