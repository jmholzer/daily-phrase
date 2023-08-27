import argparse
import json
from pathlib import Path
from typing import Dict, List

from models import Language, Phrase
from sqlalchemy.future.engine import Engine
from sqlmodel import Session, SQLModel, create_engine

DATABASE_LOCATION = Path(__file__).parent.resolve() / Path("db/daily_phrase.db")


def _parse_args():
    """
    Parse command line arguments.

    Returns:
        argparse.Namespace: An object holding all command-line provided arguments.
    """
    parser = argparse.ArgumentParser(description="Insert translations into a database.")
    parser.add_argument(
        "--json", required=True, help="JSON file containing translations"
    )
    args = parser.parse_args()
    return args


def _load_json_data(json_file: str) -> List[Dict[str, str]]:
    """
    Load JSON data from a file and return a list of dictionaries.

    Args:
        json_file (str): Path to JSON file containing translations.

    Returns:
        List[Dict[str, str]]: List of dictionaries with translation data.
    """
    with open(json_file) as f:
        data = json.load(f)
    return data


def _create_db_engine() -> Engine:
    """
    Create and return a new SQLModel engine.

    Returns:
        Session: SQLAlchemy Session object.
    """
    return create_engine("sqlite:///" + str(DATABASE_LOCATION))


def _create_db_and_tables(engine: Engine, drop_existing: bool = False) -> None:
    """
    Create a new database and tables.
    """
    if drop_existing:
        SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)


def _load_phrases(
    engine: Engine,
    phrases: List[Dict[str, str]],
):
    """
    Insert phrases into a database table.

    Args:
        engine (Engine): SQLModel/SQLAlchemy Engine object.
        phrases (List[Dict[str, str]]): List of dictionaries with phrases data.
    """
    phrase_records = []
    for phrase in phrases:
        phrase_record = Phrase(
            foreign_language=Language[phrase["foreign_language"].upper()],
            native_language=Language[phrase["native_language"].upper()],
            foreign_phrase=phrase["foreign_phrase"],
            native_phrase=phrase["native_phrase"],
        )
        phrase_records.append(phrase_record)

    with Session(engine) as session:
        session.add_all(phrase_records)
        session.commit()


def main():
    """
    Main function of the script. It performs the following steps:
    1. Parse command line arguments.
    2. Load JSON data containing the phrases.
    3. Create a database engine.
    4. Create the database and tables.
    5. Insert the phrases into the database.
    """
    args = _parse_args()
    phrases = _load_json_data(args.json)
    engine = _create_db_engine()
    _create_db_and_tables(engine)
    _load_phrases(engine, phrases)


if __name__ == "__main__":
    main()
