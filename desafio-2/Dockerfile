FROM python:3.14-slim

WORKDIR /desafio-2

RUN apt-get update && apt-get install -y

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install chromium
RUN playwright install-deps

COPY main.py . 

CMD ["python", "main.py"]