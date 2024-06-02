#!/bin/bash

mkdir pyinstaller
cd pyinstaller
pyinstaller --noconfirm --onefile --console --name "WTFinances" --add-data "../execonfig.json:." --add-data "../data:data/" --add-data "../application/web/templates:templates/" --add-data "../application/web/static:static/" "../mainexe.py"