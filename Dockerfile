FROM hitokizzy/geezram:slim-buster

RUN git clone -b main https://github.com/vckyou/Geez-Pyro /home/geez/
WORKDIR /home/geez

RUN wget https://raw.githubusercontent.com/vckyou/Geez-Pyro/main/requirements.txt \
    && pip3 install --no-cache-dir -U -r requirements.txt \
    && rm requirements.txt
    
CMD bash start
