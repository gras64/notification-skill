# <img src="https://raw.githack.com/FortAwesome/Font-Awesome/master/svgs/solid/comments.svg" card_color="#40DBB0" width="50" height="50" style="vertical-align:bottom"/> Notification
Other skills can save notifications here and have them called up later

## About
Other skills can save notifications here and have them called up later. As soon as there is a hint, the LED ring lights up orange and a notification bell sounds every few minutes

## Examples
* "Do you have any Notes for me"
* "There is something Notes for me"
* "delete old notes"
* "you can delete your old notes"


## notification from other skills

Save Notifications
```python 
def notification_example(self):
    self.emitter.emit(Message('notification:save',
                            {'skill': 'testskill', 'message': 'testutter', 'time': 30}))
```
'skill' = name of your skill
'text' = Speak text
'time' = time in minute between beep (optional)

Delete Notifications
```python 
def notification_example(self):
    self.emitter.emit(Message('notification:delete',
                            {'skill': 'testskill'}))
```

## Credits
gras64

## Category
**Daily**
Productivity

## Tags
#Notification

