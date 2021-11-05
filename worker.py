# CREATED BY JOHN EARL COBAR

# custom imports
from Main.app_workers.steamapi import steam_worker
from Main.app_workers.epicgames import egs_worker
from Main.app_workers.pinger import pinger_worker
from Main.database.database import expiry_worker

# lib imports
import threading

# THREADS INIT
steam_t = threading.Thread(target=steam_worker)
egs_t = threading.Thread(target=egs_worker)
ping_t = threading.Thread(target=pinger_worker)
exp_t = threading.Thread(target=expiry_worker)

############## RUN THREADS #######################

# THREADS START
steam_t.start()
egs_t.start()
ping_t.start()
exp_t.start()

# THREADS JOIN
steam_t.join()
egs_t.join()
ping_t.join()
exp_t.join()
