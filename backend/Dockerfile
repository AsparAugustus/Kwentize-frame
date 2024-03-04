FROM python:3.9.16
RUN apt-get install -y wget 

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

WORKDIR /root/.u2net

RUN wget https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net_human_seg.onnx

WORKDIR /app

CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]
