from flask import Flask, render_template, request
from model_interface import ModelInterface
import numpy as np
import requests
from apscheduler.schedulers.background import BackgroundScheduler

application = Flask(__name__)
MODEL_INTERFACE = ModelInterface()

LEFT_POWER = 0
RIGHT_POWER = 0
TARGET_URL = 'http://192.168.4.1:80/'
FRAME_RATE = 1
OBSERVATIONS = []
THRESHOLD = 20

def scale_real_to_sim_action(action):
    return (action - 90) / 90

def scale_sim_to_real_action(action):
    return (action * 90) + 90

def send_action():
    global OBSERVATIONS, LEFT_POWER, RIGHT_POWER
    # post to arduino
    if len(OBSERVATIONS) > 5:
        state = OBSERVATIONS[-1]
        action = np.array([LEFT_POWER, RIGHT_POWER])
        action = scale_real_to_sim_action(action)
        estimated_q = MODEL_INTERFACE.get_action_q(state, action)

        if estimated_q < THRESHOLD:
            # hold motor still
            LEFT_POWER = 90
            RIGHT_POWER = 90
            
            # action = MODEL_INTERFACE.get_action(state)
            # action = scale_sim_to_real_action(action)
            # LEFT_POWER = action[0]
            # RIGHT_POWER = action[1]

    string = f"left={LEFT_POWER};right={RIGHT_POWER}"
    response = requests.post(TARGET_URL, data=string)

    try:
        obs = response.split(',')
        obs = [float(o) for o in obs]
        OBSERVATIONS.append(obs)
    except:
        pass


scheduler = BackgroundScheduler()
scheduler.add_job(func=send_action, trigger='interval', seconds=FRAME_RATE)
scheduler.start()

@application.route('/', methods=['GET'])
def home():
    return render_template('controller.html')

@application.route('/control', methods=['POST'])
def recieve_control():
    global LEFT_POWER, RIGHT_POWER
    result = request.form
    RIGHT_POWER = int(result['right'])
    LEFT_POWER = int(result['left'])
    print(LEFT_POWER, RIGHT_POWER)

    return 'ok'

if __name__ == "__main__":
    application.run(host="0.0.0.0")
