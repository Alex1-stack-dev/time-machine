from api.index import app
from mangum import Mangum

# Reuse the FastAPI app from api/index.py and expose a handler for Vercel
handler = Mangum(app)
