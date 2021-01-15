export CARLA_ROOT=/home/mailson/Desenvolvimento/ADS/TCC/Carla/CARLA_0.9.10.1  # change to where you installed CARLA
export PORT=2000                                                              # change to port that CARLA is running on
export ROUTES=leaderboard/data/routes_training/route_14.xml                   # change to desired route
export TEAM_AGENT=image_agent.py                                              # no need to change
export TEAM_CONFIG=epoch=24.ckpt                                              # change path to checkpoint
export HAS_DISPLAY=1                                                          # set to 0 if you don't want a debug window


export PYTHONPATH=$PYTHONPATH:$CARLA_ROOT/PythonAPI/carla
export PYTHONPATH=$PYTHONPATH:$CARLA_ROOT/PythonAPI/carla/dist/carla-0.9.10-py3.7-linux-x86_64.egg

