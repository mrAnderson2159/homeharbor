#!/bin/zsh
# Esegui
cd backend
python3 venv venv
source venv
pip3 install .
cd ..
npm install
cd frontend
npm install
cd ..
npm start
