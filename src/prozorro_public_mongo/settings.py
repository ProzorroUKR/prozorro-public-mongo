import os


MONGODB_URL = os.environ.get("MONGODB_URL", "mongodb://root:example@localhost:27017")
MONGODB_DATABASE = os.environ.get("MONGODB_DATABASE", "prozorro-public")
MONGODB_COLLECTION = os.environ.get("MONGODB_COLLECTION", "tenders")
ERROR_INTERVAL = int(os.environ.get("ERROR_INTERVAL", 5))


USER_AGENT = os.getenv("USER_AGENT")
HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": USER_AGENT,
}
