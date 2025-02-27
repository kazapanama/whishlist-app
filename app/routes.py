from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from app.models import Product
from app import db

main_bp = Blueprint('main', __name__)
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

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
        image = request.form.get('image')
        url = request.form.get('url')
        
        if not title or not image:
            flash('Назва та зображення обов\'язкові', 'error')
            return redirect(url_for('admin.add_product'))
        
        product = Product(title=title, image=image, url=url)
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
        product.image = request.form.get('image')
        product.url = request.form.get('url')
        product.is_gifted = 'is_gifted' in request.form
        
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