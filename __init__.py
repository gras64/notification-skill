from os.path import dirname, join
from mycroft import MycroftSkill, intent_file_handler
from mycroft.messagebus.message import Message

REMINDER_PING = join(dirname(__file__), 'twoBeep.wav')


class Notification(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        note = []
        self.settings["notifications"] = self.settings.get('notifications', note)
        self.settings["sound"] = self.settings.get('sound', True)
        self.settings["repetition"] = self.settings.get('repetition', 60)
        self.add_event('notification:save',
                self.get_notification)
        self.add_event('notification:delete',
                self.del_notification)
        #self.add_notification()

    def add_notification(self): #test
        self.bus.emit(Message('notification:save',
                                {'skill': 'testskill', 'utterances': 'testutter'}))

    def get_notification(self, message):
        '''
        self.bus.emit(Message('notification:alert',
                        {'skill': 'testskill', 'utterances': 'testutter'}))'''

        skill = message.data.get("skill")
        utter = message.data.get("utterances")
        self.log.info("test :"+skill+ " and "+utter)
        self.save_notification(skill,utter)

    def del_notification(self,message):
        '''
        self.bus.emit(Message('notification:delete',
                        {'skill'}))'''
        pass

        

    def save_notification(self, skill, utter):
        self.set_bell()
        self.settings["notifications"] = self.settings["notifications"] + ([skill, utter])
        self.log.info("save_notification "+str(self.settings["notifications"]))

    def set_bell(self):
        self.schedule_repeating_event(self.ex_bell, self.settings["repetition"]*60, name='notebell')
        pass

    def ex_bell(self):
        self.enclosure.eyes_color(253, 158, 102)
        if self.settings["sound"]:
            play_wav(REMINDER_PING)

    def unset_bell(self):
        self.cancel_scheduled_event("notebell")
        self.bus.emit(Message('mycroft.eyes.default'))

    @intent_file_handler('notification.intent')
    def handle_notification(self, message):
        self.speak_dialog('notification')

    @intent_file_handler('del.notification.intent')
    def delete_notification(self, messages):
        #del self.settings["notifications"]
        self.unset_bell()
        self.speak_dialog("del.notification")


def create_skill():
    return Notification()

