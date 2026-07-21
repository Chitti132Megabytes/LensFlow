from ui.themes.midnight import MidnightTheme
from ui.themes.light import LightTheme

THEMES = {
    MidnightTheme.NAME: MidnightTheme,
    LightTheme.NAME: LightTheme,
}

current_theme = MidnightTheme


def set_theme(name):
    global current_theme

    if name in THEMES:
        current_theme = THEMES[name]
        print(f"🎨 Theme changed to {name}")


def get_theme():
    return current_theme


def get_theme_names():
    return list(THEMES.keys())

if __name__ == "__main__":
    print(get_theme().BG_CARD)

    set_theme("light")

    print(get_theme().BG_CARD)