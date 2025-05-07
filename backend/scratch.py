from docx import Document
import requests


resp = requests.post(
    'http://127.0.0.1:5000/api/import-directory',
    json={
        "path": "D:/projetcs/navtime/Navtime2/backend/files",
        "password": "admin123"
    }
)

print(resp.json())

