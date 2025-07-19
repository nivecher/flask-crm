from app import create_app
from app.extensions import db
from typing import Dict, Any

app = create_app()


@app.shell_context_processor
def make_shell_context() -> Dict[str, Any]:
    from app.models import User, Donor, Donation

    return {"db": db, "User": User, "Donor": Donor, "Donation": Donation}
