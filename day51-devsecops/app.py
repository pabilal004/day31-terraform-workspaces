import os

DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

def connect_database():
    if not DATABASE_PASSWORD:
        print("Database password is not configured!")
        return

    print("Database password is configured.")
