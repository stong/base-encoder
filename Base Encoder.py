from time import sleep
import base64
import sublime
import sublime_plugin
import threading


class Base64EncodeCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        performConversion(base64.b64encode, self, edit)


class Base64DecodeCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        performConversion(base64.b64decode, self, edit)


class Base32EncodeCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        performConversion(base64.b32encode, self, edit)


class Base32DecodeCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        performConversion(base64.b32decode, self, edit)


class Base16EncodeCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        performConversion(base64.b16encode, self, edit)


class Base16DecodeCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        performConversion(base64.b16decode, self, edit)


class CleanStatusThread(threading.Thread):

    def __init__(self, sleep_seconds, view):

        self.sleep_time = sleep_seconds
        self.view = view

        threading.Thread.__init__(self)

    def run(self):

        sleep(self.sleep_time)

        self.view.erase_status('base_encoder')


#-----------------------------------------------------------------------------


def performConversion(convertFunc, command, edit):

    UTF_8 = 'UTF-8'

    success_count = 0
    failure_count = 0

    for selection in command.view.sel():

        try:
            selected_text = command.view.substr(selection)

            if (len(selected_text) > 0):
                selected_bytes = bytes(selected_text, UTF_8)
                converted_output = str(convertFunc(selected_bytes), UTF_8)

                command.view.replace(edit, selection, converted_output)
                success_count += 1

        except:
            failure_count += 1

    updateStatus(convertFunc, success_count, failure_count, command.view)


def getTaskDescription(convertFunc):

    taskDescriptions = dict(zip(
        [base64.b64encode, base64.b64decode, base64.b32encode,
            base64.b32decode, base64.b16encode, base64.b16decode],
        ["Base-64 encoding", "Base-64 decoding", "Base-32 encoding",
            "Base-32 decoding", "Base-16 encoding", "Base-16 decoding"]))

    return taskDescriptions[convertFunc]


def updateStatus(convertFunc, success_count, failure_count, view):

    message = getTaskDescription(convertFunc) + ": "

    if (success_count > 0):
        item = "items" if (success_count > 1) else "item"
        message += str(success_count) + " successful " + item

    if (failure_count > 0):
        if (success_count > 0):
            message += ", "

        item = "items" if (failure_count > 1) else "item"
        message += str(failure_count) + " failed " + item

    view.set_status('base_encoder', message)

    clean_status = CleanStatusThread(10, view)
    clean_status.start()
