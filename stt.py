from flask import Flask
import ffmpy
from wit import Wit
import os
import requests
from urllib.request import urlopen
from flask import request


app = Flask(__name__)


@app.route('/myfunc',methods=['GET', 'POST'])
def myfunc():
    arg1= request.args.get('url', default = '1', type = str)
    arg2 = request.args.get('id',default = '*', type = str)

    data = urlopen(arg1).read()

    with open('file_in.oga', 'wb') as f:
        f.write(data)

    ## конвертируем
    ff = ffmpy.FFmpeg(
        inputs={'file_in.oga': None},
        outputs={'file_out.wav': None}
    )

    ff.run()

    ## речь в звук
    access_token="WIT-TOKEN"
    client = Wit(access_token)
    resp = None
    with open('file_out.wav', 'rb') as f:
        resp = client.speech(f, None, {'Content-Type': 'audio/wav'})
        
    return url_

if __name__ == '__main__':
    app.run()

