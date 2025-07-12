from app import create_app
from app.extensions import db

app = create_app()


@app.shell_context_processor
def make_shell_context():
    from app.models import User, Donor, Donation

    return {"db": db, "User": User, "Donor": Donor, "Donation": Donation}
