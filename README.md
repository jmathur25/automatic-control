# automatic-control
This repository contains our work on creating automatic safety software for autonomous vehicles at MakeHarvard 2020. Big thanks to https://github.com/abhinavsagar/Reinforcement-Learning-Tutorial for a great implementation of continuous space Deep-Q learning. We use this to train our RL model. To get started, run:

```
conda install pytorch -c pytorch
pip install -r requirements.txt
```

The navigate to `rc_car_env` and run:
```
pip install -e .
```

This makes our custon environment and physics engine. The source code for that is in `rc_car_env/rc_car_env/envs/`.

To train the RL model, go to `Reinforcement-Learning-Tutorial/ddpg walker/DDPG.ipynb` and run that notebook. Move the resulting .pth files into the `model` directory.

To see how the model performs, run `python simulation.py simple 100 1`. This shows (in a very toy case) how the model safety checks the usual moving algorithm and cuts it off before it runs into the obstacle. `simple` represents a toy case, and `regular` is the usual paramater. The other two arguments are steps and episodes respectively. A new episode lays out a new random environment.

Lastly, to interact with the RC car, connect to the car's wifi and run `python application.py`. Navigate to `127.0.0.1:5000` and use the (rather crummy) interface to drive the car. The model should kick in and prevent you from ramming into a wall or other kind of obstacle.
