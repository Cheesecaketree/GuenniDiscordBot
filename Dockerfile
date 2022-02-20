FROM python:3
FROM gorialis/discord.py

RUN mkdir -p /usr/src/bot
WORKDIR /usr/src/bot

# add files to container / to working directory
ADD ./config.json /usr/src/bot/
ADD ./Files /usr/src/bot/

# install python libraries
COPY requirements.txt .
RUN pip install -r requirements.txt

RUN apt install ffmpeg


COPY . .

CMD [ "pytohn3", "test.py" ]
# CMD [ "python3", "discord_bot.py" ]