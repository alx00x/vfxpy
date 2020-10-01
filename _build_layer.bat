@echo off

pushd %~dp0

echo Removing layer.zip
rm dist/layer.zip
7z a dist/layer.zip ./build/* -xr!__pycache__
