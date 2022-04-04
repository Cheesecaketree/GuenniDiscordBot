import logging
import os
import requests
import json
from gtts import gTTS
from datetime import datetime
import random
import string

def load_json(path):
    with open(path, "r") as f:
        data = json.load(f)
        return data

language = load_json("config.json")["language"]
config = load_json("config.json")

def get_time():
	filename = f"uhrzeit_{randStr(N=4)}"
	now = datetime.now()
	generate_voice(f"Es ist gerade {now.strftime('%H')} Uhr {now.strftime('%M')}", filename)
	return filename

def get_status():
    with open(f"Files/status.json", "r") as f:
        status = json.load(f)
    return status

# Time of day (morning, afternoon, evening, night,...)
def get_time_of_day():
	now = datetime.now()
	h = now.hour

	if h < 5:
		return "Nacht"
	elif h < 11:
		return "Morgen"
	elif h < 13:
		return "Mittag"
	elif h < 17:
		return "Nachmittag"
	elif h <= 21:
		return "Abend"
	else:
		return "Nacht"

'''
Generates the texts for different functions relying on speech output.
usecase is determines the file used to get the text templates.
'''
def generate_text(usecase,name=None, target=None, author=None):
	valid_use = {
	"welcome":"Files/welcome.json",
	"insult":"Files/insult.json",
	"love":"Files/love.json",
	"joke":"Files/jokes.json",
	"fact":"Files/facts.json",
	"stream":"Files/stream.json",
	"deaf":"Files/deaf.json"
	}
 
	if usecase in valid_use:
		filename = f"{usecase}{randStr(N=4)}"
		with open(valid_use[usecase]) as f:
			json_obj = json.load(f)
			content = json_obj[language]
   
		message = random.choice(content).format(name=name,target=target,author=author, ToD=get_time_of_day())
		generate_voice(message, filename)
		return filename

	else:
		logging.warning(f"ERROR in generate_text with usecase: {usecase}")
		return

def weather_message(pCity):
	if config["openweathermap-api-key"] == "":
		token = load_json("token.json")["weather-token"]
	else:
		token = config["openweathermap-api-key"]
    
	filename = f"weather_{randStr(N=4)}"
	city = remove_umlaut(pCity.lower())
	url = 'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={token}&units=metric'
	url = url.format(city=city, token=token)
	res = requests.get(url)
	data = res.json()

	try:
		temp = data['main']['temp']
		wetter = data['weather']
		windspeed = data['wind']['speed']
	except:
		return None

	# Temperatur
	tempR = round(temp, 1)
	print("Temperatur: " + str(tempR))
	# Wetterbedingung
	condition = ""
	for item in wetter:
		print(item['main'])
		condition = item['main']

	if condition == "Clear":
		wetterB = "Es ist klar"
	elif condition == "Thunderstorm":
		wetterB = "Es gewittert"
	elif condition == "Drizzle":
		wetterB = "Es nieselt"
	elif condition == "Rain":
		wetterB = "Es regnet"
	elif condition == "Snow":
		wetterB = "Es schneit"
	elif condition == "Clouds":
		wetterB = "Es ist bewölkt"
	else: wetterB = "Es wettert"
	# Windgeschwindigkeit
	windspeed = round(windspeed, 1)

	nachricht = f"""Hier das Wetter in {pCity}: {wetterB} bei {tempR} Grad.
					Die Windgeschwindigkeit beträgt {windspeed} Meter pro Sekunde"""
	generate_voice(nachricht, filename)
	return filename

def generate_voice(pText, name, language = language): 
	nachricht = gTTS(text=pText, lang=language, slow=False)
	filename = name + ".mp3"
	nachricht.save(filename)
	logging.info(f"{name} created")

def delete_file(file):
	os.remove(file)

def randStr(chars = string.ascii_uppercase + string.digits, N=10):
	return ''.join(random.choice(chars) for _ in range(N))

def remove_umlaut(string):
    """
    Removes umlauts from strings and replaces them with the letter+e convention
    :param string: string to remove umlauts from
    :return: unumlauted string
    """
    u = 'ü'.encode()
    U = 'Ü'.encode()
    a = 'ä'.encode()
    A = 'Ä'.encode()
    o = 'ö'.encode()
    O = 'Ö'.encode()
    ss = 'ß'.encode()

    string = string.encode()
    string = string.replace(u, b'ue')
    string = string.replace(U, b'Ue')
    string = string.replace(a, b'ae')
    string = string.replace(A, b'Ae')
    string = string.replace(o, b'oe')
    string = string.replace(O, b'Oe')
    string = string.replace(ss, b'ss')

    string = string.decode('utf-8')
    return string