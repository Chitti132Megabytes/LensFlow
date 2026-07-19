from mediapipe.tasks.cc.vision.gesture_recognizer.proto import gesture_classifier_graph_options_pb2
from mediapipe.tasks.cc.vision.gesture_recognizer.proto import gesture_classifier_graph_options_pb2
import json
import os


class StudioManager:

    def __init__(self):
        config_dir = os.path.join(
            os.path.dirname(__file__),
            "..",
            "config"
        )
        with open(
        os.path.join(config_dir, "studios.json"),
        "r",
        encoding="utf-8"
        ) as f:
            self.studios = json.load(f)

        

    def get_studios(self):
        config_dir = os.path.join(
            os.path.dirname(__file__),
            "..",
            "config"
        )

        with open(
            os.path.join(config_dir, "studios.json"),
            encoding="utf-8"
        ) as f:
            self.studios = json.load(f)

        return self.studios

    def get_studio(self, studio_id):

        for studio in self.studios:

            if studio["id"] == studio_id:
                return studio

        return None
    
    def add_studio(self, name, description, icon):
        studio = {
            "id": name.lower().replace(" ", "_"),
            "name": name,
            "description": description,
            "icon": icon,
            "flow": name.lower().replace(" ", "_") + "_flow",
            "last_used": "Never"
        }
        print(studio)

    def add_studio(self, name, description, icon):

        studio_id = name.lower().replace(" ", "_")
        for studio in self.studios:
            if studio["id"] == studio_id:
                print("❌ Studio already exists.")
                return

        studio = {
            "id": studio_id,
            "name": name,
            "description": description,
            "icon": icon,
            "flow": studio_id + "_flow",
            "last_used": "Never"
        }

        self.studios.append(studio)

        config_dir = os.path.join(
            os.path.dirname(__file__),
            "..",
            "config"
        )

        self.save_studios()

        print("✅ Studio added!")

        with open(
            os.path.join(config_dir, "studios.json"),
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(
                self.studios,
                f,
                indent=4,
                ensure_ascii=False
            )

    def delete_studio(self, studio_id):
        self.studios = [
            studio
            for studio in self.studios
            if studio["id"] != studio_id
        ]

        config_dir = os.path.join(
            os.path.dirname(__file__),
            "..",
            "config"
        )

        self.save_studios()

        print("✅ Studio deleted!")
    
    def update_studio(self, studio_id, name, description, icon):
        for studio in self.studios:
            if studio["id"] == studio_id:
                studio["name"] = name
                studio["description"] = description
                studio["icon"] = icon
                break
        self.save_studios()

    def save_studios(self):
        config_dir = os.path.join(
            os.path.dirname(__file__),
            "..",
            "config"
        )
        with open(
            os.path.join(config_dir, "studios.json"),
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(
                self.studios,
                f,
                indent=4,
                ensure_ascii=False
            )


if __name__ == "__main__":
    manager = StudioManager()
    manager.add_studio(
        "Video Editing",
        "Everything ready for editing",
        "🎬"
    )
    manager.delete_studio("video_editing")
