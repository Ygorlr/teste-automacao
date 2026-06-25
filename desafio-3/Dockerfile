FROM python:3.14-slim

WORKDIR /desafio-3

RUN apt-get update && apt-get install -y

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install chromium
RUN playwright install-deps

RUN mkdir -p ["/saida"]

COPY main.py . 
COPY data.json .
COPY image.png .

VOLUME ["/saida"]

CMD ["sh", "-c", "python main.py && mv confirmation.png /saida/confirmation.png"]