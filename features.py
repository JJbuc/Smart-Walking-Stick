#!/usr/bin/env python3


from newsapi import NewsApiClient
from datetime import datetime
from bs4 import BeautifulSoup
from gtts import gTTS
import playsound
import time as tm
import requests
import pyaudio
import wave
from send_message import email_alert, send_otp


def stt(fileName):

    """
    Purpose :To provide text input data to other functions.
    Converts input audio to text.

    Sample output :-

    {'id': 'oxbhct39j3-5520-41d2-856f-3535fa4f8b05',
     'language_model': 'assemblyai_default',
     'acoustic_model': 'assemblyai_default',
     'language_code': 'en_us',
     'status': 'completed',
     'audio_url': 'https://cdn.assemblyai.com/upload/357dcad3-3c97-49a6-9df3-b17e71f85d8b',
     'text': 'Hello.',
     'words': [{'text': 'Hello.',
       'start': 670,
       'end': 720,
       'confidence': 0.67,
       'speaker': None}],
     'utterances': None,
     'confidence': 0.67,
     'audio_duration': 1,
     'punctuate': True,
     'format_text': True,
     'dual_channel': None,
     'webhook_url': None,
     'webhook_status_code': None,
     'speed_boost': False,
     'auto_highlights_result': None,
     'auto_highlights': False,
     'audio_start_from': None,
     'audio_end_at': None,
     'word_boost': [],
     'boost_param': None,
     'filter_profanity': False,
     'redact_pii': False,
     'redact_pii_audio': False,
     'redact_pii_audio_quality': None,
     'redact_pii_policies': None,
     'redact_pii_sub': None,
     'speaker_labels': False,
     'content_safety': False,
     'iab_categories': False,
     'content_safety_labels': {'status': 'unavailable',
      'results': [],
      'summary': {}},
     'iab_categories_result': {'status': 'unavailable',
      'results': [],
      'summary': {}},
     'language_detection': False,
     'custom_spelling': None,
     'disfluencies': False,
     'sentiment_analysis': False,
     'auto_chapters': False,
     'chapters': None,
     'sentiment_analysis_results': None,
     'entity_detection': False,
     'entities': None}
    """

    # file upload
    filename = fileName

    def read_file(filename, chunk_size=5242880):
        with open(filename, "rb") as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data

    data = read_file(filename)
    headers = {"authorization": "6e78c1adb2c94b2db4fd312579584538"}
    response = requests.post(
        "https://api.assemblyai.com/v2/upload", headers=headers, data=data
    )
    fileURL = response.json()["upload_url"]

    # requesting transcription
    endpoint = "https://api.assemblyai.com/v2/transcript"
    json = {"audio_url": fileURL}
    headers = {
        "authorization": "6e78c1adb2c94b2db4fd312579584538",
        "content-type": "application/json",
        "language_code": "en_in",
    }
    response = requests.post(endpoint, json=json, headers=headers)
    id = response.json()["id"]

    # waiting for completion of transcription
    endpoint = "https://api.assemblyai.com/v2/transcript/" + id
    headers = {
        "authorization": "6e78c1adb2c94b2db4fd312579584538",
    }

    while True:
        tm.sleep(3)
        response = requests.get(endpoint, headers=headers)
        resp = response.json()
        status = resp["status"]
        if status == "completed" or status == "error":
            return resp["text"]
            break


def get_audio():

    """
    Purpose : To provide input microphone data, to perform other functions based on users requirements.
    Takes audio input from microphone and returns wav data.
    """
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "output.wav"

    p = pyaudio.PyAudio()

    stream = p.open(
        format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
    )

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(frames))
    wf.close()
    return WAVE_OUTPUT_FILENAME


def speak(test):

    """
    Purpose : To make announcements.
    It performs text to speech, save the text in the filename voice.mp3,
    it will always be overwritten to handle limited space capacity.
    """

    tts = gTTS(text=test, lang="en")
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)


