import subprocess
import platform


class LaunchAction:

    def execute(self, step, apps):

        app_name = step.get("target")
        app_path = apps.get(app_name)

        if not app_path:
            print(f"❌ App '{app_name}' not found.")
            return

        system = platform.system()

        try:
            if system == "Windows":
                subprocess.Popen(app_path, shell=True)

            elif system == "Darwin":
                subprocess.Popen(["open", "-a", app_path])

            elif system == "Linux":
                subprocess.Popen([app_path])

            print(f"✅ Launched {app_name}")

        except Exception as e:
            print(f"❌ Could not launch {app_name}: {e}")