from organizer_project import create_app
from organizer_project.config import DEBUG, DEV, LOCALHOST, LOCALHOST_PORT


if __name__ == "__main__":
    app = create_app("dev" if DEV else "prod")
    app.app_context().push()
    params = {"debug": DEBUG}
    if LOCALHOST:
        params["host"] = LOCALHOST
    if LOCALHOST_PORT:
        params["port"] = LOCALHOST_PORT
    app.run(**params)
