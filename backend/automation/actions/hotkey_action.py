import pyautogui


class HotkeyAction:

    def execute(self, step, apps=None):

        keys = step.get("keys", [])

        if not keys:
            print("❌ No hotkeys provided.")
            return

        print(f"⌨️ Pressing {' + '.join(keys)}")

        pyautogui.hotkey(*keys)