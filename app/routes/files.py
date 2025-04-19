from flask import Blueprint, request, jsonify, make_response
from app.services.file_metadata_service import insert_file_metadata
from app.utils.s3 import upload_file_to_s3, delete_file_from_s3, get_file_url
from app.models.file_metadata import FileMetadata
from app.utils.db import db
from datetime import datetime
import uuid
from app.utils.logger import log_request, webapp_logger
from app.utils.statsd_client import increment_counter, record_timer
import time

files_blueprint = Blueprint("files", __name__)

# Modify the `upload_file` route in Files.py to include metadata
@files_blueprint.route("/v1/file", methods=["POST"])
@log_request
def upload_file():
    start_time = time.time()
    increment_counter("api.upload_file.calls")  

    if "profilePic" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files["profilePic"]
    file_name = file.filename
    file_id = str(uuid.uuid4())  
    file_path = f"{file_id}/{file_name}"  
    
    # Create custom metadata (file type, file size, etc.)
    extra_metadata = {
        'fileType': file.content_type,  
        'fileSize': str(len(file.read()))  
    }

   
    file.seek(0)

    # Upload file to S3 with custom metadata
    if not upload_file_to_s3(file, file_path, extra_metadata):
        return jsonify({"error": "Failed to upload file"}), 500
    
    webapp_logger.info(f"File uploaded: {file_name}")
    

    file_url = get_file_url(file_path)

    # Save file metadata to the database
    metadata_db = FileMetadata(
        id=file_id,
        file_name=file_name,
        url=file_url,
        upload_time=datetime.utcnow().date(),
        extra_metadata=extra_metadata  
    )
    db.session.add(metadata_db)
    db.session.commit()
    
    duration = time.time() - start_time
    record_timer("api.upload_file.duration", duration) 
    try:
        insert_file_metadata(metadata_db)
    except Exception as e:
        return jsonify({"error": f"Failed to save metadata: {str(e)}"}), 500
    # Return the response with metadata excluded
    return jsonify({
        "file_name": file_name,
        "id": file_id,
        "url": file_url,
        "upload_date": metadata_db.upload_time.strftime("%Y-%m-%d")
    }), 201

@files_blueprint.route("/v1/file/<id>", methods=["GET"])
@log_request
def get_file(id):
    start_time = time.time()
    increment_counter("api.get_file.calls") 
    
    metadata = FileMetadata.query.filter_by(id=id).first()
    if not metadata:
        return jsonify({"error": "File not found"}), 404
    webapp_logger.info(f"File retrieved: {id}")

    duration = time.time() - start_time
    record_timer("api.get_file.duration", duration) 

    return jsonify({
        "file_name": metadata.file_name,
        "id": metadata.id,
        "url": metadata.url,
        "upload_date": metadata.upload_time.strftime("%Y-%m-%d")
    }), 200

@files_blueprint.route("/v1/file/<id>", methods=["DELETE"])
@log_request
def delete_file(id):
    start_time = time.time()
    increment_counter("api.delete_file.calls")
    metadata = FileMetadata.query.filter_by(id=id).first()
    if not metadata:
        return jsonify({"error": "File not found"}), 404

    # Delete from S3
    if not delete_file_from_s3(metadata.id + "/" + metadata.file_name):
        return jsonify({"error": "Failed to delete file"}), 500
    webapp_logger.info(f"File deleted: {id}")

    # Delete metadata from database
    db.session.delete(metadata)
    db.session.commit()

    duration = time.time() - start_time
    record_timer("api.delete_file.duration", duration) 

    return "", 204

@files_blueprint.route("/v1/file", methods=["OPTIONS", "HEAD","PUT", "PATCH","GET","DELETE"])
@log_request
def handle_options_head_for_file():
    response = make_response("", 405)
    response.headers["Allow"] = "POST"
    return response

 Upload file with metadata
@files_blueprint.route("/v2/file", methods=["POST"])
@log_request
def upload_file():
    start_time = time.time()
    increment_counter("api.upload_file.calls")  

    if "profilePic" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files["profilePic"]
    file_name = file.filename
    file_id = str(uuid.uuid4())  
    file_path = f"{file_id}/{file_name}"  

    extra_metadata = {
        'fileType': file.content_type,
        'fileSize': str(len(file.read()))
    }

    file.seek(0)

    if not upload_file_to_s3(file, file_path, extra_metadata):
        return jsonify({"error": "Failed to upload file"}), 500

    webapp_logger.info(f"File uploaded: {file_name}")

    file_url = get_file_url(file_path)

    metadata_db = FileMetadata(
        id=file_id,
        file_name=file_name,
        url=file_url,
        upload_time=datetime.utcnow().date(),
        extra_metadata=extra_metadata
    )
    db.session.add(metadata_db)
    db.session.commit()

    duration = time.time() - start_time
    record_timer("api.upload_file.duration", duration) 

    try:
        insert_file_metadata(metadata_db)
    except Exception as e:
        return jsonify({"error": f"Failed to save metadata: {str(e)}"}), 500

    return jsonify({
        "file_name": file_name,
        "id": file_id,
        "url": file_url,
        "upload_date": metadata_db.upload_time.strftime("%Y-%m-%d")
    }), 201

# Retrieve file
@files_blueprint.route("/v2/file/<id>", methods=["GET"])
@log_request
def get_file(id):
    start_time = time.time()
    increment_counter("api.get_file.calls") 
    
    metadata = FileMetadata.query.filter_by(id=id).first()
    if not metadata:
        return jsonify({"error": "File not found"}), 404

    webapp_logger.info(f"File retrieved: {id}")
    duration = time.time() - start_time
    record_timer("api.get_file.duration", duration) 

    return jsonify({
        "file_name": metadata.file_name,
        "id": metadata.id,
        "url": metadata.url,
        "upload_date": metadata.upload_time.strftime("%Y-%m-%d")
    }), 200

# Delete file
@files_blueprint.route("/v2/file/<id>", methods=["DELETE"])
@log_request
def delete_file(id):
    start_time = time.time()
    increment_counter("api.delete_file.calls")

    metadata = FileMetadata.query.filter_by(id=id).first()
    if not metadata:
        return jsonify({"error": "File not found"}), 404

    if not delete_file_from_s3(metadata.id + "/" + metadata.file_name):
        return jsonify({"error": "Failed to delete file"}), 500

    webapp_logger.info(f"File deleted: {id}")

    db.session.delete(metadata)
    db.session.commit()

    duration = time.time() - start_time
    record_timer("api.delete_file.duration", duration) 

    return "", 204

# Handle unsupported HTTP methods
@files_blueprint.route("/v2/file", methods=["OPTIONS", "HEAD", "PUT", "PATCH", "GET", "DELETE"])
@log_request
def handle_options_head_for_file():
    response = make_response("", 405)
    response.headers["Allow"] = "POST"
    return response
