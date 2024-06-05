FROM python:3.13.0b1-alpine3.20

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py /app/

EXPOSE 5000

CMD ["python", "app.py"]