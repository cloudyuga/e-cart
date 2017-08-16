#!flask/bin/python
from app import app

app.config['SECRET_KEY']='secret'
app.run(port=5000, debug=True, host='0.0.0.0', threaded=True)
