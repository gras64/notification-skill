from mycroft import MycroftSkill, intent_file_handler


class Notification(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('notification.intent')
    def handle_notification(self, message):
        self.speak_dialog('notification')


def create_skill():
    return Notification()

