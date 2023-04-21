import numpy as np

from epidemics.drawing import SimulationNdArrayWrapper, pygame_loop


class EpidemicSimulation(SimulationNdArrayWrapper):
    r"""
    In dieser Klasse wird Ihre Simulation laufen. Die Methoden **simulation_step** und **data_for_visulization**
    werden in jedem Frame durch die pygame_loop aufgerufen. Sie können die Simulation über die __init__ Methode
    konfigurieren, siehe Beispiel.
    """

    # my_data_matrix: ndarray

    def __init__(self):  # __init__(self, simulation_size: tuple[int, int])
        # self.my_data_matrix = np.zeros(simulation_size)
        pass

    def simulation_step(self):
        r"""
        Hier müssen Sie Ihre Simulationsschritte durchführen. Sie können natürlich weitere Methoden schreiben
        und Ihren Code weiter aufspalten.
        """
        pass

    def data_for_visualization(self) -> list[np.ndarray]:
        r"""
        Hier geben Sie eine Liste an Matrizen zurück, die dann für die Visualisierung genutzt werden. Dabei gilt
        für den Rückgabewert

        :returns
        list[numpy.ndarray]: Liste von numpy Matrizen dabei gibt es verschiedene Optionen
            [numpy.ndarray] - Eine Matrix erzeugt eine einfarbige Ausgabe
            [numpy.ndarray, numpy.ndarray, numpy.ndarray] - Drei Matrizen füllen die Farbkanäle RGB
            [numpy.ndarray, numpy.ndarray, numpy.ndarray, numpy.ndarray] - Vier Matrizen füllen dann zusätzlich noch
                den alpha Kanal
            ACHTUNG: Die Farbwerte gehen von 0 bis 255!
        """
        return []


if __name__ == "__main__":
    simulation = EpidemicSimulation()
    pygame_loop(simulation, size=(1200, 800), fps=120)
    # size=(1200, 800) erzeugt ein Fenster mit der entsprechenden Auflösung, das funktioniert am besten mit Mehrfachen
    # der Simulationsdaten Größe
