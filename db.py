from sqlmodel import create_engine, Session

DATABASE_URL = "sqlite:///./test.db"  # Cambia a PostgreSQL si lo necesitas

engine = create_engine(DATABASE_URL, echo=True)

# Dependency para FastAPI
def get_session():
    with Session(engine) as session:
        yield session