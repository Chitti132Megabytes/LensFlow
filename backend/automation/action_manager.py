import subprocess
import platform
import time
from automation.flow_manager import FlowManager

class ActionManager:

    def __init__(self):
        self.active = False
        self.last_action = ""
        self.last_action_time = 0
        self.cooldown = 2 
        self.flow_manager = FlowManager()   # seconds

    def execute(self, gesture, action):

        # Activation
        if action == "ACTIVATE":
            if not self.active:
                self.active = True
                print("✅ LensFlow Activated")
            return

        # Deactivation
        if action == "DEACTIVATE":
            if self.active:
                self.active = False
                print("🛑 LensFlow Deactivated")
            return

        # Ignore gestures while inactive
        if not self.active:
            return

        print(f"Executing action: {action}")

        current_time = time.time()

        if (
            action == self.last_action and
            current_time - self.last_action_time < self.cooldown
        ):
            return

        self.last_action = action
        self.last_action_time = current_time
        
        
        # Launch applicationsq
        # Execute Flow
        self.flow_manager.execute_flow(action)

    def launch(self, app):

        system = platform.system()

        try:

            if system == "Windows":
                subprocess.Popen(app, shell=True)

            elif system == "Darwin":
                subprocess.Popen(["open", "-a", app])

            elif system == "Linux":
                subprocess.Popen([app])

        except Exception as e:
            print(f"❌ Could not launch {app}: {e}")