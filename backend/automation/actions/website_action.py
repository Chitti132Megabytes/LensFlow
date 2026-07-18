import webbrowser


class WebsiteAction:

    def execute(self, step, apps):

        url = step.get("url")

        print(f"🌐 Opening {url}")

        webbrowser.open(url)