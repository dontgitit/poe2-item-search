from dataclasses import dataclass
from enum import StrEnum, auto
import re

from itemparser.data import affixes

class FilterType(StrEnum):
    OPTION = auto()
    RANGE = auto()

@dataclass
class TypeInfo:
    line: str
    filter: str
    value: str
    filter_type: FilterType

@dataclass
class Equipment:
    line: str
    affix_id: str
    value: float

@dataclass
class Stat:
    line: str
    affix_id: str
    affix_type: str
    value: float

@dataclass
class Item:
    type_infos: list[TypeInfo]
    equipments: list[Equipment]
    stats: list[Stat]

    def is_empty(self):
        return not self.type_infos and not self.equipments and not self.stats


def get_quality(type_infos: list[TypeInfo]) -> int:
    return next((int(type_info.value) for type_info in type_infos if type_info.filter == 'quality'), 0)


def get_type_info(line: str) -> TypeInfo | None:
    # item class
    match = re.match(affixes.item_class_re, line)
    if match:
        item_class_name = match.group(1)
        # TODO - move item_class_to_filter to query building part
        item_class_filter = affixes.item_class_to_filter.get(item_class_name)
        if item_class_filter:
            # query['query']['filters']['type_filters']['filters']['category'] = {
            #     'option': item_class_filter
            # }
            return TypeInfo(line, 'category', item_class_filter, FilterType.OPTION)
    # rarity
    match = re.match(affixes.rarity_re, line)
    if match:
        rarity_name = match.group(1)
        # query['query']['filters']['type_filters']['filters']['rarity'] = {
        #     'option': rarity_name.lower()
        # }
        return TypeInfo(line, 'rarity', rarity_name.lower(), FilterType.OPTION)
    # quality
    match = re.match(affixes.quality_re, line)
    if match:
        return TypeInfo(line, 'quality', match.group(1), FilterType.RANGE)
    return None


def get_equipment_filter(line: str, type_infos: list[TypeInfo]) -> Equipment | None:
    quality = get_quality(type_infos)
    # armor stats
    for (regex, mod) in affixes.equipment_re:
        match = re.match(regex, line)
        if match:
            # print(f"line is {line} match is {match} with regex {regex}")
            stat_value = int(match.group(1))
            # print(f"defstat is {stat_value}, quality is {quality}")
            modified_value = stat_value * 1.2 if quality == 0 else stat_value * 1.2 / (1 + quality / 100.0)
            # query['query']['filters']['equipment_filters']['filters'][mod] = {
            #     'min': modified_value
            # }
            return Equipment(line, mod, modified_value)
    return None


def get_stat_filter(line: str) -> Stat | None:
    ## stats
    for (regex, mod) in affixes.affix_re:
        match = re.match(regex, line)
        # print(f"match of {regex} against {line} is {match}")
        if match:
            stat_value = match.group(1)
            mod_type = 'implicit' if match.group(2) else 'explicit'
            return Stat(line, mod, mod_type, stat_value)
            # stat_filter = create_stat_filter(mod_type, mod, stat_value)
            # query['query']['stats'][0]['filters'].append(stat_filter)
    return None


def parse_item(item_string) -> Item:
    print("item is " + item_string)
    # query = create_trade_request_body()
    type_infos: list[TypeInfo] = []
    equipments: list[Equipment] = []
    stats: list[Stat] = []
    for line in item_string.splitlines():
        if (type_info := get_type_info(line)) is not None:
            type_infos.append(type_info)
        if (equipment := get_equipment_filter(line, type_infos)) is not None:
            equipments.append(equipment)
        if (stat := get_stat_filter(line)) is not None:
            stats.append(stat)
    return Item(type_infos, equipments, stats)
