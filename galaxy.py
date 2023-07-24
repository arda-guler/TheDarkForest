import random
import math

intelligence_classes = ["EXPANSIONIST", "ISOLATIONIST", "SELF-RESTRICTING", "TOMB"]

class Sector:
    def __init__(self, resource, life, intelligence, pos):
        self.resource = resource
        self.life = life
        self.intelligence = intelligence
        self.explored = False
        self.pos = pos
        self.progress = 0

        if self.resource:
            self.resource_amount = random.uniform(1, 6)
        else:
            self.resource_amount = 0

        if self.intelligence:
            self.intelligence_class = random.choice(intelligence_classes)
            self.population = min(int(5_000_000 * 10**(self.resource_amount + math.log(self.progress**0.05 + 0.01) - random.uniform(0, 1))), int(self.resource_amount*10_000_000_000))

            if self.intelligence_class == "TOMB":
                self.population *= 0.01
                self.population = int(self.population)

        if self.intelligence:
            if self.intelligence_class == "EXPANSIONIST":
                self.signal_strength_multiplier = 1
            elif self.intelligence_class == "ISOLATIONIST":
                self.signal_strength_multiplier = 0.4
            elif self.intelligence_class == "SELF-RESTRICTING":
                self.signal_strength_multiplier = 0.2
            else: # TOMB
                self.signal_strength_multiplier = 0
        else:
            self.signal_strength_multiplier = 0

    def do_progress(self):
        if self.intelligence:
            if self.intelligence_class == "EXPANSIONIST":
                progress_chance = 0.7
            elif self.intelligence_class == "ISOLATIONIST":
                progress_chance = 0.1
            elif self.intelligence_class == "SELF-RESTRICTING":
                progress_chance = 0.005
            else: # TOMB
                progress_chance = 0

            progress_roll = random.uniform(0, 1)
            if progress_roll < progress_chance:
                self.progress += 1

            # civilization changes their grand plan doctrine (or destroys itself!)
            if not self.intelligence_class == "TOMB":
                doctrine_roll = random.uniform(0, 1)
                if doctrine_roll > 0.9995:
                    self.intelligence_class = random.choice([x for x in intelligence_classes if x != self.intelligence_class])

            self.signal_strength = self.signal_strength_multiplier * self.progress
            self.population = min(int(5_000_000 * 10 ** (self.resource_amount + math.log(self.progress**0.05 + 0.01) - random.uniform(0, 1))), int(self.resource_amount*10_000_000_000))
            if self.intelligence_class == "TOMB":
                self.population *= 0.01
                self.population = int(self.population)

class Galaxy:
    def __init__(self, size=[30, 30], emptiness=1, resources=0.2, life=0.08, intelligence=0.02):
        self.size = size
        self.resources = resources
        self.emptiness = emptiness
        self.life = life
        self.intelligence = intelligence

        self.generate_sectors()

    def generate_sectors(self):
        size_x = self.size[0]
        size_y = self.size[1]

        self.num_sectors = size_x * size_y

        chance_intelligence = self.resources + self.life + self.emptiness
        chance_life = self.resources + self.emptiness
        chance_resources = self.emptiness
        chance_normalization = self.resources + self.life + self.intelligence + self.emptiness

        sectors = []
        for idx_y in range(size_y):
            sectors.append([])
            for idx_x in range(size_x):

                sector_chance = random.uniform(0, chance_normalization)

                if sector_chance > chance_intelligence:
                    new_sector = Sector(1, 1, 1, [idx_x, idx_y])

                elif sector_chance > chance_life:
                    new_sector = Sector(1, 1, 0, [idx_x, idx_y])

                elif sector_chance > chance_resources:
                    new_sector = Sector(1, 0, 0, [idx_x, idx_y])

                else:
                    new_sector = Sector(0, 0, 0, [idx_x, idx_y])

                sectors[idx_y].append(new_sector)

        self.sectors = sectors
