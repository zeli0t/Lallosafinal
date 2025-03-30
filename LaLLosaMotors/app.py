import os
import json
import logging
import sys
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Configuración de logging
logging.basicConfig(level=logging.DEBUG)

# Clase base para SQLAlchemy
class Base(DeclarativeBase):
    pass

# Inicialización de SQLAlchemy
db = SQLAlchemy(model_class=Base)

# Creación de la aplicación Flask
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "lallosa_motors_secreto")

# Determinar si estamos ejecutando en modo congelado (PyInstaller)
def is_frozen():
    return getattr(sys, 'frozen', False) or os.environ.get("PYINSTALLER_FROZEN") == "1"

# Obtener el directorio base de la aplicación
def get_base_dir():
    if is_frozen():
        # Estamos ejecutando desde un .exe compilado
        return os.path.dirname(sys.executable)
    else:
        # Estamos ejecutando desde el código fuente
        return os.path.dirname(os.path.abspath(__file__))

# Función para determinar la ruta de la base de datos según el entorno
def get_db_url():
    # Si ya tenemos una URL de base de datos configurada, usarla
    if os.environ.get("DATABASE_URL"):
        return os.environ.get("DATABASE_URL")
    
    # En cualquier otro caso, configurar SQLite en el directorio de datos
    base_dir = get_base_dir()
    data_dir = os.path.join(base_dir, 'data')
    
    # Asegurar que el directorio de datos exista
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # Ruta a la base de datos SQLite
    db_path = os.path.join(data_dir, 'lallosa.db')
    return f'sqlite:///{db_path}'

# Configurar la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = get_db_url()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializar la aplicación con SQLAlchemy
db.init_app(app)

# Función para cargar datos iniciales
def cargar_datos_iniciales():
    with app.app_context():
        from models import Servicio, Presupuesto, PresupuestoItem, RecordatorioITV
        db.create_all()
        
        # Determinar la ruta de los archivos de datos
        base_dir = get_base_dir()
            
        # Rutas de archivos de datos
        services_path = os.path.join(base_dir, 'static', 'data', 'services.json')
        budgets_path = os.path.join(base_dir, 'static', 'data', 'budgets.json')
        
        # Cargar datos de servicios.json si existe
        try:
            if os.path.exists(services_path):
                with open(services_path, 'r', encoding='utf-8') as f:
                    servicios = json.load(f)
                    for servicio in servicios:
                        if not Servicio.query.filter_by(nombre=servicio['nombre']).first():
                            db.session.add(Servicio(
                                nombre=servicio['nombre'],
                                descripcion=servicio['descripcion'],
                                precio=servicio['precio']
                            ))
                    db.session.commit()
        except Exception as e:
            app.logger.error(f"Error al cargar servicios: {e}")
    
        # Cargar datos de presupuestos.json si existe
        try:
            if os.path.exists(budgets_path):
                with open(budgets_path, 'r', encoding='utf-8') as f:
                    presupuestos = json.load(f)
                    for presupuesto_data in presupuestos:
                        fecha = datetime.strptime(presupuesto_data['fecha'], '%Y-%m-%d')
                        presupuesto = Presupuesto(
                            cliente=presupuesto_data['cliente'],
                            vehiculo=presupuesto_data['vehiculo'],
                            fecha=fecha,
                            observaciones=presupuesto_data.get('observaciones', '')
                        )
                        db.session.add(presupuesto)
                        db.session.flush()  # Para obtener el ID del presupuesto
                        
                        for item in presupuesto_data['items']:
                            servicio = Servicio.query.filter_by(nombre=item['servicio']).first()
                            if servicio:
                                db.session.add(PresupuestoItem(
                                    presupuesto_id=presupuesto.id,
                                    servicio_id=servicio.id,
                                    cantidad=item['cantidad'],
                                    precio_unitario=item['precio_unitario']
                                ))
                    db.session.commit()
        except Exception as e:
            app.logger.error(f"Error al cargar presupuestos: {e}")

# Importar modelos después de inicializar db
with app.app_context():
    from models import Servicio, Presupuesto, PresupuestoItem, RecordatorioITV
    db.create_all()

# Cargar datos iniciales
cargar_datos_iniciales()

# Función para guardar servicios en JSON
def get_data_dir():
    """Obtiene el directorio para los datos de la aplicación"""
    # Directorio base de la aplicación
    base_dir = get_base_dir()
    
    # Directorio de datos
    data_dir = os.path.join(base_dir, 'data')
    
    # Asegurar que existe el directorio
    os.makedirs(data_dir, exist_ok=True)
    
    # También crear el directorio para los JSON si no existe
    json_dir = os.path.join(base_dir, 'static', 'data')
    os.makedirs(json_dir, exist_ok=True)
    
    return json_dir

