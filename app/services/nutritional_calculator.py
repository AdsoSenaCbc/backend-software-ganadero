from app import db
from app.models import Animal, Racion, RequerimientosNutricionales, DetalleRacion, CaracteristicasNutricionales

class NutritionalCalculator:
    def calculate_nutritional_needs(self, animal_id):
        animal = Animal.query.get(animal_id)
        if not animal or not animal.id_etapa:
            return None
        
        requerimiento = RequerimientosNutricionales.query.filter_by(id_etapa=animal.id_etapa).first()
        if not requerimiento:
            return None
        
        needs = {
            "peso_min": float(requerimiento.peso_min),
            "peso_max": float(requerimiento.peso_max),
            "valor_min": float(requerimiento.valor_min),
            "valor_max": float(requerimiento.valor_max)
        }
        return needs

    def adjust_ration(self, racion_id, target_ms):
        racion = Racion.query.get(racion_id)
        if not racion:
            return False
        
        total_ms = 0
        detalles = DetalleRacion.query.filter_by(id_racion=racion_id).all()
        for detalle in detalles:
            total_ms += float(detalle.porcentaje_ms or 0)
        
        if total_ms == 0:
            return False
        
        adjustment_factor = target_ms / total_ms
        for detalle in detalles:
            detalle.cantidad_kg = float(detalle.cantidad_kg or 0) * adjustment_factor
            detalle.porcentaje_ms = float(detalle.porcentaje_ms or 0) * adjustment_factor
            db.session.commit()
        
        racion.ms_total = target_ms
        db.session.commit()
        return True