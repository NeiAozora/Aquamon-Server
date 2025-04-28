import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError

# Base class for models
Base = declarative_base()

# The db variable for SQLAlchemy
db = None

def init_db(db_uri):
    """Initialize the database engine and session."""
    global db
    try:
        # Create the database engine
        engine = create_engine(db_uri, echo=True)

        # Create a scoped session for thread safety
        db = scoped_session(sessionmaker(bind=engine))

    except SQLAlchemyError as e:
        logging.error(f"Error initializing the database: {e}")
        raise

def get_session():
    """Get a scoped session for database transactions."""
    try:
        return db()
    except SQLAlchemyError as e:
        logging.error(f"Error obtaining session: {e}")
        raise

def commit(session):
    """Commit the current session."""
    try:
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()  # Ensure rollback in case of failure
        logging.error(f"Error committing session: {e}")
        raise

def close(session):
    """Close the session."""
    try:
        session.close()
    except SQLAlchemyError as e:
        logging.error(f"Error closing session: {e}")
        raise
