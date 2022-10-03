# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

import arrow 
import dateparser

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.executor import CollectingDispatcher
import webbrowser

city_db = {
    'Delhi' : 'Asia/India',
    'brussels': 'Europe/Brussels', 
    'zagreb': 'Europe/Zagreb',
    'london': 'Europe/Dublin',
    'lisbon': 'Europe/Lisbon',
    'amsterdam': 'Europe/Amsterdam',
    'seattle': 'US/Pacific',
    'berlin': 'Europe/Germany'
    
}


def generate_match_phrase_query(attribute: Text, value: Text) -> Dict:
    return {
        "match_phrase": {
            attribute: {
                "query": value
            }
        }
    }


class ActionTellTime(Action):

    def name(self) -> Text:
        return "action_tell_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_place = next(tracker.get_latest_entity_values("place"), None)
        utc = arrow.utcnow()
        
        if not current_place:
            msg = f"It's {utc.format('HH:mm')} utc now. You can also give me a place."
            dispatcher.utter_message(text=msg)
            return []
        
        tz_string = city_db.get(current_place, None)
        if not tz_string:
            msg = f"It's I didn't recognize {current_place}. Is it spelled correctly?"
            dispatcher.utter_message(text=msg)
            return []
                
        msg = f"It's {utc.to(city_db[current_place]).format('HH:mm')} in {current_place} now."
        dispatcher.utter_message(text=msg)
        
        return []


class ActionRememberWhere(Action):

    def name(self) -> Text:
        return "action_remember_where"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_place = next(tracker.get_latest_entity_values("place"), None)
        utc = arrow.utcnow()
        
        if not current_place:
            msg = "I didn't get where you lived. Are you sure it's spelled correctly?"
            dispatcher.utter_message(text=msg)
            return []
        
        tz_string = city_db.get(current_place, None)
        if not tz_string:
            msg = f"I didn't recognize {current_place}. Is it spelled correctly?"
            dispatcher.utter_message(text=msg)
            return []
        
        msg = f"Sure thing! I'll remember that you live in {current_place}."
        dispatcher.utter_message(text=msg)
        
        return [SlotSet("location", current_place)]


class ActionTimeDifference(Action):

    def name(self) -> Text:
        return "action_time_difference"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        timezone_to = next(tracker.get_latest_entity_values("place"), None)
        timezone_in = tracker.get_slot("location")
        
        if not timezone_in:
            msg = "To calculuate the time difference I need to know where you live."
            dispatcher.utter_message(text=msg)
            return []
        
        if not timezone_to:
            msg = "I didn't get the timezone you'd like to compare against. Are you sure it's spelled correctly?"
            dispatcher.utter_message(text=msg)
            return []
        
        tz_string = city_db.get(timezone_to, None)
        if not tz_string:
            msg = f"I didn't recognize {timezone_to}. Is it spelled correctly?"
            dispatcher.utter_message(text=msg)
            return []
        
        t1 = arrow.utcnow().to(city_db[timezone_to])
        t2 = arrow.utcnow().to(city_db[timezone_in])
        max_t, min_t = max(t1, t2), min(t1, t2)
        diff_seconds = dateparser.parse(str(max_t)[:19]) - dateparser.parse(str(min_t)[:19])
        diff_hours = int(diff_seconds.seconds/3600)
        
        msg = f"There is a {min(diff_hours, 24-diff_hours)}H time difference."
        dispatcher.utter_message(text=msg)
        
        return []




class ActionVideo(Action):
    def name(self) -> Text:
        return "action_video"

    async def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        video_url="https://youtu.be/DD-XQzVA38A"
        dispatcher.utter_message("wait... Playing your video.")
        webbrowser.open(video_url)
        return []

class ValidateRestaurantForm(Action):
    def name(self) -> Text:
        return "user_details_form"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        required_slots = ["name", "number"]

        for slot_name in required_slots:
            if tracker.slots.get(slot_name) is None:
                # The slot is not filled yet. Request the user to fill this slot next.
                return [SlotSet("requested_slot", slot_name)]

        # All slots are filled.
        return [SlotSet("requested_slot", None)]

class ActionSubmit(Action):
    def name(self) -> Text:
        return "action_submit"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template = "utter_details_thanks",
                                 Name=tracker.get_slot("name"),
                                 Mobile_number=tracker.get_slot("number"))

# 1.10.2022
class DocumentType(ABC):

    def __init__(self, index: Text, attributes: Dict[Text, Attribute]):
        self.index: Text = index
        self.attributes: Dict[Text, Attribute] = attributes

    @abstractmethod
    def to_string(self, document: Dict[Text, Any]) -> Text:
        pass
      
        
class TextAttribute(DefaultAttribute):
  
    def generate_query(self, value: Text, role: Text) -> Dict:
        return generate_match_phrase_query(self._name, value)




async def get_objects(
        self, object_type: Text, attributes: List[Dict[Text, Text]],
        limit: int = 5
    ) -> List[Dict[Text, Any]]:
        if object_type not in self.document_types:
            return []

        document_type = self.document_types[object_type]
        queries = [
            document_type.attributes[attribute["name"]].generate_query(
                attribute["value"], attribute.get("role", None))
            for attribute in attributes]
        query = {
            "size": limit,
            "query": {
                "bool": {
                    "must": queries
                }
            }
        }

        logger.info(f"Searching for {object_type} using {query}")
        index = document_type.index
        res = self.es.search(index=index, body=query)
        
        return [self.to_kb_obj(hit, object_type) for hit in res['hits']['hits']]

        # 3.10.22

        # action_query_knowledge_base