def get_news(category="business"):

    """
    Use NewsAPI
    Purpose : To get top headlines and their descriptions for India
    In order to limit the annnouncement time we limit the initial announcement to 2 news
    then based on user's interest we further announce the remaining news
    """
    newsapi = NewsApiClient(api_key="378c61276f8247039dc5206d64ef50b8")

    top_headlines_category_based = newsapi.get_top_headlines(
        category=category, language="en", country="in"
    )

    for i in range(len(top_headlines_category_based["articles"])):
        if i < 1:
            title = top_headlines_category_based["articles"][i]["title"]
            description = top_headlines_category_based["articles"][i]["description"]
            source = title.split("-")[-1].strip()
            announce = (
                "News "
                + str(i + 1)
                + "by "
                + source
                + " "
                + title.replace(source, "")
                + " "
                + description
            )
            speak(announce)
        else:
            speak("Would you like to hear more")
            answer = stt(get_audio())
            print(answer)
            if "yes" in answer.lower():
                announce = (
                    "News "
                    + str(i + 1)
                    + " "
                    + top_headlines_category_based["articles"][i]["title"]
                    + " "
                    + top_headlines_category_based["articles"][i]["description"]
                )
                speak(announce)
            elif "no" in answer.lower():
                speak("Okay")
                break
            else:
                speak("Sorry some error occurred")


def get_weather(lat="19.107344", long="72.836977"):

    """
    Purpose : It announces the today's main weather, temperature and hummidity.

    obj =   { 'lat': 19.1073,
              'lon': 72.837,
              'time':{
                      'timestamp': 1651060397,
                      'sunrise': 1651020187,
                      'sunset': 1651066158
                      },
              'measures':{
                          'temperature': 33.95,
                          'temperatureFeelLike': 37.01,
                          'pressure': 1003,
                          'humidity': 46,
                          'dew': 20.7,
                          'visibility': 5000
                          },
              'weather': [{'main': 'Smoke', 'description': 'smoke'}]}
    """

    units = "metric"
    exclude = "minutely,hourly,daily"
    apiID = "f4a62f4ae6b9aff4dfc5b35dd71339ea"
    baseURL = "https://api.openweathermap.org/data/2.5/onecall"

    URL = "{baseURL}?lat={lat}&lon={long}&exclude={exclude}&units={units}&appid={apiID}".format(
        baseURL=baseURL, lat=lat, long=long, units=units, exclude=exclude, apiID=apiID
    )
    r = requests.get(url=URL).json()

    obj = {}
    obj["lat"] = r["lat"]
    obj["lon"] = r["lon"]

    time = {}
    current = r["current"]
    time["timestamp"] = current["dt"]
    time["sunrise"] = current["sunrise"]
    time["sunset"] = current["sunset"]
    obj["time"] = time

    measures = {}
    measures["temperature"] = current["temp"]
    measures["temperatureFeelLike"] = current["feels_like"]
    measures["pressure"] = current["pressure"]
    measures["humidity"] = current["humidity"]
    measures["dew"] = current["dew_point"]
    measures["visibility"] = current["visibility"]

    obj["measures"] = measures

    weather = []
    tempWeather = current["weather"]
    for i in tempWeather:
        temp = {}
        temp["main"] = i["main"]
        temp["description"] = i["description"]
        weather.append(temp)
    obj["weather"] = weather

    if "rain" in current.keys():
        obj["rain"] = current["rain"]

    if "alerts" in r.keys():
        alerts = []
        tempAlerts = r["alerts"]

        for i in tempAlerts:
            temp = {}
            temp["event"] = i["event"]
            temp["description"] = i["description"]
            alerts.append(temp)

        obj["alerts"] = alerts

    announce = (
        "The main weather is "
        + str(obj["weather"][0]["main"])
        + ".The temperature is "
        + str(obj["measures"]["temperatureFeelLike"])
        + " and humidity is "
        + str(obj["measures"]["humidity"])
    )
    speak(announce)
    return obj


def get_current_location(lat="19.107455901601767", long="72.8372078264864"):

    """
    It returns the current location of the person and also announces it.
    """

    apiID = "AIzaSyCMuvKJWOfR-3_En2FBErmldSdX8JiUfdw"
    URL = "https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{long}&key={api}".format(
        lat=lat, long=long, api=apiID
    )
    r = requests.get(url=URL).json()
    t = r["results"][1]["formatted_address"]
    speak(t)
    return t


