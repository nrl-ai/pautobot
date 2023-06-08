import os

DATA_ROOT = os.path.abspath(
    os.path.join(os.path.expanduser("~"), "pautobot-data")
)
DATABASE_PATH = os.path.abspath(os.path.join(DATA_ROOT, "pautobot.db"))
