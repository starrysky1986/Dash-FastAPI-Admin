from waitress import serve
from app import app
from config.env import AppConfig

serve(
    app.server,
    host=AppConfig.app_host,
    port=AppConfig.app_port
)
