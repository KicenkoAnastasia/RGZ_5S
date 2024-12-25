from flask import Flask
from rdz import rdz_bp

app = Flask(__name__)

# Конфигурация приложения
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'

# Подключение blueprint
app.register_blueprint(rdz_bp)

if __name__ == '__main__':
    app.run(debug=True)
