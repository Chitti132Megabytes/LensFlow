from mediapipe.framework import status_handler_pb2
import json
import os
import subprocess
import platform
import time
import webbrowser
import pyautogui
from .actions.launch_action import LaunchAction
from .actions.wait_action import WaitAction
from .actions.website_action import WebsiteAction

class FlowManager:

    def __init__(self):
        config_dir = os.path.join(
            os.path.dirname(__file__),
            "..",
            "config"
        )
        self.actions = {
    "launch": LaunchAction(),
    "wait": WaitAction(),
    "website": WebsiteAction()
}

        with open(os.path.join(config_dir, "flows.json")) as f:
            self.flows = json.load(f)

        with open(os.path.join(config_dir, "apps.json")) as f:
            self.apps = json.load(f)

    def execute_flow(self, flow_name):

        flow = self.flows.get(flow_name)

        if not flow:
            print(f"❌ Flow '{flow_name}' not found.")
            return

        print(f"🚀 Executing Flow: {flow_name}")

        for step in flow:
            action_type = step.get("type")
            action = self.actions.get(action_type)
            if action:
                action.execute(step, self.apps)
            else:
                print(f"❌ Unknown action type: {action_type}")

    def launch_app(self, app):

        system = platform.system()

        try:

            if system == "Windows":
                subprocess.Popen(app, shell=True)

            elif system == "Darwin":
                subprocess.Popen(["open", "-a", app])

            elif system == "Linux":
                subprocess.Popen([app])

            print(f"✅ Launched {app}")

        except Exception as e:
            print(f"❌ Could not launch {app}: {e}")
        

    