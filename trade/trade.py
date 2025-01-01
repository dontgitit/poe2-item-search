import json
from collections import defaultdict
from urllib.parse import quote_plus

from itemparser.data.affixes import Affix, affixes as all_affixes, Pseudo
from itemparser.item_parser import Item, Stat, FilterType

trade_url = 'https://www.pathofexile.com/trade2/search/poe2/Standard'


def get_trade_url(query):
    return f"{trade_url}?q={quote_plus(json.dumps(query))}"


def create_trade_request_body():
    return {
        'query': {
            'status': {
                'option': 'onlineleague'
            },
            'stats': [
                {
                    'type': 'and',
                    'filters': []
                }
            ],
            'filters': {
                'type_filters': {
                    'disabled': False,
                    'filters': {}
                },
                'equipment_filters': {
                    'filters': {}
                }
            }
        },
        'sort': {
            'price': 'asc'
        }
    }


def get_type_filters(item: Item) -> dict:
    if item.type_infos:
        type_filters = {
            'filters': {}
        }
        f = {}
        for type_info in item.type_infos:
            if type_info.filter == 'rarity' and type_info.value == 'currency':
                # there's no currency rarity on trade site
                continue
            if not type_info.create_filter:
                continue

            if type_info.filter_type is FilterType.OPTION:
                f = {'option': type_info.value}
            elif type_info.filter_type is FilterType.RANGE:
                f = {'min': type_info.value}
            else:
                raise ValueError(f"{type_info.filter_type} is an unhandled FilterType")
            type_filters['filters'][type_info.filter] = f

        return type_filters

    return {}


def get_equipment_filters(item: Item) -> dict:
    if item.equipments:
        equipments = {
            'filters': {}
        }
        for equipment in item.equipments:
            equipments['filters'][equipment.affix_id] = {
                'min': equipment.value
            }
        return equipments
    return {}


def create_affix_filter(affix: Affix, affix_type: str, disabled: bool = False, min: float | None = None, weight: float | None = None):
    value = {}
    if min is not None:
        value['min'] = min
    if weight is not None:
        value['weight'] = weight
    return {
        'id': f"{affix_type}.stat_{affix.trade_id}",
        'disabled': disabled,
        'value': value,
    }


def create_stat_filter(stat: Stat):
    return create_affix_filter(stat.affix, stat.affix_type, min=stat.value, disabled=not not stat.affix.pseudos)


def get_pseudo_by_hint(affix: Affix, pseudo_hint: str) -> Pseudo | None:
    return next((pseudo for pseudo in affix.pseudos if pseudo.hint == pseudo_hint), None)


def create_weight_filter(pseudo_hint: str, affixes: list[Affix], total: float):
    # TODO - would be nice to also include `enchant` and `rune` but that leads to `query too complex` from trade...
    filters = [create_affix_filter(affix, affix_type, weight=get_pseudo_by_hint(affix, pseudo_hint).weight) for affix_type in ['explicit', 'implicit'] for affix in affixes]
    return {
        'type': 'weight2',
        'filters': filters,
        'value': {
            'min': total
        }
    }


def affix_is_part_of_pseudo_hint(affix: Affix, pseudo_hint: str) -> bool:
    return not not get_pseudo_by_hint(affix, pseudo_hint)


def get_affixes_for_hint(hint: str) -> list[Affix]:
    return [affix for affix in all_affixes if affix_is_part_of_pseudo_hint(affix, hint)]


def get_stat_filters(item: Item) -> list[dict]:
    if item.stats:
        and_filter = {
            'type': 'and',
            'filters': [create_stat_filter(stat) for stat in item.stats]
        }

        pseudos = defaultdict(float)
        for stat in item.stats:
            for pseudo in stat.affix.pseudos:
                pseudos[pseudo.hint] += stat.value * pseudo.weight
        pseudo_filters = [
            create_weight_filter(hint, get_affixes_for_hint(hint), total)
            for (hint, total) in pseudos.items()
        ]
        return [and_filter] + pseudo_filters
    return []


def item_to_trade_json(item: Item) -> dict:
    request = create_trade_request_body()
    if type_filters := get_type_filters(item):
        request['query']['filters']['type_filters'] = type_filters
    if equipment_filters := get_equipment_filters(item):
        request['query']['filters']['equipment_filters'] = equipment_filters
    if stat_filters := get_stat_filters(item):
        request['query']['stats'] = stat_filters
    return request
