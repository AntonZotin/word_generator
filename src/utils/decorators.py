import traceback

import PySimpleGUI as Gui


def exception_handler(callee):
    def upd(*args, **kwargs):
        try:
            return callee(*args, **kwargs)
        except Exception as e:
            Gui.PopupAnimated(None)
            tb = traceback.format_exc()
            Gui.popup_error(f'An error happened. Here is the info:', e, tb)
            return 0
    return upd
