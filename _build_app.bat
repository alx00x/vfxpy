@echo off

pushd %~dp0

echo Removing app.zip
rm dist/app.zip
7z a dist/app.zip generate.py client_secret.json src/ -xr!__pycache__
