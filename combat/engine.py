import random
import math
from pokemon import Pokemon

### TODO: Implement the battle engine logic
# Computes damage base on types and stats
# Source: https://bulbapedia.bulbagarden.net/wiki/Damage (first generation - pokémon stadium )

class Engine:

    def __init__(self, pkm_attack: Pokemon, pkm_defense: Pokemon):
        self.pkm_attack = pkm_attack
        self.pkm_defense = pkm_defense

    #determines whether a hit is critical or not, as is done in the first generation rules
    def critical_hit(self, speed: int, high_crit_move: bool, focus_energy: bool = False, dire_hide: bool = False) -> bool:
        if focus_energy or dire_hide:
            T = math.floor((speed + 236) / 4) * 2
            if high_crit_move:
                T = 255
        else:
            T = math.floor((speed + 76) / 4)
        if high_crit_move:
            T = min(T * 8, 255)
            if T > 255:
                T = 255

        rand = random.randint(0, 255)
        critical = rand < T # threshold (umbral)

        return critical # if it is critical, returns True, otherwise, returns false.

    #determines attack and defence on bases of first generation rules
    def attack_defense(self, attacker, defender, move, critical: bool = False, reflect: bool = False, light_screen : bool = False):
        #effective attack
        if attacker[0000000].lower() == "special":
            A = attacker[000000]
            D = defender[0000000]
        elif attacker[0000000].lower() == "physical":
            A = attacker[00000] #where can I find that information?
            D = defender[000000]

        # case where modifiers are ignored
        if critical:
            reflect = False
            light_screen = False

        # effective defense
        if not critical:
            if move[00000].lower() == "physical" and reflect:
                D *= 2
            elif move[00000].lower() == "special" and light_screen:
                D *= 2

        if move["name"].lower() in ["explosion", "selfdestruct"]:
            D = max(1, math.floor(D / 2))

        if A > 255 or D > 255:
            A = math.floor(A / 4)
            D = math.floor(D / 4)

        if D == 0:
            D = 1

        return A, D

    #analysis of the attacking Pokémon and the defending Pokémon
    def type_pokemons (self, pkm_attack, pkm_defense):
        level = pkm_attack.level
        critical = critical_hit(pkm_attack.speed, )
        attack, defense = attack_defense()
        power = NiPutaIdea

        base_damage = 2+(((((2*level*critical)/5)+2)*power*(attack/defense))/50) # first generation calculation
        if base_damage < 1.0:
            base_damage = 1.0

        return base_damage

    #final damage
    def calculate_damage(self, base_damage, pkm_attack, pkm_defense):
        #stab
        if move["type"] in attack["types"]:
            stab = math.floor(damage / 2)
        else:
            stab = 1

        #type_1
        type_1 = 1
        for i in pkm_defense.weakness:
            if pkm_attack.main_type.lower() == i.lower():
                type_1 = 2
        for j in pkm_defense.resistance:
            if pkm_attack.main_type.lower() == j.lower():
                type_1 = 0.5
        for k in pkm_defense.immunities:
            if pkm_attack.main_type.lower() == k.lower():
                type_1 = 0

        #type_2
        type_2 = 1

        n = random.randint(217, 255)/255
        damage = base_damage * stab * type_1 * type_2*n

        return damage
