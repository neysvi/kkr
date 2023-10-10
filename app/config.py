from datetime import timedelta

SQLALCHEMY_DATABASE_URI = 'postgresql://neys:1230@localhost:5432/med_data'
UPLOAD_FOLDER = 'files/'
ALLOWED_EXTENSIONS = {'rar', 'zip'}
SESSION_TYPE = "filesystem"
SECRET_KEY = "3a43257fc6b86f4d4a550a5abe79cc46f026b93cd3b3675d"
PERMANENT_SESSION_LIFETIME = timedelta(minutes=10)
SESSION_PERMANENT = False
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "None"
SESSION_COOKIE_SECURE = True
