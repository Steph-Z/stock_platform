#This file serves as the entry point for hosting the dashboard
#It is minimal.
#The main entry point for local development is in src/app/app.py
#For an easy workflow use Strg + g and then Strg +0 to collapse all blocks
#This way it is easy to navigate each file 
import os 
from src.app.app import app

server = app.server

if __name__ == '__main__':
    app.run(debug= False)
    
    