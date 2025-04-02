from app.utils.statsd_client import record_timer
import time
from app.utils.db import db

def insert_file_metadata(metadata_db):
    start_time = time.time()
    
    try:
        db.session.add(metadata_db)
        db.session.commit()
        return True
    
    except Exception as e:
        db.session.rollback()
        raise e
    
    finally:
        duration = time.time() - start_time
        record_timer("db.insert_file_metadata.duration", duration)  
