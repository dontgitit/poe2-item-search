from dataclasses import dataclass, field

item_class_to_filter = {
    'Helmets': 'armour.helmet',
    'Body Armours': 'armour.chest',
    'Belts': 'accessory.belt',
    'Amulets': 'accessory.amulet',
    'Rings': 'accessory.ring',
    'Gloves': 'armour.gloves',
    'Boots': 'armour.boots',
    'Wands': 'weapon.wand',
    'Foci': 'armour.focus',
    'Life Flasks': 'flask.life',
    'Mana Flasks': 'flask.mana',
    'Socketable': 'currency.socketable',
    'Stackable Currency': 'currency',
}

item_class_re = r"Item Class: (.+)"
rarity_re = r"Rarity: (.+)"
quality_re = r"Quality: \+(\d+)%"
equipment_re = [
    (r"Energy Shield: (\d+)", 'es'),
    # the extra stuff for `Armour` is to avoid matching `Armour: ` lines on socketables (runes and soul cores)
    (r"Armour: (\d+)(?:$| \()", 'ar'),
    (r"Evasion Rating: (\d+)", 'ev'),
]


@dataclass
class Pseudo:
    hint: str
    weight: float = 1


@dataclass
class Affix:
    mod: str
    trade_id: str
    pseudos: list[Pseudo] = field(default_factory=list)

    def __post_init__(self):
        self.regex = fr"([+-]?\d+)%? (?:to )?{self.mod}( \(implicit\))?"


affixes = [
    # prefixes
    Affix('maximum Life', '3299347043'),
    Affix('maximum Mana', '1050105434'),
    Affix('increased Spell Damage', '2974417149'),
    # suffixes
    Affix('Strength', '4080418644', [Pseudo('stat')]),
    Affix('Dexterity', '3261801346', [Pseudo('stat')]),
    Affix('Intelligence', '328541901', [Pseudo('stat')]),
    Affix('All Attributes', '1379411836', [Pseudo('stat', weight=3)]),
    Affix('Fire Resistance', '3372524247', [Pseudo('resist')]),
    Affix('Cold Resistance', '4220027924', [Pseudo('resist')]),
    Affix('Lightning Resistance', '1671376347', [Pseudo('resist')]),
    Affix('Chaos Resistance', '2923486259', [Pseudo('resist', weight=1.5)]),
    Affix('all Elemental Resistances', '2901986750', [Pseudo('resist', weight=3)]),
    Affix('increased Mana Regeneration Rate', '789117908'),
    Affix('increased Critical Hit Chance', '587431675'),
    Affix('increased Critical Damage Bonus', '3556824919'),
    Affix('increased Cast Speed', '2891184298'),
    # Either
    Affix('increased Rarity of Items found', '3917489142'),
    # TODO - use correct accuracy filter depending on item class. for now just do non-weapon...
    # other accuracy
    Affix('Accuracy Rating', '803737631'),
    # weapon accuracy
    Affix('Accuracy Rating', '691932474'),
]
