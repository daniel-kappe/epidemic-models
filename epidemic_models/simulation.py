from typing import NamedTuple
from numpy import (
    random,
    ndarray,
    ones,
    zeros,
    roll,
    logical_and,
    stack,
    ceil,
    sum,
    int8,
)

from epidemic_models.drawing import SimulationNdArrayWrapper, pygame_loop


class DiseaseParameters(NamedTuple):
    infection_chance: float
    infectious_days: int
    immun_days: int


class EpidemicSimulation:
    infection_chance: float
    immunity_decay: float
    infection_decay: float
    susceptible_population: ndarray
    infection_strength: ndarray
    immunity_strength: ndarray

    def __init__(
        self,
        population: tuple[int, int],
        patient_zero: tuple[int, int],
        disease_parameters: DiseaseParameters,
    ):
        self.susceptible_population = ones(population)
        self.susceptible_population[patient_zero] = 0
        self.infection_strength = zeros(population)
        self.infection_strength[patient_zero] = 1
        self.immunity_strength = zeros(population)
        self.infection_chance = disease_parameters.infection_chance
        self.infection_decay = 1 / disease_parameters.infectious_days
        self.immunity_decay = 1 / disease_parameters.immun_days

    def update_population(self):
        susceptible_population = self.susceptible_population > 0
        infected_population = self.infection_strength > 0
        immun_population = self.immunity_strength > 0
        infected_neighbours = self.count_neighbours(infected_population)
        new_infections = self.newly_infected(
            infected_neighbours, susceptible_population
        )
        recovered = logical_and(
            self.infection_strength <= self.infection_decay, infected_population
        )
        no_longer_immun = logical_and(
            self.immunity_strength <= self.immunity_decay, immun_population
        )
        self.infection_strength[self.infection_strength > 0] -= self.infection_decay
        self.immunity_strength[self.immunity_strength > 0] -= self.immunity_decay
        self.infection_strength[recovered] = 0
        self.immunity_strength[recovered] = 1
        self.immunity_strength[no_longer_immun] = 0
        self.susceptible_population[no_longer_immun] = 1
        self.susceptible_population[new_infections] = 0
        self.infection_strength[new_infections] = 1

    def newly_infected(self, infected_neighbours, susceptible_population):
        infection_chance = 1 - (1 - self.infection_chance) ** infected_neighbours
        random_variable = random.random(infected_neighbours.shape)
        new_infections = logical_and(
            infection_chance >= random_variable, susceptible_population
        )
        return new_infections

    def count_neighbours(self, infected_population):
        return sum(
            [
                roll(infected_population, shift=1, axis=0),
                roll(infected_population, shift=-1, axis=0),
                roll(infected_population, shift=1, axis=1),
                roll(infected_population, shift=-1, axis=1),
            ],
            axis=0,
            dtype=int8,
        )

    def to_rgba(self):
        return stack(
            [
                ceil(self.infection_strength) * 255,
                ceil(self.immunity_strength) * 255,
                self.susceptible_population * 255,
            ],
            axis=-1,
        )


if __name__ == "__main__":
    parameter_sets: dict[str, DiseaseParameters] = {
        "single_wave": DiseaseParameters(0.1, 14, 90),
        "continuous_waves": DiseaseParameters(0.1, 14, 30),
        "meander": DiseaseParameters(0.05, 14, 30),
        "die_out": DiseaseParameters(0.05, 11, 30),
    }
    population_shape = (600, 400)
    patient_zero = (population_shape[0] // 2, population_shape[1] // 2)
    sim = EpidemicSimulation(
        population=population_shape,
        patient_zero=patient_zero,
        disease_parameters=parameter_sets["meander"],
    )
    wrapper = SimulationNdArrayWrapper(sim.update_population, sim.to_rgba)
    pygame_loop(wrapper, size=(1800, 1200), fps=250)
