from flask import Blueprint, request, jsonify
from app.utils.s3 import upload_file_to_s3, delete_file_from_s3, get_file_url
from app.models.file_metadata import FileMetadata
from app.utils.db import db
from datetime import datetime
import uuid

files_blueprint = Blueprint("files", __name__)

@files_blueprint.route("/v1/file", methods=["POST"])
def upload_file():
    if "profilePic" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files["profilePic"]
    file_name = file.filename
    file_id = str(uuid.uuid4())  # Generate unique ID
    file_path = f"{file_id}/{file_name}"  # Store in bucket with unique identifier
    
    # Upload to S3
    if not upload_file_to_s3(file, file_path):
        return jsonify({"error": "Failed to upload file"}), 500
    
    file_url = get_file_url(file_path)
    
    # Save metadata to database
    metadata = FileMetadata(
        id=file_id,
        file_name=file_name,
        url=file_url,
        upload_time=datetime.utcnow().date()
    )
    db.session.add(metadata)
    db.session.commit()
    
    return jsonify({
        "file_name": file_name,
        "id": file_id,
        "url": file_url,
        "upload_date": metadata.upload_time.strftime("%Y-%m-%d")
    }), 201

@files_blueprint.route("/v1/file/<id>", methods=["GET"])
def get_file(id):
    metadata = FileMetadata.query.filter_by(id=id).first()
    if not metadata:
        return jsonify({"error": "File not found"}), 404

    return jsonify({
        "file_name": metadata.file_name,
        "id": metadata.id,
        "url": metadata.url,
        "upload_date": metadata.upload_time.strftime("%Y-%m-%d")
    }), 200

@files_blueprint.route("/v1/file/<id>", methods=["DELETE"])
def delete_file(id):
    metadata = FileMetadata.query.filter_by(id=id).first()
    if not metadata:
        return jsonify({"error": "File not found"}), 404

    # Delete from S3
    if not delete_file_from_s3(metadata.id + "/" + metadata.file_name):
        return jsonify({"error": "Failed to delete file"}), 500

    # Delete metadata from database
    db.session.delete(metadata)
    db.session.commit()

    return "", 204