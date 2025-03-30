from app import db
from datetime import datetime

class Servicio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(250), nullable=True)
    precio = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f'<Servicio {self.nombre}>'

class Presupuesto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100), nullable=False)
    vehiculo = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.now)
    observaciones = db.Column(db.Text, nullable=True)
    
    # Relación con items
    items = db.relationship('PresupuestoItem', backref='presupuesto', lazy=True)
    
    def __repr__(self):
        return f'<Presupuesto {self.id} - {self.cliente}>'

class PresupuestoItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    presupuesto_id = db.Column(db.Integer, db.ForeignKey('presupuesto.id'), nullable=False)
    servicio_id = db.Column(db.Integer, db.ForeignKey('servicio.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=1)
    precio_unitario = db.Column(db.Float, nullable=False)
    
    # Relación con servicio
    servicio = db.relationship('Servicio')
    
    def __repr__(self):
        return f'<PresupuestoItem {self.id}>'

class RecordatorioITV(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100), nullable=False)
    vehiculo = db.Column(db.String(100), nullable=False)
    matricula = db.Column(db.String(10), nullable=False)
    fecha_itv = db.Column(db.Date, nullable=False)
    observaciones = db.Column(db.Text, nullable=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    def __repr__(self):
        return f'<RecordatorioITV {self.vehiculo} - {self.matricula}>'
    
    def dias_restantes(self):
        """Calcula los días restantes hasta la próxima ITV"""
        hoy = datetime.now().date()
        if self.fecha_itv < hoy:
            return -1  # ITV vencida
        else:
            return (self.fecha_itv - hoy).days
