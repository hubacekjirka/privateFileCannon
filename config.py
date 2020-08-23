import os

class Config:
    """Base config."""
    current_dir = os.path.dirname(os.path.realpath(__file__))
    SECRET_KEY = os.environ.get('SECRET_KEY')
    UPLOAD_PASSWORD = os.environ.get('UPLOAD_PASSWORD')
    FILE_STORAGE_PATH = os.path.join(current_dir, "app", "fileStorage")
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_FILESIZE_MB')) * 1024 * 1024

class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False

class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True