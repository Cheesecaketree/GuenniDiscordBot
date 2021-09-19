FROM python:3
FROM gorialis/discord.py

# set the working directory in the container
WORKDIR /code

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY src/ .




CMD [ "python3", "discord_bot.py" ]