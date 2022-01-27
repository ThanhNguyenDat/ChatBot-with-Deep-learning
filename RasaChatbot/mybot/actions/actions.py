from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

import pickle
from mtcnn import MTCNN
import arrow
import dateparser
import dlib
from imutils import face_utils
import cv2
import numpy as np
import sys
import os

# load model
file_name = "../face_models/model.sav"
clf = pickle.load(open(file_name, 'rb'))

desc_file = "../face_models/face_desc.csv"
f = open(desc_file, "r")
desc = f.readlines()
f.close()
dict = {}
for line in desc:
    dict[line.split('|')[0]] = [line.split('|')[1], line.split("|")[2], line.split("|")[3]]

detector = MTCNN()
predictor = dlib.shape_predictor("../face_models/shape_predictor_68_face_landmarks.dat")


city_db = {
    'brussels': 'Europe/Brussels',
    'zagreb': 'Europe/Zagreb',
    'london': 'Europe/Dublin',
    'lisbon': 'Europe/Lisbon',
    'amsterdam': 'Europe/Amsterdam',
    'seattle': 'US/Pacific',
    'newyork': 'America/New_York',
    'hochiminh': 'Vietnam/Ho_Chi_Minh'

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
        return "action_pix"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Xu ly hinh anh/nhan dien qua model
        image_url = tracker.latest_message["text"]
        print('----------------------------------------------------------------')
        print(image_url)
        print('----------------------------------------------------------------')
        print(tracker.latest_message)

        if image_url is not None:
            image_url
        if not image_url.startswith("http"):
            dispatcher.utter_message(text="Please send face photo to get recommendation!")
            return []

        # Save image from url
        import urllib.request
        import numpy as np
        import cv2
        resource = urllib.request.urlopen(image_url)
        image = np.asarray(bytearray(resource.read()), dtype="uint8")
        frame = cv2.imdecode(image, cv2.IMREAD_COLOR)

        # Nhan dien qua model de lay hinh dang khuon mat
        results = detector.detect_faces(frame)

        if len(results) != 0:
            for result in results:
                x1, y1, width, height = result['box']

                x1, y1 = abs(x1), abs(y1)
                x2, y2 = x1 + width, y1 + height

                # Extract dlib
                landmark = predictor(frame, dlib.rectangle(x1, y1, x2, y2))
                landmark = face_utils.shape_to_np(landmark)

                print("O", landmark.shape)
                landmark = landmark.reshape(68 * 2)
                print("R", landmark.shape)

                # Co ket qua du doan
                y_pred = clf.predict([landmark])
                print(y_pred)

                face_desc = dict[y_pred[0]][1]
                face_shape = dict[y_pred[0]][0]
                face_image = dict[y_pred[0]][2]

                dispatcher.utter_message(
                    text="Bạn có khuôn {}.\nCách chọn kình phù hợp: {}".format(face_shape.upper(), face_desc),
                    image=face_image)
                dispatcher.utter_message(text="Please send face photo to get recommendation!")

        return []
