from flask import Flask
from routes.mongo import router as mongo_router
from routes.postgres import router as postgres_router

app = Flask(__name__)

app.register_blueprint(mongo_router)
app.register_blueprint(postgres_router)
