from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker


url_object=URL.create(
    drivername="mysql+mysqlconnector",
    username="root",
    password="mysqlD123",  # No manual escaping needed here
    host="localhost",
    database="social_media_app"
)
engine = create_engine(url_object)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try: yield db
    finally: 
        print("closing db connection!")
        db.close()