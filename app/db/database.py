from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.settings.config import DB_URL

engine = create_engine(DB_URL, echo=False)
Session = sessionmaker(bind=engine)