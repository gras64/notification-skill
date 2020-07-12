from os.path import os, abspath, dirname, join
from mycroft.util import play_wav
from mycroft import MycroftSkill, intent_file_handler
from mycroft.messagebus.message import Message

REMINDER_PING = join(dirname(__file__), 'twoBeep.wav')


class Notification(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        self.settings["notifications"] = self.settings.get('notifications', [])
        self.settings["sound"] = self.settings.get('sound', True)
        self.settings["autoplay"] = self.settings.get('autoplay', True)
        self.settings["repetition"] = self.settings.get('repetition', 30)
        self.repetition = self.settings["repetition"]
        self.settings["timer"] = self.settings.get("timer", 30)
        self.notetime = 120 # max notification waittime
        self.add_event('notification:save',
                self.get_notification)
        self.add_event('notification:delete',
                self.del_notification)
        if len(self.settings["notifications"]) >= 1:
            self.set_bell(self.settings["timer"])
            self.ex_bell()
        self.register_intent_file('notification.intent', self.handle_notification)
        self.register_intent_file('del.notification.intent', self.delete_notification)
        #self.notification_example() #activate test
        #self.del_notifivation_example() #test2

    def notification_example(self): #example
        self.bus.emit(Message('notification:save',
                                {'skill': 'homeassistent', 'text': 'coffee is ready', 'time': 1}))

    def del_notifivation_example(self): #example
        self.bus.emit(Message('notification:delete',
                        {'skill': 'homeassistent'}))

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
                        {'skill': homeassistent}))'''
        skill = message.data.get("skill")
        notes = len(self.settings["notifications"])
        if notes >= 1:
            i = 0
            while i < notes:
                note = self.settings["notifications"][i]
                if skill in note["Skill"]:
                    self.log.info(note)
                    del self.settings["notifications"][i]
                i = i + 1
        if len(self.settings["notifications"]) < 1:
            self.unset_bell()

        

    def save_notification(self, skill, utter, time=30):
        self.set_bell(time)
        self.ex_bell()
        #self.register_intent_file('notification.intent', self.handle_notification)
        #self.repetition = []
        r = [{"Skill" : skill, "text": utter, "time": str(time)}]
        self.settings["notifications"] = self.settings['notifications'] + r
        self.log.info("save_notification "+str(self.settings["notifications"]))

    def set_bell(self, time=30):
        ## shortest time wins
        if self.notetime < time: 
            time = self.notetime
        self.notetime = time
        ##
        self.settings["timer"] = time
        self.schedule_repeating_event(self.ex_bell, None, time*60, name='notebell')
        if self.settings["autoplay"]:
            self.add_event('recognizer_loop:audio_output_end',
                        self.handle_notification)

    def ex_bell(self):
        self.enclosure.eyes_color(253, 158, 102)
        self.log.info("show picture")
        self.gui.show_image(abspath(dirname(__file__))+"/alarm-clock.jpg", fill='PreserveAspectFit')
        if self.settings["sound"]:
            play_wav(REMINDER_PING)
        self.log.info("notifacation available")

    def unset_bell(self):
        self.cancel_scheduled_event("notebell")
        self.bus.emit(Message('mycroft.eyes.default'))
        self.notetime = 120
        self.gui.clear()
        #self.remove_instance_handlers()
        #self.disable_intent("notification.intent")
        self.remove_event('recognizer_loop:audio_output_end')

    def handle_notification(self, message=None):
        notes = len(self.settings["notifications"])
        self.remove_event('recognizer_loop:audio_output_end')
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
        self.remove_event('recognizer_loop:audio_output_end')
        if len(self.settings["notifications"]) < 1:
            self.unset_bell()


    @intent_file_handler('del.notification.intent')
    def delete_notification(self, messages):
        self.settings["notifications"].clear()
        self.unset_bell()
        self.speak_dialog("del.notification")
        self.log.info(self.settings["notifications"])

    def shutdown(self):
        #self.remove_instance_handlers()
        self.remove_event('recognizer_loop:audio_output_end')
        self.cancel_scheduled_event("notebell")

def create_skill():
    return Notification()

