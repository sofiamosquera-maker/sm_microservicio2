from sqlalchemy.orm import Session
from typing import List
import logging

from database import engine, get_db, Base
from models import DataEntity

# Crear las tablas
Base.metadata.create_all(bind=engine)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.get("/data/all")
def get_all_data(db: Session = Depends(get_db)):
    """
    Obtiene todos los registros de la tabla datos
    """
    try:
        logger.info("Obteniendo todos los datos de PostgreSQL")
        datos = db.query(DataEntity).all()
        result = [dato.to_dict() for dato in datos]
        logger.info(f"Se encontraron {len(result)} registros")
        return result
    except Exception as e:
        logger.error(f"Error al obtener datos: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/data/{data_id}")
def get_data_by_id(data_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un registro específico por ID
    """
    try:
        dato = db.query(DataEntity).filter(DataEntity.id == data_id).first()
        if dato is None:
            raise HTTPException(status_code=404, detail="Registro no encontrado")
        return dato.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al obtener dato {data_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/data/")
def create_data(nombre: str, descripcion: str, db: Session = Depends(get_db)):
    """
    Crea un nuevo registro
    """
    try:
        nuevo_dato = DataEntity(nombre=nombre, descripcion=descripcion)
        db.add(nuevo_dato)
        db.commit()
        db.refresh(nuevo_dato)
        logger.info(f"Registro creado con ID: {nuevo_dato.id}")
        return nuevo_dato.to_dict()
    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear dato: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.route('/health', methods=['GET'])
def call_health():
    return 'OK', 200

@app.route('/startup', methods=['GET'])
def call_startup():
    return 'OK', 200
    
@app.route('/readiness', methods=['GET'])
def call_readiness():
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)

