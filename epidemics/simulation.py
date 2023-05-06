from numpy import ndarray, zeros, float32, logical_and, where, roll, int8
from numpy.random import random

from epidemics.drawing import SimulationNdArrayWrapper, pygame_loop
import epidemics.parametersets as ps


class EpidemicSimulation(SimulationNdArrayWrapper):
    r"""
    In dieser Klasse wird Ihre Simulation laufen. Die Methoden **simulation_step** und **data_for_visulization**
    werden in jedem Frame durch die pygame_loop aufgerufen. Sie können die Simulation über die __init__ Methode
    konfigurieren, siehe Beispiel.
    """
    population_viral_load: ndarray
    infection_susceptibility: ndarray
    viral_load_half_time: float
    contact_infection_chance: float
    viral_load_recovered: float
    viral_load_susceptible: float

    def __init__(
            self,
            population_size: tuple[int, int],
            patient_zero: tuple[int, int],
            viral_load_half_time: float,
            contact_infection_chance: float,
            viral_load_recovered: float,
            viral_load_susceptible: float,
            infection_susceptibility_spread: float
    ):
        self.set_initial_state(population_size, patient_zero)
        self.infection_susceptibility = 1 + (random(population_size) - 0.5) * infection_susceptibility_spread
        self.viral_load_half_time = viral_load_half_time
        self.contact_infection_chance = contact_infection_chance
        self.viral_load_recovered = viral_load_recovered
        self.viral_load_susceptible = viral_load_susceptible

    def simulation_step(self):
        r"""
        Hier müssen Sie Ihre Simulationsschritte durchführen. Sie können natürlich weitere Methoden schreiben
        und Ihren Code weiter aufspalten.
        """
        self.speard_infection()
        self.reduce_viral_load()

    def speard_infection(self):
        random_variable = random(self.population_viral_load.shape)
        chance_no_infection = 1 - self.contact_infection_chance * self.infection_susceptibility
        chance_for_infection = 1 - chance_no_infection ** self.get_infected_neighbour_count()
        self.population_viral_load[
            logical_and(
                random_variable <= chance_for_infection,
                self.get_susceptible()
            )
        ] = 1

    def reduce_viral_load(self):
        self.population_viral_load -= self.population_viral_load / self.viral_load_half_time

    def get_infected_neighbour_count(self) -> ndarray:
        infected_population = self.get_infected()
        return (
                roll(infected_population, shift=1, axis=0) +
                roll(infected_population, shift=-1, axis=0) +
                roll(infected_population, shift=1, axis=1) +
                roll(infected_population, shift=-1, axis=1)
        )

    def data_for_visualization(self) -> list[ndarray]:
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
        return [
            self.get_infected() * 255,
            self.get_recovered() * 255,
            self.get_susceptible() * 255
        ]

    def get_infected(self) -> ndarray:
        return where(self.population_viral_load > self.viral_load_recovered, 1, 0)

    def get_recovered(self) -> ndarray:
        return where(
            logical_and(self.population_viral_load <= self.viral_load_recovered, self.population_viral_load > self.viral_load_susceptible),
            1,
            0
        )

    def get_susceptible(self) -> ndarray:
        return where(self.population_viral_load <= self.viral_load_susceptible, 1, 0)

    def set_initial_state(self, population_size: tuple[int, int], patient_zero: tuple[int, int]):
        self.population_viral_load = zeros(population_size, dtype=float32)
        self.population_viral_load[patient_zero] = 1


if __name__ == "__main__":
    active_set = ps.pulsing_infection_wave
    simulation = EpidemicSimulation(
        population_size=(700, 400),
        patient_zero=(350, 200),
        viral_load_half_time=active_set["viral_load_half_time"],
        contact_infection_chance=active_set["contact_infection_chance"],
        viral_load_recovered=active_set["viral_load_recovered"],
        viral_load_susceptible=active_set["viral_load_susceptible"],
        infection_susceptibility_spread=1
    )
    pygame_loop(simulation, size=(2800, 1600), fps=120)
    # size=(1200, 800) erzeugt ein Fenster mit der entsprechenden Auflösung, das funktioniert am besten mit Mehrfachen
    # der Simulationsdaten Größe
