import os
import sys
import locale

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Default language
LANGUAGE = 'en'

def get_gettext(lang):
    import gettext
    path = os.path.join(PROJECT_ROOT, 'locale')
    try:
        t = gettext.translation(
            'messages',
            path,
            languages=[lang],
            fallback=True,
        )
        t.install()

        if sys.version_info >= (3, 0):
            return lambda message: t.gettext(message)
        else:
            return lambda message: t.ugettext(message)
    except IOError:
        print("Fix this!")
        return lambda x: x

# Function to get OS language
def get_os_language():
    return locale.getdefaultlocale()[0]

try:
    # Get language from OS settings
    lang = os.environ.get("INVOICE_LANG", get_os_language() or LANGUAGE)
    _ = get_gettext(lang)
except OSError:
    print("Fix this!")
    _ = lambda x: x

FONT_PATH = os.path.join(PROJECT_ROOT, "fonts", "DejaVuSans.ttf")
FONT_BOLD_PATH = os.path.join(PROJECT_ROOT, "fonts", "DejaVuSans-Bold.ttf")

if not os.path.isfile(FONT_PATH):
    FONT_PATH = "/usr/share/fonts/TTF/DejaVuSans.ttf"
    FONT_BOLD_PATH = "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf"

if not os.path.isfile(FONT_PATH):
    raise FileNotFoundError("Fonts not found")