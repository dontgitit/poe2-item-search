import json
from urllib.parse import quote_plus

from itemparser.item_parser import Item, Stat, FilterType

# online_filter = ['any', 'online', 'onlineleague']
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


def create_stat_filter(stat: Stat):
    return {
        'id': f"{stat.affix_type}.stat_{stat.affix.trade_id}",
        'disabled': False,
        'value': {
            'min': stat.value
        }
    }


def get_stat_filters(item: Item) -> list[dict]:
    if item.stats:
        return [
            {
                'type': 'and',
                'filters': [create_stat_filter(stat) for stat in item.stats]
            }
        ]
    return []
    # stat_filter = create_stat_filter(mod_type, mod, stat_value)
    # query['query']['stats'][0]['filters'].append(stat_filter)


def item_to_trade_json(item: Item) -> dict:
    request = create_trade_request_body()
    if type_filters := get_type_filters(item):
        request['query']['filters']['type_filters'] = type_filters
    if equipment_filters := get_equipment_filters(item):
        request['query']['filters']['equipment_filters'] = equipment_filters
    if stat_filters := get_stat_filters(item):
        request['query']['stats'] = stat_filters
    return request
