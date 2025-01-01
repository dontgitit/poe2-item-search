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

def r(mod):
    return fr"([+-]?\d+)%? (?:to )?{mod}( \(implicit\))?"

affix_re = [
    # prefixes
    (r('maximum Life'), 'stat_3299347043'),
    (r('maximum Mana'), 'stat_1050105434'),
    (r('increased Spell Damage'), 'stat_2974417149'),
    # suffixes
    (r('Strength'), 'stat_4080418644'),
    (r('Dexterity'), 'stat_3261801346'),
    (r('Intelligence'), 'stat_328541901'),
    (r('Fire Resistance'), 'stat_3372524247'),
    (r('Cold Resistance'), 'stat_4220027924'),
    (r('Lightning Resistance'), 'stat_1671376347'),
    (r('Chaos Resistance'), 'stat_2923486259'),
    (r('all Elemental Resistances'), 'stat_2901986750'),
    (r('increased Mana Regeneration Rate'), 'stat_789117908'),
    (r('increased Critical Hit Chance'), 'stat_587431675'),
    (r('increased Critical Damage Bonus'), 'stat_3556824919'),
    (r('increased Cast Speed'), 'stat_2891184298'),
    # Either
    (r('increased Rarity of Items found'), 'stat_3917489142'),
    # TODO - use correct accuracy filter depending on item class. for now just do non-weapon...
    # other accuracy
    (r('Accuracy Rating'), 'stat_803737631'),
    # weapon accuracy
    (r('Accuracy Rating'), 'stat_691932474'),
]

