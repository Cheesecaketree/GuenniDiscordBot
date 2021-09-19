FROM python:3
FROM gorialis/discord.py

RUN mkdir -p /usr/src/bot
WORKDIR /usr/src/bot

ADD ./config.json /usr/src/bot/
ADD ./Files /usr/src/bot/
# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

COPY . .

CMD [ "python3", "discord_bot.py" ]