def get_destination_support(
    origin="19.107344,72.836977", destination="Andheri Station", need="navigation"
):

    """
    It announces the distance of the end destination from origin and
    how long it will take to reach there using a particular mode of transport.

    It also announces the initial directions to reach the destination, which can be mmade dynamic using
    continuous GPS input.
    """

    apiID = "AIzaSyDygYmz0Z3rcyBi9a4bvrorB-UPRaYZjcU"
    URL = (
        "https://maps.googleapis.com/maps/api/directions/json"
        "?origin={origin}&destination={destination}&key={api}"
    ).format(origin=origin, destination=destination, api=apiID)

    r = requests.get(url=URL).json()
    print(r)
    distance = r["routes"][0]["legs"][0]["distance"]["text"]
    time = r["routes"][0]["legs"][0]["duration"]["text"]
    time = "".join(time.split(" "))
    end_dest = r["routes"][0]["legs"][0]["end_address"]
    end_dest_announce = "".join(end_dest.split(",")[0:3])
    mode = r["routes"][0]["legs"][0]["steps"][0]["travel_mode"]

    route_1 = BeautifulSoup(
        r["routes"][0]["legs"][0]["steps"][0]["html_instructions"]
    ).get_text()

    route_1_dist = r["routes"][0]["legs"][0]["steps"][0]["distance"]["text"]
    route_2 = BeautifulSoup(
        r["routes"][0]["legs"][0]["steps"][1]["html_instructions"]
    ).get_text()

    announce = (
        "Your destination that is "
        + end_dest_announce
        + " is "
        + distance
        + " away and will take you"
        + time
        + " to reach there via mode of "
        + mode
    )
    announce_route = route_1 + " for " + route_1_dist + " then " + route_2
    speak(announce)
    if need == "navigation":
        speak(announce_route)


def get_nearby_places(lat="19.107344", long="72.836977", types="restaurants"):

    """
    Sample Output

        [{'address': 'opp. Prime Mall, Shop No 6, Ahmed Mension, opp. Prime Mall, Irla '
                 'Road, Vile Parle West, Mumbai',
        'name': 'Ovenstory Vile Parle',
        'rating': 3},
        {'address': 'opp. Diamond Chemist, Shop no 1,MCGM parking lane, opp. Diamond '
                 'Chemist, Irla Road, Vile Parle West, Mumbai',
        'name': 'Priya Fast Food',
        'rating': 4.3},
        {'address': '4R5P+25P, Suvarna Nagar, Juhu, Mumbai',
        'name': 'ISKCON Canteen',
        'rating': 4.1},
        {'address': 'Shop no. 1, New Hazrabai House, near Cooper hospital, 2, Irla '
                 'Road, Vile Parle West, Mumbai',
        'name': 'Pappilon Fast Food Corner Irla',
        'rating': 3.9},
        {'address': 'Besides Papillon, Shop no 4/5 Harzabai House, Irla Road, Vile '
                 'Parle West, Mumbai',
        'name': 'Udupi 2 Mumbai',
        'rating': 4.1},
        {'address': 'behind ICICI Direct Bank, 13, Shri Dwarkesh Niketan Building, '
                 'Plot No 13, 3rd Floor, behind ICICI Direct Bank, North South '
                 'Road Number 1, Azadanagar Society, JVPD Scheme, Vile Parle West, '
                 'Mumbai',
        'name': 'Juice Lounge Main Office',
        'rating': 4},
        {'address': 'No.3, Gulmohar Road, Beside Cooper Hospital, JVPD Scheme, Vile '
                 'Parle West, Mumbai',
        'name': 'Amar Juice Centre',
        'rating': 4.2},
        {'address': 'Shop No-24, Arif Mansion, Irla Lane, Navpada, Irla, Vile Parle '
                 'West, Mumbai',
        'name': 'Sai Sagar Fast Food',
        'rating': 4.2},
        {'address': 'Juhu JVPD NS Road no 1, Ram Gadkari Marg, Mumbai',
        'name': 'Bombay Spices - The Flavours of India',
        'rating': 5},
        {'address': '4R5Q+W65, Tata Colony, Vile Parle West, Mumbai',
        'name': 'The happy chef',
        'rating': 4.2},
        {'address': 'De Menthe Eatery, opp. Irla Nursing Home, SV Road, Mumbai',
        'name': 'De Menthe Eatery',
        'rating': 5},
        {'address': 'opposite Prime Mall, Arif Mansion, opposite Prime Mall, Market, '
                 'Irla, Vile Parle West, Mumbai',
        'name': 'Asiad',
        'rating': 4},
        {'address': 'Shanti Niketan, Shop Number 1 Opposite Sameer Ceramics, Vile '
                 'Parle West, Mumbai',
        'name': 'The Belgian Waffle Co.',
        'rating': 4.3},
        {'address': 'Shop No 4A, Apurva Vaibhav CHS, SV Road, Irla, Vile Parle West, '
                 'Mumbai',
        'name': 'Nothing But Chicken , NBC Irla',
        'rating': 4.6},
        {'address': 'near Sony Mony Showroom, SV Road, Indira Nagar, Vile Parle West, '
                 'Mumbai',
        'name': 'Anil Sandwich',
        'rating': 4.4}]
    """

    apiID = "AIzaSyAFyUTH4oaSlpjXcKHXEBqdJu1psvoKjcE"
    URL = (
        "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
        "location={lat},{long}&sensor=true&rankby=distance&key={apiID}&types={types}&opennow=true"
    ).format(lat=lat, long=long, apiID=apiID, types=types)

    r = requests.get(url=URL).json()
    results = r["results"]
    resp = []
    for i in results:
        if "name" in i.keys() and "vicinity" in i.keys() and "rating" in i.keys():
            temp = {}
            temp["name"] = i["name"]
            temp["address"] = i["vicinity"]
            temp["rating"] = i["rating"]
            resp.append(temp)
    announce = (
        "The nearby places are "
        + resp[0]["name"]
        + " "
        + resp[1]["name"]
        + " "
        + resp[2]["name"]
    )
    speak(announce)


