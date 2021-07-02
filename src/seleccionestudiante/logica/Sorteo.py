from src.seleccionestudiante.modelo.Asignatura import Asignatura
from src.seleccionestudiante.modelo.Actividad import Actividad
from src.seleccionestudiante.modelo.Equipo import Equipo
from src.seleccionestudiante.modelo.Estudiante import Estudiante

from src.seleccionestudiante.modelo.declarative_base import engine, Base, session

class Sorteo():

    def __init__(self):
        Base.metadata.create_all(engine)

    def agregar_asignatura(self, nombreAsignatura):
        busqueda = session.query(Asignatura).filter(Asignatura.nombreAsignatura == nombreAsignatura).all()
        if len(busqueda) == 0:
            asignatura = Asignatura(nombreAsignatura = nombreAsignatura)
            session.add(asignatura)
            session.commit()
            return True
        else:
            return False

    def agregar_actividad(self, denominacionActividad, fecha):
        busqueda = session.query(Actividad).filter(Actividad.denominacionActividad == denominacionActividad, fecha==fecha).all()
        if len(busqueda) == 0:
            actividad = Actividad(denominacionActividad = denominacionActividad, fecha = fecha)
            session.add(actividad)
            session.commit()
            return True
        else:
            return False

    def agregar_equipo(self, denominacionEquipo):
        busqueda = session.query(Equipo).filter(Equipo.denominacionEquipo == denominacionEquipo).all()
        if len(busqueda) == 0:
            equipo = Equipo(denominacionEquipo = denominacionEquipo)
            session.add(equipo)
            session.commit()
            return True
        else:
            return False

    def agregar_estudiante(self, apellidoPaterno, apellidoMaterno, nombres, elegible):
        busqueda = session.query(Estudiante).filter(Estudiante.apellidoPaterno == apellidoPaterno, Estudiante.apellidoMaterno == apellidoMaterno, nombres == nombres, elegible == elegible ).all()
        if len(busqueda) == 0:
            estudiante = Estudiante(apellidoPaterno = apellidoPaterno, apellidoMaterno = apellidoMaterno, nombres = nombres, elegible = elegible)
            session.add(estudiante)
            session.commit()
            return True
        else:
            return False