import json
import os


class StudioManager:

    def __init__(self):
        config_dir = os.path.join(
            os.path.dirname(__file__),
            "..",
            "config"
        )
        with open(os.path.join(config_dir, "studios.json")) as f:
            self.studios = json.load(f)

    def get_studios(self):
        return self.studios

    def get_studio(self, studio_id):

        for studio in self.studios:

            if studio["id"] == studio_id:
                return studio

        return None

if __name__ == "__main__":
    manager = StudioManager()
    print(manager.get_studio("coding"))
