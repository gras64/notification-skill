# <img src="https://raw.githack.com/FortAwesome/Font-Awesome/master/svgs/solid/comments.svg" card_color="#40DBB0" width="50" height="50" style="vertical-align:bottom"/> Notification
Other skills can save notifications here and have them called up later

## About
Other skills can save notifications here and have them called up later

## Examples
* "Do you have any news for me"
* "There is something new for me"

## send notification from other skills

```python
... 
def notification_example(self):
    self.bus.emit(Message('notification:save',
                            {'skill': 'testskill', 'utterances': 'testutter'}))
...
```

## Credits
gras64

## Category
**Daily**
Productivity

## Tags
#Notification

