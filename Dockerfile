FROM python:3.7-slim
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY vtes-telegram-bot /usr/local/bot/
CMD python3 /usr/local/bot/bot.py