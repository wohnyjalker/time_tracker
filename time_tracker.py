import subprocess
import time
import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

WEB_BROWSER = 'Mozilla Firefox'
TERMINAL = 'zawrat@zawrat'
PY_CHARM = 'PyCharm'


class Activity(object):
    """Activity class"""
    def __init__(self, window_title):
        #self.window_title = window_title
        self.window_title = self.normalize_title(window_title)
        self.start_time = self.get_time()
        self.end_time = None
        self.diff = None
        self.uid = self.get_uid()

    def __str__(self):
        return f"{self.window_title}\ntime start: {self.start_time}\ntime end:   {self.end_time}" \
               f"\ntime delta: {self.diff}"

    def to_dict(self):
        data = {
            u'window': self.window_title,
            u'delta': self.diff,
        }
        return data

    @staticmethod
    def get_time():
        return datetime.datetime.now()#.strftime("%H:%M:%S")

    @staticmethod
    def get_uid():
        return datetime.datetime.now().strftime("%Y-%m-%d")

    def normalize_title(self, window_title):
        if WEB_BROWSER in window_title:
            return self.get_webbrowser_url(window_title)
        elif TERMINAL in window_title:
            return 'Terminal'
        elif PY_CHARM in window_title:
            return PY_CHARM
        elif 'Sublime Text' in window_title:
            return 'Sublime Text'
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

    def calculate_delta(self):
        start_time = self.start_time.timestamp()
        end_time = self.end_time.timestamp()
        self.diff = end_time - start_time
        

#------------------FIRE BASE-------------------------------------

    def activity_to_dict(self): #<-------skonczyc
        dest = {
            u'title': self.window_title,
            u'delta': self.delta, 
        }
        return dest

    def push_data(self):
        activities_ref = db.collection(u'activities').document(self.uid)
        activiti_ref = activities_ref.collection(self.uid).document(self.window_title)
        activiti_ref.set({
            u'window': self.window_title,
            u'delta': self.diff,
            })
        print(f'[FB][!]{self.window_title} - {self.diff} first time added.')

    def update(self):
        activities_ref = db.collection(u'activities').document(self.uid)
        activiti_ref = activities_ref.collection(self.uid).document(self.window_title)
        activiti_ref.update({'delta': firestore.Increment(self.diff)})
        print(f"[FB][+]{self.window_title} - {self.diff} updated.")


def find_activity():
    p = subprocess.Popen(["xdotool", "getactivewindow", "getwindowname"], stdout=subprocess.PIPE)
    window_name = p.communicate()
    return window_name[0].decode('utf-8').rstrip()

def start_firebase():
#    cred = credentials.Certificate('ignore/time-ae333-firebase-adminsdk-7wtrj-2759f7cd9c.json')
#    app = firebase_admin.initialize_app(cred)
#    db = firestore.client()
    try:
        cred = credentials.Certificate('ignore/time-ae333-firebase-adminsdk-7wtrj-2759f7cd9c.json')
        app = firebase_admin.initialize_app(cred)
        db = firestore.client()
        return db
    except:
        print("firebase error")

def get_titles():
    title_list = []
    uid = datetime.datetime.now().strftime("%Y-%m-%d")
    data_ref = db.collection('activities').document(uid)
    data = data_ref.collection(uid).stream()
    for d in data:
        title_list.append(d.id)
    return title_list




db = start_firebase()

activities = get_titles()

print(activities)
last_activity = Activity(find_activity())  # ostatnia aktywnosc bez endtime
print(f"[!]First activity: {last_activity.window_title}")


try:
    while True:

        new_activity = Activity(find_activity())

        if new_activity.window_title != last_activity.window_title:
            print(f"[!]New activity found: {new_activity.window_title}")

            last_activity.end_timer()
            last_activity.calculate_delta()

            if last_activity.window_title in activities:
                last_activity.update()
            elif last_activity.window_title not in activities:
                last_activity.push_data()
            else:
                print("f wyszlo z else")

            activities.append(last_activity.window_title)

            #activities[-1].push_data()
            #last_activity.push_data()

            print(f"[+]Previous activity added.")
            last_activity = new_activity

        time.sleep(2)


except KeyboardInterrupt:
    print(f"\n{__file__} finish.")