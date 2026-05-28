from app.db.database import engine, Base
# We must import the models here so SQLAlchemy knows they exist before creating tables
from app.db.models import SavedBriefing

def initialize_database():
    print("🛠️  Connecting to PostgreSQL vault...")
    # This command inspects our Python models and builds the matching SQL tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")

if __name__ == "__main__":
    initialize_database()