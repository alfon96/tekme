FROM python:3.11.6-alpine3.18

WORKDIR /app

COPY requirements.txt . 

RUN pip install --upgrade pip 
RUN pip install -r requirements.txt

COPY . .

EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]