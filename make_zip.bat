@echo off

pushd %~dp0

echo Removing app.zip
rm app.zip
7z a app.zip generate.py client_secret.json src/ -xr!__pycache__
cd .Python
7z a ../app.zip . -xr!__pycache__
cd ..

pause
