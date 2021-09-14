import logging
import os
import requests
import json
from gtts import gTTS
from datetime import datetime
import random
import string

def get_uhrzeit():
	filename = f"uhrzeit_{randStr(N=4)}"
	now = datetime.now()
	generate_voice(f"Es ist gerade {now.strftime('%H')} Uhr {now.strftime('%M')}", filename)
	return filename

# generiert verschiedene einfache Textnachrichten.
def generate_text(usecase,u=None, t=None, o=None):
	validuse = {
	"welcome":"Files/welcome.json",
	"insult":"Files/insult.json",
	"love":"Files/love.json",
	"joke":"Files/jokes.json",
	"fact":"Files/facts.json",
	"stream":"Files/stream.json",
	"deaf":"Files/deaf.json"
	}
	
	if usecase in validuse:
		filename = f"{usecase}{randStr(N=4)}"
		nachricht = get_random_item(validuse[usecase]).format(name=u,ziel=t,author=o)
		generate_voice(nachricht, filename)
		return filename

	else:
		logging.warning(f"ERROR in generate_text with usecase: {usecase}")
		return

def weather_message(pCity):
	filename = f"wetter_{randStr(N=4)}"
	city = remove_umlaut(pCity.lower())
	url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=ead5112e1fc36110be448eeb3a357bb2&units=metric'
	res = requests.get(url.format(city))
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

def generate_voice(pText, name, language = 'de'): 
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

def get_config(name):
	with open('/home/Guenni_Bot/config.json', "r") as file:
		config = json.load(file)
		data = config[name]
		return data

def get_list(path):
	with open(path) as file:
		json_obj = json.load(file)
		return json_obj['content']

def get_random_item(path):
	content = get_list(path)
	return random.choice(content)

