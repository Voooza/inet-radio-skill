from mycroft import MycroftSkill, intent_file_handler


class InetRadio(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('radio.inet.intent')
    def handle_radio_inet(self, message):
        self.speak_dialog('radio.inet')


def create_skill():
    return InetRadio()

