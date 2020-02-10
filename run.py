import os

from app import app as application

if __name__ == '__main__':
    port = int(os.getenv('PORT', default=5000))
    host = '0.0.0.0'
    application.run(host=host, port=port)