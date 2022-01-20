from app import app, db
from app.models import User, Product, Category

# Loads new instance of a flask shell with the following imports
@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Product': Product,
        'Category': Category
    }