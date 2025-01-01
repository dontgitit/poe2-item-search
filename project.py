import json
from pynput.keyboard import Controller, GlobalHotKeys, Key
import pyperclip
import time
import webbrowser

from itemparser.item_parser import parse_item
from trade.trade import item_to_trade_json, get_trade_url

controller = Controller()


def copy_item():
    # CAN'T PRESS CTRL AGAIN OR IT MAKES IT STICKY! BECAUSE IT'S ALREADY PRESSED DURING MACRO
    # https://stackoverflow.com/questions/73682630/pynput-non-specified-key-combo-triggers-hotkey-fxn-after-alt-tab-windows
    with controller.pressed(Key.ctrl):
        controller.tap('c')


global listener

def start_price_check():
    # print('starting price check')
    # copy sends keyboard stuff which seems to mess with the listener
    listener.stop()
    copy_item()
    # sleep for a bit to wait for PoE to update clipboard
    time.sleep(0.3)
    item_string = pyperclip.paste()
    item = parse_item(item_string)
    if item.is_empty():
        print('no parsed mods')
    else:
        js = item_to_trade_json(item)
        # print('search is '+json.dumps(js, indent=None))
        url = get_trade_url(js)
        print(url)
        webbrowser.open(url, new=0, autoraise=True)


def main():
    # for some reason the hotkey turns sticky (pressing CTRL or D again, separately, will fire the lambda)
    while True:
        # print("starting listener")
        with GlobalHotKeys({
            '<ctrl>+d': start_price_check
        }) as h:
            global listener
            listener = h
            h.join()


if __name__ == "__main__":
    main()
