from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, current_app
from app.models import Product
from app import db
import os
import uuid
from werkzeug.utils import secure_filename

main_bp = Blueprint('main', __name__)
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']
           
def save_image(file):
    if file and allowed_file(file.filename):
        # Generate a unique filename to prevent collisions
        filename = str(uuid.uuid4()) + secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        # Return the path relative to the static folder for use in templates
        return f'/static/uploads/{filename}'
    return None

@main_bp.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@main_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@main_bp.route('/product/<int:product_id>/gift', methods=['POST'])
def gift_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    if product.is_gifted:
        return jsonify({'success': False, 'message': 'Цей подарунок вже подаровано'})
    
    product.is_gifted = True
    db.session.commit()
    
    return jsonify({'success': True})

@admin_bp.route('/')
def admin_index():
    products = Product.query.all()
    return render_template('admin/index.html', products=products)

@admin_bp.route('/product/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        title = request.form.get('title')
        url = request.form.get('url')
        
        if not title:
            flash('Назва обов\'язкова', 'error')
            return redirect(url_for('admin.add_product'))
        
        # Handle image upload
        if 'image' not in request.files:
            flash('Зображення обов\'язкове', 'error')
            return redirect(url_for('admin.add_product'))
            
        image_file = request.files['image']
        
        if image_file.filename == '':
            flash('Зображення не вибрано', 'error')
            return redirect(url_for('admin.add_product'))
        
        image_path = save_image(image_file)
        
        if not image_path:
            flash('Непідтримуваний формат файлу. Дозволені формати: png, jpg, jpeg, gif', 'error')
            return redirect(url_for('admin.add_product'))
        
        product = Product(title=title, image=image_path, url=url)
        db.session.add(product)
        db.session.commit()
        
        flash('Елемент успішно додано', 'success')
        return redirect(url_for('admin.admin_index'))
    
    return render_template('admin/add_product.html')

@admin_bp.route('/product/<int:product_id>/edit', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        product.title = request.form.get('title')
        product.url = request.form.get('url')
        product.is_gifted = 'is_gifted' in request.form
        
        # Handle image upload if a new image is provided
        if 'image' in request.files and request.files['image'].filename != '':
            image_file = request.files['image']
            image_path = save_image(image_file)
            
            if image_path:
                # If there was a successful upload, update the image path
                product.image = image_path
            else:
                flash('Непідтримуваний формат файлу. Зображення не було оновлено.', 'warning')
        
        db.session.commit()
        flash('Елемент успішно оновлено', 'success')
        return redirect(url_for('admin.admin_index'))
    
    return render_template('admin/edit_product.html', product=product)

@admin_bp.route('/product/<int:product_id>/delete', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    db.session.delete(product)
    db.session.commit()
    
    flash('Елемент успішно видалено', 'success')
    return redirect(url_for('admin.admin_index'))