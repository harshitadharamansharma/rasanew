# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from re import template
from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from rasa_sdk.events import SlotSet
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



class ActionFirstName(Action):

    def name(self) -> Text:
        # unique identifier of the form
        return "action_last_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(template="utter_last_name")

        return [SlotSet('firstN',tracker.latest_message['text'])]

# class ActionLastName(Action):

#     def name(self) -> Text:
#         # unique identifier of the form
#         return "action_feedback"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="utter_last_name")

#         return [SlotSet('lastN',tracker.latest_message['text'])] 


#
class ActionFeedbackSubmit(Action):

    def name(self) -> Text:
        # unique identifier of the form
        return "action_feedback_submit"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(template="utter_submit")

        return [SlotSet('feedback',tracker.latest_message['text'])] 



class ActionFeedback(Action):

    def name(self) -> Text:
        # unique identifier of the form
        return "action_feedback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(template="utter_feedback")

        return [SlotSet('lastN',tracker.latest_message['text'])] 


class ActionSubmit(Action):

    def name(self) -> Text:
        # unique identifier of the form
        return "action_submit"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Your first name is : {0}\n your last name is : {1}\n your feedback is : {2}\n".format(
            tracker.get_slot("firstN"),tracker.get_slot("lastN"), tracker.get_slot("feedback")))
        
        return [] 