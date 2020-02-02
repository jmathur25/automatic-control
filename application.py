from flask import Flask, render_template, request
application = Flask(__name__)

LEFT_POWER = 0
RIGHT_POWER = 0

@application.route('/', methods=['GET'])
def home():
    return render_template('controller.html')

@application.route('/control', methods=['POST'])
def recieve_control():
    global LEFT_POWER, RIGHT_POWER
    result = request.form
    if 'right' in result:
        RIGHT_POWER = int(result['right'])
    else:
        LEFT_POWER = int(result['left'])

    # post to arduino

    return 'ok'

@application.route('/env', methods=['POST'])
def recieve_observations():
    pass

if __name__ == "__main__":
    application.run(host="0.0.0.0")
