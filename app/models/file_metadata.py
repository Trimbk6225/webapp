from app.utils.db import db
from datetime import datetime

class FileMetadata(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.String(255), primary_key=True)  # UUID as the primary key
    file_name = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(512), nullable=False)  # Store the file URL
    upload_time = db.Column(db.Date, default=datetime.utcnow().date, nullable=False)
    extra_metadata = db.Column(db.JSON, nullable=True)  # Changed from 'metadata' to 'extra_metadata'