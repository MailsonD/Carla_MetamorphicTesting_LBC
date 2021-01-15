#!/bin/bash
# export PYTHONPATH=$PYTHONPATH:$CARLA_ROOT/PythonAPI/carla
# export PYTHONPATH=$PYTHONPATH:$CARLA_ROOT/PythonAPI/carla/dist/carla-0.9.10-py3.7-linux-x86_64.egg
export PYTHONPATH=$PYTHONPATH:leaderboard
export PYTHONPATH=$PYTHONPATH:leaderboard/team_code
export PYTHONPATH=$PYTHONPATH:scenario_runner

if [ -d "$TEAM_CONFIG" ]; then
    CHECKPOINT_ENDPOINT="$TEAM_CONFIG/experiment_results/$(basename $ROUTES .xml)_complementary.json"
else
    CHECKPOINT_ENDPOINT="$(dirname $TEAM_CONFIG)/experiment_results/$(basename $ROUTES .xml)_complementary.json"
fi

python3 leaderboard/test_suite.py \
    --track=SENSORS \
    --scenarios=leaderboard/data/all_towns_traffic_scenarios_public.json  \
    --agent=${TEAM_AGENT} \
    --agent-config=${TEAM_CONFIG} \
    --routes=${ROUTES} \
    --checkpoint=${CHECKPOINT_ENDPOINT} \
    --port=${PORT} \
    --repetitions=2

echo "Done. See $CHECKPOINT_ENDPOINT for detailed results."
