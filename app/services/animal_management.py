from app import db
from app.models import Animal, EventoAnimal, HistorialAnimal

class AnimalManagement:
    def record_event(self, animal_id, event_type_id, value, observations=None):
        event = EventoAnimal(
            id_animal=animal_id,
            id_tipo_evento=event_type_id,
            valor=value,
            observaciones=observations
        )
        db.session.add(event)
        db.session.commit()
        return event

    def update_history(self, animal_id, hacienda_id, exit_date=None, observations=None):
        historial = HistorialAnimal.query.filter_by(id_animal=animal_id, fecha_salida=None).first()
        if historial:
            historial.fecha_salida = exit_date
            historial.observaciones = observations
        else:
            new_history = HistorialAnimal(
                id_animal=animal_id,
                id_hacienda=hacienda_id,
                fecha_salida=exit_date,
                observaciones=observations
            )
            db.session.add(new_history)
        db.session.commit()
        return True