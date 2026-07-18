import time


class WaitAction:

    def execute(self, step, apps):

        duration = step.get("duration", 1)

        print(f"⏳ Waiting {duration} second(s)...")

        time.sleep(duration)