def guardar_servicios():
    servicios = Servicio.query.all()
    datos = []
    for servicio in servicios:
        datos.append({
            'id': servicio.id,
            'nombre': servicio.nombre,
            'descripcion': servicio.descripcion,
            'precio': servicio.precio
        })
    
    data_dir = get_data_dir()
    services_file = os.path.join(data_dir, 'services.json')
    with open(services_file, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)

# Función para guardar presupuestos en JSON
def guardar_presupuestos():
    presupuestos = Presupuesto.query.all()
    datos = []
    for presupuesto in presupuestos:
        items_data = []
        for item in presupuesto.items:
            servicio = Servicio.query.get(item.servicio_id)
            items_data.append({
                'servicio': servicio.nombre,
                'cantidad': item.cantidad,
                'precio_unitario': item.precio_unitario
            })
        
        datos.append({
            'id': presupuesto.id,
            'cliente': presupuesto.cliente,
            'vehiculo': presupuesto.vehiculo,
            'fecha': presupuesto.fecha.strftime('%Y-%m-%d'),
            'observaciones': presupuesto.observaciones,
            'items': items_data
        })
    
    data_dir = get_data_dir()
    budgets_file = os.path.join(data_dir, 'budgets.json')
    with open(budgets_file, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)

# Rutas de la aplicación

@app.route('/')
def index():
    # Obtener los recordatorios ITV
    recordatorios = RecordatorioITV.query.order_by(RecordatorioITV.fecha_itv).all()
    return render_template('index.html', recordatorios=recordatorios)

# Rutas para servicios
@app.route('/servicios')
def servicios():
    servicios = Servicio.query.all()
    return render_template('services.html', servicios=servicios)

@app.route('/servicios/nuevo', methods=['POST'])
def nuevo_servicio():
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    precio = request.form.get('precio')
    
    if not nombre or not precio:
        flash('Nombre y precio son obligatorios', 'danger')
        return redirect(url_for('servicios'))
    
    try:
        precio = float(precio)
        servicio = Servicio(nombre=nombre, descripcion=descripcion, precio=precio)
        db.session.add(servicio)
        db.session.commit()
        guardar_servicios()
        flash('Servicio añadido correctamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al añadir servicio: {str(e)}', 'danger')
    
    return redirect(url_for('servicios'))

@app.route('/servicios/editar/<int:id>', methods=['POST'])
def editar_servicio(id):
    servicio = Servicio.query.get_or_404(id)
    servicio.nombre = request.form.get('nombre')
    servicio.descripcion = request.form.get('descripcion')
    
    try:
        servicio.precio = float(request.form.get('precio'))
        db.session.commit()
        guardar_servicios()
        flash('Servicio actualizado correctamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al actualizar servicio: {str(e)}', 'danger')
    
    return redirect(url_for('servicios'))

@app.route('/servicios/eliminar/<int:id>')
def eliminar_servicio(id):
    servicio = Servicio.query.get_or_404(id)
    
    try:
        db.session.delete(servicio)
        db.session.commit()
        guardar_servicios()
        flash('Servicio eliminado correctamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar servicio: {str(e)}', 'danger')
    
    return redirect(url_for('servicios'))

# Rutas para presupuestos
@app.route('/presupuestos')
def presupuestos():
    return render_template('budget.html')

@app.route('/api/servicios')
def api_servicios():
    servicios = Servicio.query.all()
    return jsonify([{
        'id': s.id,
        'nombre': s.nombre,
        'descripcion': s.descripcion,
        'precio': s.precio
    } for s in servicios])

