Feature: Notification
    Scenario: user notification english
        Given an english speaking user
        Then the user says "Do you have any Notes for me" 
        Then "notification-skill" should reply with dialog from "no.notification.dialog"
        When send test notification
        Then mycroft should send the message "notification:save"
        Then the user says "Do you have any Notes for me" 
        Then "notification-skill" should reply with exactly "homeassistent coffee is ready"
        Then the user says "delete old notes"
        Then "notification-skill" should reply with dialog from "del.notification.dialog"


    Scenario: extern skill notification english
        Given an english speaking user
        When send test notification
        Then mycroft should send the message "notification:save"
        When delete test notification
        Then mycroft should send the message "notification:delete"