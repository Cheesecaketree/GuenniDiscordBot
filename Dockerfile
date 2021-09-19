FROM python:3
FROM gorialis/discord.py

# set the working directory in the container
WORKDIR /code

# set the working directory in the container
WORKDIR /code

# install dependencies
RUN pip3 install 

# copy the content of the local src directory to the working directory
COPY src/ .

CMD [ "python3", "discord_bot.py" ]