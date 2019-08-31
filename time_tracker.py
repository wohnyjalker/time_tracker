import subprocess
import time
import datetime

WEB_BROWSER = 'Mozilla Firefox'
TERMINAL = 'zawrat@zawrat'
PY_CHARM = 'PyCharm'


class Activity:
    """Activity class"""
    def __init__(self, window_title):
        #self.window_title = window_title
        self.window_title = self.normalize_title(window_title)
        self.start_time = self.get_time()
        self.end_time = None
        self.diff = None

    def __str__(self):
        return f"{self.window_title}\ntime start: {self.start_time}\ntime end:   {self.end_time}" \
               f"\ntime delta: {str(self.delta_time())[:-3]}"

    @staticmethod
    def get_time():
        return datetime.datetime.now()

    def normalize_title(self, window_title):
        if WEB_BROWSER in window_title:
            return self.get_webbrowser_url(window_title)
        elif TERMINAL in window_title:
            return 'Terminal'
        elif PY_CHARM in window_title:
            return PY_CHARM
        else:
            return window_title

    def get_webbrowser_url(self, window_title):
        if 'GitHub' in window_title:
            return 'GitHub'
        elif 'Google' in window_title:
            return 'Google'
        elif 'YouTube' in window_title:
            return 'YouTube'
        else:
            return WEB_BROWSER

    def end_timer(self):
        self.end_time = self.get_time()

    def delta_time(self):
        return self.end_time - self.start_time
        #self.diff = divmod(self.diff.days*86400 + self.diff.seconds, 60)


def find_activity():
    p = subprocess.Popen(["xdotool", "getactivewindow", "getwindowname"], stdout=subprocess.PIPE)
    window_name = p.communicate()
    return window_name[0].decode('utf-8').rstrip()


activities = []
last_activity = Activity(find_activity())  # ostatnia aktywnosc bez endtime
print(f"[!]First activity: {last_activity.window_title}")


try:
    while True:

        new_activity = Activity(find_activity())

        if new_activity.window_title != last_activity.window_title:
            print(f"[!]New activity found: {new_activity.window_title}")
            last_activity.end_timer()
            activities.append(last_activity)
            print(f"[+]Previous activity added.")
            last_activity = new_activity

        time.sleep(2)


except KeyboardInterrupt:
    print(f"\n{__file__} finish.")
    for activity in activities:
        activity.delta_time()
        print(activity)



# ANSI colors
c = (
    "\033[0m",   # End of color
    "\033[36m",  # Cyan
    "\033[91m",  # Red
    "\033[35m",  # Magenta
)


