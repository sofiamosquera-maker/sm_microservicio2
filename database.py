from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

db_host = os.getenv('host', 'postgres-service')
db_port = os.getenv('port', '5432')
db_name = os.getenv('database', 'datosdb')
db_user = os.getenv('user', 'admin')
db_password = os.getenv('password', 'secret123')

# Construir la URL de conexi—n
DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
print(f"Conectando a: postgresql://{db_user}:****@{db_host}:{db_port}/{db_name}")


# Crear engine de SQLAlchemy
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Crear SessionLocal para manejar sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

# Dependency para obtener DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
