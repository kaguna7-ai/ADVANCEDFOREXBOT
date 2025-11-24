FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip && pip install -r requirements.txt
ENV PYTHONUNBUFFERED=1
CMD ["python", "bot.py"]
