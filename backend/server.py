# backend/server.py
import os
import subprocess
import csv
import getpass
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from sqlalchemy import or_, func

# For Compiling
# from backend.database import SessionLocal, init_db, Document
# from backend.utils import create_document, TEMPLATE_DIR, OUTPUT_DIR


## Before Compiling
from database import SessionLocal, init_db, Document
from utils import create_document, TEMPLATE_DIR, OUTPUT_DIR



app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), '../frontend/build'), static_url_path='/')
CORS(app)  # Enable CORS for development

# Initialize the database tables.
init_db()

@app.route('/api/templates', methods=['GET'])
def list_templates():
    try:
        templates = [f for f in os.listdir(TEMPLATE_DIR) if f.endswith('.docx')]
        return jsonify({"templates": templates})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/create-document', methods=['POST'])
def create_doc():
    data = request.get_json()
    template_name = data.get('template')
    keywords = data.get('keywords', '')

    if not template_name:
        return jsonify({"error": "Template name is required"}), 400

    try:
        # Retrieve the current logged-in user.
        username = getpass.getuser()

        # Read the abbreviation from user_abbreviations.csv.
        # The CSV should have rows in the format: username,abbreviation
        abbrev = None
        csv_path = os.path.join(os.path.dirname(__file__), 'user_abbreviations.csv')
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                # Compare usernames case-insensitively.
                if row and row[0].strip().lower() == username.lower():
                    abbrev = row[5].strip()
                    break
        if not abbrev:
            abbrev = "XX"  # Use a default abbreviation if none found.

        # Generate today's date in ddmmyy format.
        today_str = datetime.now().strftime("%d%m%y")

        # Count documents for this user created today.
        db = SessionLocal()
        # We assume that Document.created_at stores a string or datetime;
        # in our utils we saved current_date_display as yyyy-mm-dd.
        # To count, we can filter based on the date prefix if stored as a string.
        # Alternatively, if created_at is a datetime, we can use date comparisons.
        # Here, we assume created_at is a string in "yyyy-mm-dd" format,
        # and we compare the day, month and year (adjust accordingly if needed).
        today_date = datetime.now().date()
        count = db.query(Document).filter(
            Document.user == username,
            func.date(Document.created_at) == today_date
        ).count()
        doc_count = count + 1
        # Build the file name as: NV-{abbrev}-{ddmmyy}-{doc_count}
        new_filename = f"NV-{abbrev}-{today_str}-{doc_count}"
        # Create the document by calling the updated function.

        print(f'template name: {template_name}, keywords: {keywords}, new filename: {new_filename}')
        
        doc_metadata = create_document(template_name, keywords, new_filename)

        # Save the document metadata in the database.
        new_doc = Document(
            file_name=doc_metadata['file_name'],
            file_path=doc_metadata['file_path'],
            created_at=datetime.now(),  # Storing current datetime.
            user=username,
            keywords=doc_metadata['keywords']
        )
        db.add(new_doc)
        db.commit()
        db.refresh(new_doc)
        db.close()

        return jsonify({"message": "Document created", "document": {
            "id": new_doc.id,
            "file_name": new_doc.file_name,
            "file_path": new_doc.file_path,
            "created_at": new_doc.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "user": new_doc.user,
            "keywords": new_doc.keywords
        }})
    except Exception as e:
        print("error here")
        return jsonify({"error": str(e)}), 500

@app.route('/api/documents', methods=['GET'])
def get_documents():
    sort_by = request.args.get('sort_by', 'created_at')
    search = request.args.get('search', '')
    user_filter = request.args.get('user', '').strip()

    db = SessionLocal()
    query = db.query(Document)
    
    if search:
        query = query.filter(
            or_(
                Document.file_name.like(f"%{search}%"),
                Document.keywords.like(f"%{search}%"),
                Document.user.like(f"%{search}%")
            )
        )
    
    if user_filter:
        query = query.filter(Document.user == user_filter)
    
    if sort_by in ['created_at', 'user', 'file_name']:
        query = query.order_by(getattr(Document, sort_by).desc())
    
    documents = query.all()
    db.close()

    docs = []
    for doc in documents:
        # Format created_at if it's a datetime; adjust if stored differently.
        docs.append({
            "id": doc.id,
            "file_name": doc.file_name,
            "file_path": doc.file_path,
            "created_at": doc.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "user": doc.user,
            "keywords": doc.keywords
        })

    return jsonify({"documents": docs})

@app.route('/api/open-file/<path:filename>', methods=['GET'])
def open_file(filename):
    try:
        return send_from_directory(OUTPUT_DIR, filename, as_attachment=False)
    except Exception as e:
        return jsonify({"error": str(e)}), 404
    

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

# open the links using python method instead of a js one
@app.route('/api/launch-file/<path:filename>', methods=['GET', 'POST'])
def launch_file(filename):
    """
    Tell the OS to open the given file (in OUTPUT_DIR) with its default application.
    """
    file_path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    try:
        if os.name == 'nt':  # Windows
            os.startfile(file_path)
        elif sys.platform == 'darwin':  # macOS
            subprocess.Popen(['open', file_path])
        else:  # Linux variants
            subprocess.Popen(['xdg-open', file_path])
        return jsonify({"message": "File launched"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
