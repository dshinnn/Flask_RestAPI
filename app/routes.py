from app import app
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import RegisterForm, LoginForm, ProductForm
from app.models import User, Product, Category

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

# Register a new user
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    # checks if the method is a post and if it is, it checks if all inputs are valid
    if form.validate_on_submit():
        # Get data from the form
        username = form.username.data
        email = form.email.data
        password = form.password.data
        
        # Check if either the username or email is already in db
        user_exists = User.query.filter((User.username==username)|(User.email==email)).all()

        if user_exists:
            flash(f'Username with { username } already or email with { email } already exists', 'danger')
            return redirect(url_for('register'))

        # Create a new user instance using form data
        User(username=username, email=email, password=password)
        flash(f'Thank you for registering', 'primary')

        # Redirects to home page after registration
        return redirect(url_for('index'))
        
    return render_template('register.html', form=form)

# Logins user
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # Get data from the form
        username = form.username.data
        password = form.password.data

        # Query user table for user with username
        user = User.query.filter_by(username=username).first()

        # if the user does not exist or the user has an incorrect password
        if not user or not user.check_password(password):
            # redirect to login page
            flash('Username and/or password is incorrect', 'danger')
            return redirect(url_for('login'))
        # if user does exist and correct password, log user in
        login_user(user)
        flash('You have successfully logged in', 'success')
        return redirect(url_for('index'))

    return render_template('login.html', form=form)

# Logs out current user
@app.route('/logout')
def logout():
    logout_user()
    flash('You have successfully logged out', 'secondary')
    return redirect(url_for('index'))

# --- CRUD Operations ---
# INSERT
@app.route('/products/<int:prod_id>')
@login_required
def product_info(prod_id):
    # get_or_404 returns a http 404 error instead of a 500 (interal server error)
    product = Product.query.get_or_404(prod_id)
    return render_template('product.html', product=product)

# UPDATE
@app.route('/products/<int:prod_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(prod_id):
    # Checks if the user is an admin and redirects user to home page if not
    if not current_user.is_admin:
        flash("Excuse me you are not allowed here.", "warning")
        return redirect(url_for('index'))
    product = Product.query.get_or_404(prod_id)
    form = ProductForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]

    # Checks if the inputted information is valid
    if form.validate_on_submit():
        # Get data from the form
        name = form.name.data
        price = form.price.data
        image_url = form.image_url.data
        category_id = form.category_id.data

        # Update the product with the new info
        product.name = name
        product.price = price
        product.image_url = image_url
        product.category_id = category_id
        product.save()
        flash(f"{product.name} has been updated", "primary")
        
        # Redirects to product info page
        return redirect(url_for('product_info', prod_id=product.id))
    return render_template('edit_product.html', product=product, form=form)

# DELETE
@app.route('/products/<int:prod_id>/delete')
@login_required
def delete_product(prod_id):
    # Checks if the user is an admin and redirects user to home page if not
    if not current_user.is_admin:
        flash("Excuse me you are not allowed here.", "warning")
        return redirect(url_for('index'))
    
    # Grabs the product to delete
    product = Product.query.get_or_404(prod_id)
    
    # Deletes product
    product.delete()
    
    # Display message
    flash(f"{product.name} has been deleted", "danger")
    
    # Redirects to home page
    return redirect(url_for('index'))