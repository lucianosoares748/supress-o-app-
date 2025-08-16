from app import app  # importa o Flask app do app.py
from mangum import Mangum

handler = Mangum(app)

