from pathlib import Path

DATABASE_LOCATION = (Path(__file__).parent / Path("db/daily_phrase.db")).resolve()
print(DATABASE_LOCATION)
