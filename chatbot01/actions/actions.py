# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []




from typing import Any,Text, Dict, List

# import datetime as dt 

import arrow   # for timezone logic
import dateparser
from numpy import diff
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

city_db = {  # need to check arrow class documentation anfd then redefine this dictionary
    'delhi': 'Asia/delhi',
    'India': 'Asia/India',
    'Amritsar': 'Asia/Amritsar',
    'Rajasthan': 'Asia/Rajasthan',
    'Mumbai':'Asia/Mumbai',
    'Kolkata':'Asia/kolkata',
    'Brussels':'Europe/brussels',
    'zagreb':'Europe/zagreb',
    'london' :'Europe/london',
    'amsterdam':'Europe/amsterdam',
    'seattle':'US/Pacific'
}

class ActionTellTime(Action):

    def name(self) -> Text:
        return "action_tell_time"    #------> name to refer to story , domain , rule ...

    def run(self, dispatcher: CollectingDispatcher,    #------> send messages back to the user
            tracker: Tracker,     #------>  Fetch information ,  Intent, Entities, Conversation sofar
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:    #------> data defines in domain.yml files
        
        current_place = next(tracker.get_latest_entity_values("place"), None) #---> get the value of entity place and if its unavailable then get the value none 
        ist = arrow.istnow()

        if not current_place:  #---> if no current place got detected then send back a general message 
            msg = f"It's{ist.format('HH:mm')} ist now. You can also give me a place."
            dispatcher.utter_message(text=msg) #---> dispatcher utter message back 
            return[]



# the place is detected but - in order to calculate the time , we are making use of a database resource here we are checking the city database ;
# and that's another one of these edge ; cases that we have to consider; here database is just a dictionary; pretend like actual db; 
# If the current place isn't in my db then send another msg to my user; that the bot didn't reconized it, may be the spelling is not collect


        tz_string = city_db.get(current_place,None)
        if not tz_string:
            msg = f"It's I didn't recognize {current_place}. It is spelled corrently?"
            dispatcher.utter_message(text=msg)
            return[]

        msg = f"It's{ist.to(city_db[current_place]).format('HH:mm')} in {current_place} now."
        dispatcher.utter_message(text=msg)
    
        return[]







class ActionRememberWhere(Action):

    def name(self) -> Text:
        return "action_remember_where"    #------> name to refer to story , domain , rule ...

    def run(self, dispatcher: CollectingDispatcher,    #------> send messages back to the user
            tracker: Tracker,     #------>  Fetch information ,  Intent, Entities, Conversation sofar
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:    #------> data defines in domain.yml files
        current_place = next(tracker.get_latest_entity_values("place"), None) #---> get the value of entity place and if its unavailable then get the value none 
        ist = arrow.istnow()
        

        if not current_place:  #---> if no current place got detected then send back a general message 
            msg = "I didn't get where you lived. Are you sure it's spelled correctly?"
            dispatcher.utter_message(text=msg) #---> dispatcher utter message back 
            return[]



# the place is detected but - in order to calculate the time , we are making use of a database resource here we are checking the city database ;
# and that's another one of these edge ; cases that we have to consider; here database is just a dictionary; pretend like actual db; 
# If the current place isn't in my db then send another msg to my user; that the bot didn't reconized it, may be the spelling is not collect


        tz_string = city_db.get(currnt_place,None)
        if not tz_string:
            msg = f"It's I didn't recognize {current_place}. It is spelled corrently?"
            dispatcher.utter_message(text=msg)
            return[]

        msg = f"Sure thing! I'll remember that you live in {current_place}."
        dispatcher.utter_message(text=msg)
    
        return[SlotSet("location", current_place)]

#_____________________________

class ActionTimeDifference(Action):

    def name(self) -> Text:
        return "action_time_difference"    #------> name to refer to story , domain , rule ...

    def run(self, dispatcher: CollectingDispatcher,    #------> send messages back to the user
            tracker: Tracker,     #------>  Fetch information ,  Intent, Entities, Conversation sofar
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:    #------> data defines in domain.yml files
        
        timezone_to = next(tracker.get_latest_entity_values("place"), None) #---> get the value of entity place and if its unavailable then get the value none 
        timezone_in = tracker.get_slot("location")

        if not timezone_in:  #---> if no current place got detected then send back a general message 
            msg = "To calculate the time difference I need to know where you live"
            dispatcher.utter_message(text=msg) #---> dispatcher utter message back 
            return[]

        if not timezone_to:  #---> if no current place got detected then send back a general message 
            msg = "I didn't get the timezone you'd like to compare against. Are you sure it's spelled correctly"
            dispatcher.utter_message(text=msg) #---> dispatcher utter message back 
            return[]

# the place is detected but - in order to calculate the time , we are making use of a database resource here we are checking the city database ;
# and that's another one of these edge ; cases that we have to consider; here database is just a dictionary; pretend like actual db; 
# If the current place isn't in my db then send another msg to my user; that the bot didn't reconized it, may be the spelling is not collect


        tz_string = city_db.get(currnt_place,None)
        if not tz_string:
            msg = f"It's I didn't recognize {current_place}. It is spelled corrently?"
            dispatcher.utter_message(text=msg)
            return[]

        t1 = arrow.istnow().to(city_db[timezone_to])
        t2 = arrow.istnow().to(city_db[timezone_in])
        max_t, min_t = max(t1, t2) , min(t1,t2)
        diff_seconds = dataparse.parse(str(max_t[:19])) - dataparse.parse(str(min_t[:19]))
        diff_hours = int(diff_seconds.seconds/3600)

        msg = f"There is a {min(diff_hours, 24-diff_hours)} H time difference."
        dispatcher.utter_message(text=msg)
    
       
        return[]

