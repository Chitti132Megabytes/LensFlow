import subprocess

class ActionManager:

    def __init__(self):
        self.active = False
        self.last_action = None

    def execute(self, gesture):

        if gesture == self.last_action:
            return

        self.last_action = gesture

        if gesture == "✋ Open Palm":
            self.active = True
            print("✅ LensFlow Activated")

        elif gesture == "✊ Fist":
            self.active = False
            print("🛑 LensFlow Deactivated")

        elif self.active:

            if gesture == "✌️ Peace":
                print("Opening Calculator...")
                subprocess.Popen("calc.exe")