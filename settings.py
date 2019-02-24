class Config:
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'novel website'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:admin@localhost/novel_website"
    SQLALCHEMY_POOL_SIZE = 20
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_TEARDOWN = True