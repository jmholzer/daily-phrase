import json
import argparse
from typing import List, Dict
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import sessionmaker, Session
from pathlib import Path


DATABASE_LOCATION = Path(__file__).parent.resolve() / Path("db/daily_phrase.db")
print(DATABASE_LOCATION)


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


def _load_translations(
    session: Session,
    table: Table,
    phrases: List[Dict[str, str]],
):
    """
    Insert translations into a database table.

    Args:
        session (Session): SQLAlchemy Session object.
        table (Table): SQLAlchemy Table object.
        translations (List[Dict[str, str]]): List of dictionaries with translation data.
    """
    for phrase in phrases:
        foreign_language, native_language = phrase
        values = {
            "foreign_language": foreign_language.capitalize(),
            "native_language": native_language.capitalize(),
            "foreign_phrase": phrase[foreign_language],
            "native_phrase": phrase[native_language],
            "used": 0,
        }
        insert_stmt = table.insert().values(**values)
        session.execute(insert_stmt)
    session.commit()


def _create_db_session() -> Session:
    """
    Create and return a new SQLAlchemy session.

    Returns:
        Session: SQLAlchemy Session object.
    """
    engine = create_engine("sqlite:///" + str(DATABASE_LOCATION))
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def _get_table(session: Session, table_name: str) -> Table:
    """
    Get a table from the database.

    Args:
        session (Session): SQLAlchemy Session object.
        table_name (str): Name of the table in the database.

    Returns:
        Table: SQLAlchemy Table object.
    """
    metadata = MetaData()
    table = Table(table_name, metadata, autoload_with=session.bind)
    return table


def main():
    """
    Main function of the script. It performs the following steps:
    1. Parse command line arguments.
    2. Create a database session.
    3. Get the translations table.
    4. Load JSON data containing translations.
    5. Load translations into the database.
    """
    args = _parse_args()
    session = _create_db_session()
    translations_table = _get_table(session, "translations")
    phrases = _load_json_data(args.json)
    _load_translations(session, translations_table, phrases)


if __name__ == "__main__":
    main()
