import unittest
from datetime import datetime
from src.seleccionestudiante.modelo.Asignatura import Asignatura
from src.seleccionestudiante.modelo.Estudiante import Estudiante
from src.seleccionestudiante.modelo.Equipo import Equipo
from src.seleccionestudiante.modelo.Actividad import Actividad
from src.seleccionestudiante.logica.Sorteo import Sorteo
from src.seleccionestudiante.modelo.declarative_base import Session

class AsignaturaTestCase ( unittest.TestCase ) :
    def setUp ( self ) :
        # Crea una sorteo para hacer las pruebas
        self.sorteo = Sorteo ( )

        # Abre la sesión
        self.session = Session ( )

        # crear estudiantes
        self.estudiante1 = Estudiante ( apellidoPaterno = "Bullon" , apellidoMaterno = "Arango" , nombres = "Fernando" ,
                              elegible = True )
        self.estudiante2 = Estudiante ( apellidoPaterno = "Solis" , apellidoMaterno = "Matos" , nombres = "Pedro" ,
                                   elegible = True )
        self.estudiante3 = Estudiante ( apellidoPaterno = "Paredes" , apellidoMaterno = "Torres" , nombres = "Luis Alberto" ,
                                   elegible = True )
        self.estudiante4 = Estudiante ( apellidoPaterno = "Garcia" , apellidoMaterno = "Mateo" , nombres = "Miguel Angel" ,
                                   elegible = True )

        self.session.add ( self.estudiante1 )
        self.session.add ( self.estudiante2 )
        self.session.add ( self.estudiante3 )
        self.session.add ( self.estudiante4 )
        self.session.commit ( )

        # crear asignatura
        self.asignatura1 = Asignatura ( nombreAsignatura = "Análisis y diseño de sistemas" )
        self.asignatura2 = Asignatura ( nombreAsignatura = "Pruebas de software" )
        self.session.add ( self.asignatura1 )
        self.session.add ( self.asignatura2 )
        self.session.commit ( )

        # crear equipo de trabajo
        self.equipo1 = Equipo ( denominacionEquipo = "Equipo01" )
        self.equipo2 = Equipo ( denominacionEquipo = "Equipo02" )
        self.session.add ( self.equipo1 )
        self.session.add ( self.equipo2 )
        self.session.commit ( )

        # crear actividad
        self.actividad1 = Actividad ( denominacionActividad = "Prueba unitaria" ,
                                 fecha = datetime ( 2021 , 9 , 28 , 00 , 00 , 00 , 00000 ) )
        self.actividad2 = Actividad ( denominacionActividad = "TDD" , fecha = datetime ( 2021 , 9 , 25 , 00 , 00 , 00 , 00000 ) )
        self.actividad3 = Actividad ( denominacionActividad = "BDD" , fecha = datetime ( 2021 , 9 , 25 , 00 , 00 , 00 , 00000 ) )
        self.session.add ( self.actividad1 )
        self.session.add ( self.actividad2 )
        self.session.add ( self.actividad3 )
        self.session.commit ( )

        # Relacionar Asignatura con estudiantes
        self.asignatura1.estudiantes = [ self.estudiante1 , self.estudiante4 ]
        self.asignatura2.estudiantes = [ self.estudiante2 , self.estudiante3 ]
        self.session.commit ( )

        # Relacionar equipo con estudiantes
        self.equipo1.estudiantes = [ self.estudiante1 , self.estudiante3 ]
        self.equipo2.estudiantes = [ self.estudiante2 , self.estudiante4 ]
        self.session.commit ( )

        # Relacionar Equipo de trabajo con actividad
        self.equipo1.actividades = [ self.actividad1 , self.actividad2 ]
        self.equipo2.actividades = [ self.actividad3 ]
        self.session.commit ( )

        self.session.close ( )

    def tearDown ( self ) :
        self.session = Session ( )

        estudiantes = self.session.query ( Estudiante ).all ( )
        for estudiante in estudiantes :
            self.session.delete ( estudiante )
        self.session.commit ( )
        self.session.close()

        asignaturas = self.session.query ( Asignatura ).all ( )
        for asignatura in asignaturas :
            self.session.delete ( asignatura )
        self.session.commit ( )
        self.session.close ( )

        actividades = self.session.query ( Actividad ).all ( )
        for actividad in actividades :
            self.session.delete ( actividad )
        self.session.commit ( )
        self.session.close ( )

        equipos = self.session.query ( Equipo ).all ( )
        for equipo in equipos :
            self.session.delete ( equipo )
        self.session.commit ( )
        self.session.close ( )

    def test_agregar_estudiante ( self ) :
        resultado = self.sorteo.agregar_estudiante ( apellidoPaterno = "Solis" , apellidoMaterno = "Serazo" , nombres = "Fabricio Martin" ,
                                   elegible = True )
        self.assertEqual ( resultado , True )

    def test_agregar_estudiante_repetido(self):
        resultado = self.sorteo.agregar_estudiante ( apellidoPaterno = "Bullon" , apellidoMaterno = "Arango" , nombres = "Fernando" ,
                              elegible = True)
        self.assertNotEqual(resultado, True)

    def test_verificar_almacenamiento_agregar_estudiante(self):
        self.sorteo.agregar_estudiante(apellidoPaterno = "Solis" , apellidoMaterno = "Serazo" , nombres = "Fabricio Martin" ,
                                   elegible = True)

        self.session = Session()
        estudiante = self.session.query(Estudiante).filter(Estudiante.apellidoPaterno == "Solis" , Estudiante.apellidoMaterno == "Serazo" ,
                                                           Estudiante.nombres == "Fabricio Martin" , Estudiante.elegible == True).first()

        self.assertEqual("Solis", estudiante.apellidoPaterno)
        self.assertEqual("Serazo", estudiante.apellidoMaterno)
        self.assertEqual("Fabricio Martin", estudiante.nombres)
        self.assertEqual(True, estudiante.elegible)

    def test_agregar_estudiantevacio(self):
        resultado = self.sorteo.agregar_estudiante(" "," "," "," ")
        self.assertFalse(resultado)

    def test_editar_estudiante(self):
        self.sorteo.editar_estudiante(1, "Bullon", "Arango", "Fernando", True)
        consulta = self.session.query(Estudiante).filter(Estudiante.idEstudiante == 1).first()
        self.assertIsNot(consulta.nombres, "Fernando Alcides")

    def test_eliminar_estudiante(self):
        self.sorteo.eliminar_estudiante(3)
        consulta = self.session.query(Estudiante).filter(Estudiante.idEstudiante == 3).first()
        self.assertIsNone(consulta)

    def test_dar_estudiante(self):
        estudiantes = self.sorteo.dar_estudiante()
        self.assertTrue(True)

    def test_dar_estudiante_por_id(self):
        self.sorteo.agregar_estudiante("Alvarado", "Torres", "Piero", True)
        idEstudiante = self.session.query(Estudiante).filter(Estudiante.apellidoPaterno == "Alvarado",
                                                             Estudiante.apellidoMaterno == "Torres",
                                                             Estudiante.nombres == "Piero",
                                                             Estudiante.elegible == True).first().idEstudiante
        consulta = self.sorteo.dar_estudiante_por_idEstudiante(idEstudiante)["apellidoPaterno"]
        consulta2 = self.sorteo.dar_estudiante_por_idEstudiante(idEstudiante)["apellidoMaterno"]
        consulta3 = self.sorteo.dar_estudiante_por_idEstudiante(idEstudiante)["nombres"]
        consulta4 = self.sorteo.dar_estudiante_por_idEstudiante(idEstudiante)["elegible"]
        self.assertEqual(consulta, ("Alvarado"))
        self.assertEqual(consulta2, ("Torres"))
        self.assertEqual(consulta3, ("Piero"))
        self.assertEqual(consulta4, (True))

    def test_buscar_estudiante_por_nomyapEstudiante(self):
        consulta1 = self.sorteo.buscar_estudiante_por_nombresyapeEstudiante("Paredes", "Luis Alberto")
        self.sorteo.agregar_estudiante("Torres", "Torres", "Paulino", True)
        consulta2 = self.sorteo.buscar_estudiante_por_nombresyapeEstudiante("Paredes", "Luis Alberto")
        self.assertLessEqual(len(consulta1), len(consulta2))

