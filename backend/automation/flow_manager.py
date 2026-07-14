from mediapipe.framework import status_handler_pb2
import json
import os
import subprocess
import platform
import time
import webbrowser
import pyautogui

class FlowManager:

    def __init__(self):
        config_dir = os.path.join(
            os.path.dirname(__file__),
            "..",
            "config"
        )

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

            step_type = step.get("type")

            if step_type == "launch":

                app_name = step.get("target")

                app_path = self.apps.get(app_name)

                if app_path:
                    self.launch_app(app_path)
                else:
                    print(f"❌ App '{app_name}' not found.")

            elif step_type == "wait":

                duration = step.get("duration", 1)
                print(f"⏳ Waiting {duration} seconds...")
                time.sleep(duration)

            elif step_type == "website":
                url = step.get("url")
                print(f"🌐 Opening {url}")
                webbrowser.open(url)

            elif step_type == "hotkey":
                keys = step.get("keys")
                print(f"⌨️ Pressing {keys}")
                pyautogui.hotkey(*keys)


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