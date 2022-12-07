from wolf_sheep.server import server
import os

if (os.path.exists ("res.txt")):
    	os.system ("rm res.txt")

server.launch()
