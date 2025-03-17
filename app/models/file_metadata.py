from app.utils.db import db

class FileMetadata(db.Model):
    __tablename__ = 'file_metadata'
    id = db.Column(db.String(255), primary_key=True)  # UUID as the primary key
    file_name = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(512), nullable=False)  # Store the file URL
    upload_time = db.Column(db.DateTime, nullable=False)