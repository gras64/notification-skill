from os.path import dirname, join
from mycroft.util import play_wav
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
        self.settings["repetition"] = self.settings.get('repetition', 30)
        self.repetition = self.settings["repetition"]
        self.notetime = 120 # max notification waittime
        self.add_event('notification:save',
                self.get_notification)
        self.add_event('notification:delete',
                self.del_notification)
        #self.notification_example() #activate test

    def notification_example(self): #example
        self.bus.emit(Message('notification:save',
                                {'skill': 'homeassistent', 'text': 'coffee is ready', 'time': 1}))

    def get_notification(self, message):
        '''
        self.bus.emit(Message('notification:alert',
                        {'skill': 'homeassistent', 'text': 'coffee is ready', 'time': 30}))'''

        skill = message.data.get("skill")
        utter = message.data.get("text")
        if message.data.get("time"):
            time = message.data.get("time")
        else:
            time = self.settings["repetition"]
        self.log.info("test :"+skill+ " and "+utter +" and "+str(time))
        self.save_notification(skill, utter, time)
        

    def del_notification(self, message):
        '''
        self.bus.emit(Message('notification:delete',
                        {'skill'}))'''
        pass

        

    def save_notification(self, skill, utter, time=30):
        self.set_bell(time)
        self.ex_bell()
        #self.repetition = []
        r = [{"Skill" : skill, "text": utter, "time": str(time)}]
        self.settings["notifications"] = self.settings['notifications'] + r
        self.log.info("save_notification "+str(self.settings["notifications"]))

    def set_bell(self, time):
        ## shortest time wins
        if self.notetime < time: 
            time = self.notetime
        self.notetime = time
        ##
        self.schedule_repeating_event(self.ex_bell, None, time*60, name='notebell')

    def ex_bell(self):
        self.enclosure.eyes_color(253, 158, 102)
        if self.settings["sound"]:
            play_wav(REMINDER_PING)
        self.log.info("notifacation available")

    def unset_bell(self):
        self.cancel_scheduled_event("notebell")
        self.bus.emit(Message('mycroft.eyes.default'))

    @intent_file_handler('notification.intent')
    def handle_notification(self, message):
        notes = len(self.settings["notifications"])
        if notes > 1:
            self.speak_dialog('notification', data={"notes":notes})
            i = 0
            while (i < notes) and (i < 4):
                note = self.settings["notifications"].pop()
                self.log.info(note)
                self.speak(note["Skill"]+" "+note["text"])
                i = i + 1
        elif notes == 1:
            note = self.settings["notifications"].pop()
            self.log.info(note)
            self.speak(note["Skill"]+" "+note["text"])
        else:
            self.speak_dialog('no.notification')
        self.log.info(self.settings["notifications"])


    @intent_file_handler('del.notification.intent')
    def delete_notification(self, messages):
        self.settings["notifications"].clear()
        self.unset_bell()
        self.speak_dialog("del.notification")
        self.log.info(self.settings["notifications"])

    def shutdown(self):
        self.cancel_scheduled_event("notebell")

def create_skill():
    return Notification()

