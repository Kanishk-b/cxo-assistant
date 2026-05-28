from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# This is the exact connection string matching your docker-compose file
# Format: postgresql://user:password@host:port/database_name
SQLALCHEMY_DATABASE_URL = "postgresql://cxo_admin:cxo_password@localhost:5432/cxo_assistant"

# The 'Engine' is the actual connection to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# The 'Session' is what we use to actually query and save data
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This is the foundation class that all our future database tables will inherit from
Base = declarative_base()

# A dependency function we will use in FastAPI to safely open and close DB connections
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()