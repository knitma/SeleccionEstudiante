from src.seleccionestudiante.modelo.Asignatura import Asignatura
from src.seleccionestudiante.modelo.Actividad import Actividad
from src.seleccionestudiante.modelo.Equipo import Equipo
from src.seleccionestudiante.modelo.Estudiante import Estudiante
from datetime import date
from datetime import datetime

from src.seleccionestudiante.modelo.declarative_base import engine, Base, session

class Sorteo():

    def __init__(self):
        Base.metadata.create_all(engine)
    """INICIO DE ASIGNATURA"""
    def agregar_asignatura(self, nombreAsignatura):
        if (nombreAsignatura == ""):
            return False
        busqueda = session.query(Asignatura).filter(Asignatura.nombreAsignatura == nombreAsignatura).all()
        if len(busqueda) == 0:
            asignatura = Asignatura(nombreAsignatura = nombreAsignatura)
            session.add(asignatura)
            session.commit()
            return True
        else:
            return False

    def editar_asignatura(self, idAsignatura, nombreAsignatura):
        busqueda = session.query(Asignatura).filter(Asignatura.nombreAsignatura == nombreAsignatura,
                                                    Asignatura.idAsignatura != idAsignatura).all()
        if len(busqueda) == 0:
            asignatura = session.query(Asignatura).filter(Asignatura.idAsignatura == idAsignatura).first()
            asignatura.nombreAsignatura = nombreAsignatura
            session.commit()
            return True
        else:
            return False

    def eliminar_asignatura(self, idAsignatura):
        try:
            asignatura = session.query(Asignatura).filter(Asignatura.idAsignatura == idAsignatura).first()
            session.delete(asignatura)
            session.commit()
            return True
        except:
            return False

    def dar_asignatura(self):
        asignaturas = [elem.__dict__ for elem in
                       session.query(Asignatura).all()]
        return asignaturas

    def dar_asignatura_por_idAsignatura(self, idAsignatura):
        return session.query(Asignatura).get(idAsignatura).__dict__

    def buscar_asignatura_por_nombreAsignatura(self, nombreAsignatura):
        asignaturas = [elem.__dict__ for elem in
                       session.query(Asignatura).filter(
                           Asignatura.nombreAsignatura.ilike('%{0}%'.format(nombreAsignatura))).all()]
        return asignaturas

    """ TERMINO DE ASIGNATURA"""

    def agregar_actividad(self, denominacionActividad, fecha):
        busqueda = session.query(Actividad).filter(Actividad.denominacionActividad==denominacionActividad,Actividad.fecha==fecha).all()
        if len(busqueda) == 0:
            print(fecha)
            print("hola")
            actividad = Actividad( denominacionActividad = denominacionActividad, fecha = fecha)
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

    """"INICIO ESTUDIANTE"""

    def agregar_estudiante(self, apellidoPaterno, apellidoMaterno, nombres, elegible):

        if (apellidoPaterno == " " and apellidoMaterno == " " and nombres == " " and elegible == " "):
            return False

        busqueda = session.query(Estudiante).filter(Estudiante.apellidoPaterno == apellidoPaterno, Estudiante.apellidoMaterno == apellidoMaterno, Estudiante.nombres == nombres, Estudiante.elegible == elegible ).all()
        if len(busqueda) == 0:
            estudiante = Estudiante(apellidoPaterno = apellidoPaterno, apellidoMaterno = apellidoMaterno, nombres = nombres, elegible = elegible)
            session.add(estudiante)
            session.commit()
            return True
        else:
            return False

    def editar_estudiante(self, idEstudiante, apellidoPaterno, apellidoMaterno, nombres, elegible):
        busqueda = session.query(Estudiante).filter(Estudiante.apellidoPaterno == apellidoPaterno,
                                                    Estudiante.apellidoMaterno == apellidoMaterno,
                                                    Estudiante.nombres == nombres,
                                                    Estudiante.elegible == elegible,
                                                    Estudiante.idEstudiante != idEstudiante).all()
        if len(busqueda) == 0:
            estudiante = session.query(Estudiante).filter(Estudiante.idEstudiante == idEstudiante).first()
            estudiante.apellidoPaterno = apellidoPaterno
            estudiante.apellidoMaterno = apellidoMaterno
            estudiante.nombres = nombres
            estudiante.elegible =elegible
            session.commit()
            return True
        else:
            return False

    def eliminar_estudiante(self, idEstudiante):
        try:
            estudiante = session.query(Estudiante).filter(Estudiante.idEstudiante == idEstudiante).first()
            session.delete(estudiante)
            session.commit()
            return True
        except:
            return False

    def dar_estudiante(self):
        estudiantes = [elem.__dict__ for elem in
                       session.query(Estudiante).all()]
        return estudiantes

    def dar_estudiante_por_idEstudiante(self, idEstudiante):
        return session.query(Estudiante).get(idEstudiante).__dict__

    def buscar_estudiante_por_nombresyapeEstudiante(self, apellidoPaterno, nombres):
        estudiantes = [elem.__dict__ for elem in
                       session.query(Estudiante).filter(
                           Estudiante.apellidoPaterno.ilike('%{0}%'.format(apellidoPaterno)),
                           Estudiante.nombres.ilike('%{0}%'.format(nombres))).all()]
        return estudiantes

