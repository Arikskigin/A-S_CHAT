from flask import Flask


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    with app.app_context():
        # Imports
        from Web_Chat.application.routes import view
        from Web_Chat.application.filters import _slice
        from Web_Chat.application.local_database import DataBase

        # REGISTER ROUTES
        app.register_blueprint(view, url_prefix="/")

        # REGISTER CONTEXT PROCESSOR
        @app.context_processor
        def slice():
            return dict(slice=_slice)

        return app