def current_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    speak("Current Time =" + str(current_time))
    return current_time


# rules for function calls


def on_click_true():

    rules = {
        "navigation": [
            "navigate to",
            "direction to",
            "directions to",
            "take me to",
            "navigate",
            "navigation",
        ],
        "navigation_time": ["how much time to reach"],
        "weather": ["weather"],
        "current_time": ["what time is it", "current time"],
        "current_location": ["where am", "current location"],
        "news": ["news"],
        "nearby": ["nearby"],
        "emergency": ["emergency", "help"],
    }

    announce = "Hello, how can i help you ?"
    speak(announce)
    response = stt(get_audio()).lower()
    print(response)
    task = ""
    a = list(rules.values())
    for i in range(len(a)):
        for j in range(len(a[i])):
            if a[i][j] in response.lower():
                print("match")
                task = list(rules.keys())[i]
                print(task)

                if task == "navigation_time":
                    dest = response
                    for term in rules["navigation_time"]:
                        dest = dest.replace(term, "")

                    for x in dest.split(" "):
                        if x in ["under", "undheri", "underi"]:
                            dest = "Andheri Station"
                            break

                    dest = "Andheri Station"
                    return get_destination_support(
                        origin="19.107344,72.836977",
                        destination=dest.strip().replace(",", ""),
                        need="time",
                    )

                elif task == "navigation":
                    dest = response
                    for term in rules["navigation"]:
                        dest = dest.replace(term, "")

                    for x in dest.split(" "):
                        if x in ["under", "undheri", "underi"]:
                            dest = "Andheri Station"
                            break

                    dest = "Andheri Station"
                    return get_destination_support(
                        origin="19.107344,72.836977",
                        destination=dest.strip().replace(",", ""),
                        need="navigation",
                    )

                elif task == "weather":
                    return get_weather()
                    # get_weather(lat = "19.107344",long = "72.836977")

                elif task == "current_location":
                    return get_current_location()
                    # get_current_location(lat='19.107455901601767',long='72.8372078264864')

                elif task == "news":
                    return get_news()
                    # category = 'business'

                elif task == "nearby":
                    return get_nearby_places()
                    # get_nearby_places(lat="19.107344",long="72.836977",types="restaurants")

                elif task == "current_time":
                    return current_time()

                elif task == "emergency":
                    email_alert(
                        "Emergency - Walking Stick",
                        "The user has fired up the emergency contact protocol ",
                        "jazib980@gmail.com",
                    )
                    send_otp(9137670353)
                    return

    return speak("No task identified. Please re-press the button")
