class DebugConfig:
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductConfig(DebugConfig):
    DEBUG = False
