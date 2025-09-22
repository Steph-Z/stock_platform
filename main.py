#This file serves as the entry point for hosting the dashboard
#It is minimal.

import os 
from src.app.app import app

server = app.server

if __name__ == '__main__':
    app.run(debug= False)
    
    