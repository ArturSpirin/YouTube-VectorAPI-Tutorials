import functools
import time

import anki_vector
import requests
import json

from anki_vector.events import Events
from anki_vector.faces import Face


class Main:

    LAST_INTERACTION = 0

    def tell_joke(self, robot):
        response = requests.get("http://api.icndb.com/jokes/random?")
        if response.status_code == 200:
            joke = str(json.loads(response.content)["value"]["joke"])
            robot.conn.request_control()
            try:
                print(joke)
                robot.say_text(joke)
                Main.LAST_INTERACTION = time.time()
                robot.anim.play_animation("anim_eyecontact_giggle_01")
            finally:
                robot.conn.release_control()

    def on_object_observed(self, robot, event_type, event):

        if event_type == "object_observed":
            if isinstance(event.obj, Face):
                print("Face observed!")
                print("Id ", event.obj.face_id)
                print("Name ", event.obj.name)
                if time.time() - Main.LAST_INTERACTION > 30:
                    self.tell_joke(robot)
                else:
                    print("no time for jokes")

    def run(self):
        args = anki_vector.util.parse_command_args()
        with anki_vector.Robot(args.serial, enable_face_detection=True, take_control=False) as robot:
            on_object_observed = functools.partial(self.on_object_observed, robot)
            robot.events.subscribe(on_object_observed, Events.object_observed)
            while True:
                time.sleep(1)


if "__main__" == __name__:

    Main().run()
