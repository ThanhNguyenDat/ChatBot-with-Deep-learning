from typing import Any, Text, Dict, List

import arrow
import dateparser
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

import pickle

# load model
file_name = ""
clf = pickle.load(open(file_name, 'rb'))

city_db = {
    'brussels': 'Europe/Brussels',
    'zagreb': 'Europe/Zagreb',
    'london': 'Europe/Dublin',
    'lisbon': 'Europe/Lisbon',
    'amsterdam': 'Europe/Amsterdam',
    'seattle': 'US/Pacific',
    'vietnam': 'Asia/Vietnam'
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
            msg = "I didn't the timezone you'd like to compare against. Are you sure it's spelled correctly?"
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
        diff_hours = int(diff_seconds.seconds / 3600)

        msg = f"There is a {min(diff_hours, 24 - diff_hours)}H time difference."
        dispatcher.utter_message(text=msg)

        return []


class ActionPix(Action):

    def name(self) -> Text:
        return 'action_pix'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get url
        image_url = tracker.latest_message["text"]
        if not image_url.startswith("http"):
            msg = "Please send face photo to get recommendation!"
            dispatcher.utter_message(text=msg)
            return []

        # Save image from url
        import urllib.request
        import numpy as np
        import cv2

        resource = urllib.request.urlopen(image_url)
        image = np.asarray(bytearray(resource.read()), dtype="uint8")
        frame = cv2.imdecode(image, cv2.IMREAD_COLOR)

        # Recogniztion
        msg = "Dang xu ly anh"
        dispatcher.utter_message(text=msg)
        return []
