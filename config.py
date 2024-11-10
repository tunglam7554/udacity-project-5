import os

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', '123456')
DB_NAME = os.getenv('DB_NAME', 'capstone')
DB_PORT = os.getenv('DB_PORT', '5432')

SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'postgresql://{}:{}@{}:{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME))

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN', 'dev-cpow2e2hthall7yb.us.auth0.com')
API_AUDIENCE = os.getenv('API_AUDIENCE', 'capstone')
ALGORITHMS = os.getenv('ALGORITHMS', 'RS256')