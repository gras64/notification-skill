from behave import given, then, when
from mycroft.messagebus.message import Message

@when('send test notification')
def notification_example(self): #example
    self.bus.emit(Message('notification:save',
                                {'skill': 'homeassistent', 'text': 'coffee is ready', 'time': 1}))
@when('delete test notification')
def del_notifivation_example(self): #example
    self.bus.emit(Message('notification:delete',
                        {'skill': 'homeassistent'}))