@app.route('/presupuestos/nuevo', methods=['POST'])
def nuevo_presupuesto():
    data = request.json
    
    try:
        presupuesto = Presupuesto(
            cliente=data['cliente'],
            vehiculo=data['vehiculo'],
            fecha=datetime.now(),
            observaciones=data.get('observaciones', '')
        )
        db.session.add(presupuesto)
        db.session.flush()  # Para obtener el ID del presupuesto
        
        for item in data['items']:
            presupuesto_item = PresupuestoItem(
                presupuesto_id=presupuesto.id,
                servicio_id=item['servicio_id'],
                cantidad=item['cantidad'],
                precio_unitario=item['precio_unitario']
            )
            db.session.add(presupuesto_item)
        
        db.session.commit()
        guardar_presupuestos()
        
        return jsonify({'success': True, 'id': presupuesto.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@app.route('/presupuestos/editar/<int:id>', methods=['GET'])
def obtener_presupuesto(id):
    try:
        presupuesto = Presupuesto.query.get_or_404(id)
        items = PresupuestoItem.query.filter_by(presupuesto_id=id).all()
        
        items_data = []
        for item in items:
            servicio = Servicio.query.get(item.servicio_id)
            items_data.append({
                'servicio_id': item.servicio_id,
                'nombre_servicio': servicio.nombre,
                'cantidad': item.cantidad,
                'precio_unitario': item.precio_unitario
            })
        
        resultado = {
            'id': presupuesto.id,
            'cliente': presupuesto.cliente,
            'vehiculo': presupuesto.vehiculo,
            'fecha': presupuesto.fecha.strftime('%Y-%m-%d'),
            'observaciones': presupuesto.observaciones,
            'items': items_data
        }
        
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/presupuestos/editar/<int:id>', methods=['POST'])
def actualizar_presupuesto(id):
    data = request.json
    
    try:
        presupuesto = Presupuesto.query.get_or_404(id)
        presupuesto.cliente = data['cliente']
        presupuesto.vehiculo = data['vehiculo']
        presupuesto.observaciones = data.get('observaciones', '')
        
        # Eliminar todos los items existentes
        PresupuestoItem.query.filter_by(presupuesto_id=id).delete()
        
        # Añadir los nuevos items
        for item in data['items']:
            presupuesto_item = PresupuestoItem(
                presupuesto_id=presupuesto.id,
                servicio_id=item['servicio_id'],
                cantidad=item['cantidad'],
                precio_unitario=item['precio_unitario']
            )
            db.session.add(presupuesto_item)
        
        db.session.commit()
        guardar_presupuestos()
        
        return jsonify({'success': True, 'id': presupuesto.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/presupuestos/imprimir/<int:id>')
def imprimir_presupuesto(id):
    presupuesto = Presupuesto.query.get_or_404(id)
    items = PresupuestoItem.query.filter_by(presupuesto_id=id).all()
    
    detalles_items = []
    total_sin_iva = 0
    
    for item in items:
        servicio = Servicio.query.get(item.servicio_id)
        subtotal = item.cantidad * item.precio_unitario
        total_sin_iva += subtotal
        
        detalles_items.append({
            'servicio': servicio.nombre,
            'descripcion': servicio.descripcion,
            'cantidad': item.cantidad,
            'precio_unitario': item.precio_unitario,
            'subtotal': subtotal
        })
    
    iva = total_sin_iva * 0.21  # 21% de IVA
    total_con_iva = total_sin_iva + iva
    
    return render_template(
        'budget_print.html',
        presupuesto=presupuesto,
        items=detalles_items,
        total_sin_iva=total_sin_iva,
        iva=iva,
        total_con_iva=total_con_iva
    )

@app.route('/api/presupuestos')
def api_presupuestos():
    presupuestos = Presupuesto.query.all()
    resultado = []
    
    for p in presupuestos:
        items = PresupuestoItem.query.filter_by(presupuesto_id=p.id).all()
        items_data = []
        total = 0
        
        for item in items:
            servicio = Servicio.query.get(item.servicio_id)
            subtotal = item.cantidad * item.precio_unitario
            total += subtotal
            
            items_data.append({
                'servicio': servicio.nombre,
                'cantidad': item.cantidad,
                'precio_unitario': item.precio_unitario,
                'subtotal': subtotal
            })
        
        resultado.append({
            'id': p.id,
            'cliente': p.cliente,
            'vehiculo': p.vehiculo,
            'fecha': p.fecha.strftime('%d/%m/%Y'),
            'observaciones': p.observaciones,
            'items': items_data,
            'total_sin_iva': total,
            'iva': total * 0.21,
            'total_con_iva': total * 1.21
        })
    
    return jsonify(resultado)

@app.route('/presupuestos/eliminar/<int:id>', methods=['POST', 'DELETE'])
def eliminar_presupuesto(id):
    try:
        # Primero eliminamos los items relacionados
        PresupuestoItem.query.filter_by(presupuesto_id=id).delete()
        
        # Luego eliminamos el presupuesto
        presupuesto = Presupuesto.query.get_or_404(id)
        db.session.delete(presupuesto)
        db.session.commit()
        guardar_presupuestos()
        
        if request.is_json:
            return jsonify({'success': True})
        else:
            flash('Presupuesto eliminado correctamente', 'success')
            return redirect(url_for('presupuestos'))
    
    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({'success': False, 'error': str(e)}), 500
        else:
            flash(f'Error al eliminar presupuesto: {str(e)}', 'danger')
            return redirect(url_for('presupuestos'))

# Rutas para búsqueda
@app.route('/buscar')
def buscar():
    termino = request.args.get('q', '')
    if not termino:
        return jsonify([])
    
    # Buscar en servicios
    servicios = Servicio.query.filter(
        Servicio.nombre.ilike(f'%{termino}%') | 
        Servicio.descripcion.ilike(f'%{termino}%')
    ).all()
    
    # Buscar en presupuestos
    presupuestos = Presupuesto.query.filter(
        Presupuesto.cliente.ilike(f'%{termino}%') | 
        Presupuesto.vehiculo.ilike(f'%{termino}%') |
        Presupuesto.observaciones.ilike(f'%{termino}%')
    ).all()
    
    # Formatear resultados
    resultados = {
        'servicios': [{
            'id': s.id,
            'nombre': s.nombre,
            'descripcion': s.descripcion,
            'precio': s.precio,
            'url': url_for('servicios')
        } for s in servicios],
        'presupuestos': [{
            'id': p.id,
            'cliente': p.cliente,
            'vehiculo': p.vehiculo,
            'fecha': p.fecha.strftime('%d/%m/%Y'),
            'url': url_for('imprimir_presupuesto', id=p.id)
        } for p in presupuestos]
    }
    
    return jsonify(resultados)

# Rutas para recordatorios ITV
@app.route('/recordatorios/itv', methods=['GET'])
def listar_recordatorios_itv():
    recordatorios = RecordatorioITV.query.order_by(RecordatorioITV.fecha_itv).all()
    return jsonify([{
        'id': r.id,
        'cliente': r.cliente,
        'vehiculo': r.vehiculo,
        'matricula': r.matricula,
        'fecha_itv': r.fecha_itv.strftime('%Y-%m-%d'),
        'observaciones': r.observaciones,
        'dias_restantes': r.dias_restantes()
    } for r in recordatorios])

@app.route('/recordatorios/itv/nuevo', methods=['POST'])
def nuevo_recordatorio_itv():
    try:
        # Si los datos vienen como JSON
        if request.is_json:
            data = request.json
            cliente = data.get('cliente')
            vehiculo = data.get('vehiculo')
            matricula = data.get('matricula')
            fecha_itv = datetime.strptime(data.get('fecha_itv'), '%Y-%m-%d').date()
            observaciones = data.get('observaciones', '')
        else:
            # Si los datos vienen como form-data
            cliente = request.form.get('cliente')
            vehiculo = request.form.get('vehiculo')
            matricula = request.form.get('matricula')
            fecha_itv = datetime.strptime(request.form.get('fecha_itv'), '%Y-%m-%d').date()
            observaciones = request.form.get('observaciones', '')
        
        if not cliente or not vehiculo or not matricula or not fecha_itv:
            if request.is_json:
                return jsonify({'success': False, 'error': 'Faltan datos obligatorios'}), 400
            else:
                flash('Todos los campos son obligatorios', 'danger')
                return redirect(url_for('index'))
        
        recordatorio = RecordatorioITV(
            cliente=cliente,
            vehiculo=vehiculo,
            matricula=matricula,
            fecha_itv=fecha_itv,
            observaciones=observaciones
        )
        
        db.session.add(recordatorio)
        db.session.commit()
        
        if request.is_json:
            return jsonify({'success': True, 'id': recordatorio.id})
        else:
            flash('Recordatorio de ITV añadido correctamente', 'success')
            return redirect(url_for('index'))
    
    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({'success': False, 'error': str(e)}), 500
        else:
            flash(f'Error al añadir recordatorio de ITV: {str(e)}', 'danger')
            return redirect(url_for('index'))

@app.route('/recordatorios/itv/eliminar/<int:id>', methods=['POST', 'DELETE'])
def eliminar_recordatorio_itv(id):
    try:
        recordatorio = RecordatorioITV.query.get_or_404(id)
        db.session.delete(recordatorio)
        db.session.commit()
        
        if request.is_json:
            return jsonify({'success': True})
        else:
            flash('Recordatorio de ITV eliminado correctamente', 'success')
            return redirect(url_for('index'))
    
    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({'success': False, 'error': str(e)}), 500
        else:
            flash(f'Error al eliminar recordatorio de ITV: {str(e)}', 'danger')
            return redirect(url_for('index'))
