import os
import logging

from logging.handlers import RotatingFileHandler
from flask import Flask

from config import Config
from webapp.blueprints.main import main as main_blueprint
from webapp.blueprints.auth import auth as auth_blueprint
from webapp.extensions import db, migrate, login
from webapp import models

def create_app():
	app = Flask(__name__)
	app.config.from_object(Config)

	register_extensions(app)

	app.register_blueprint(main_blueprint)
	app.register_blueprint(auth_blueprint, url_prefix="/auth")

	register_make_shell_context(app)

	if app.config['LOG_TO_STDOUT']:
		stream_handler = logging.StreamHandler()
		stream_handler.setLevel(logging.INFO)
		app.logger.addHandler(stream_handler)
	else:
		if not os.path.exists('logs'):
			os.mkdir('logs')
		file_handler = RotatingFileHandler('logs/todo.log', maxBytes=10240, backupCount=10)
		file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s ''[in %(pathname)s:%(lineno)d]'))
		file_handler.setLevel(logging.INFO)
		app.logger.addHandler(file_handler)

	app.logger.setLevel(logging.INFO)
	app.logger.info('ToDo List')

	return app

def register_extensions(app):
	db.init_app(app)
	migrate.init_app(app, db=db)
	login.init_app(app)

def register_make_shell_context(app):
	@app.shell_context_processor
	def make_shell_context():
		return {'db': models.db, 'Users': models.Users, 'Tasks': models.Tasks, 'Projects':models.Projects}