#! /bin/bash 
export PYTHONPATH=$PYTHONPATH:leaderboard
export PYTHONPATH=$PYTHONPATH:leaderboard/team_code
export PYTHONPATH=$PYTHONPATH:scenario_runner

EXPERIMENT_ROUTES=(
    leaderboard/data/routes_training/route_10.xml
    # leaderboard/data/routes_training/route_11.xml
    # leaderboard/data/routes_training/route_12.xml 
    # leaderboard/data/routes_training/route_13.xml
)

echo "================================"
echo "======== INIT TEST SUIT ========"
echo "================================"

# Here we start the test suit for all the for routes setted on EXPERIMENT_ROUTES
for ROUTE in "${EXPERIMENT_ROUTES[@]}"; do
    
    # Each route runs a basic test case 
    # And has a different checkpoint endpoint
    # CHECKPOINT_ENDPOINT="$(dirname $TEAM_CONFIG)/experiment_results/$(basename $ROUTE .xml).json"

    # python3 leaderboard/test_suite.py \
    # --track=SENSORS \
    # --scenarios=leaderboard/data/all_towns_traffic_scenarios_public.json  \
    # --agent=${TEAM_AGENT} \
    # --agent-config=${TEAM_CONFIG} \
    # --checkpoint=${CHECKPOINT_ENDPOINT} \
    # --port=${PORT} \
    # --repetitions=2

    # And each route has his metamorphic relaciton exectuion
    CHECKPOINT_ENDPOINT_COMPLEMENTARY="$(dirname $TEAM_CONFIG)/experiment_results/$(basename $ROUTE .xml)_complementary.json"


    # And for this metamorphic relation, before start the evaluation
    # We need to start the change that we want to apply here.
    
    # In this case we gonna have a environment change with rain

    echo "Starting the Metamorphic relation for route ${ROUTE}"
    
    ./leaderboard/start_metamorphic_relation.sh & disown

    jobs

    echo "Epa"

    # After that we can start the evaluation indeed

    python3 leaderboard/test_suite.py \
    --track=SENSORS \
    --scenarios=leaderboard/data/all_towns_traffic_scenarios_public.json  \
    --agent=${TEAM_AGENT} \
    --agent-config=${TEAM_CONFIG} \
    --checkpoint=${CHECKPOINT_ENDPOINT_COMPLEMENTARY} \
    --port=${PORT} \
    --repetitions=2

done

echo "==============================="
echo "======== END TEST SUIT ========"
echo "==============================="

echo "Done. You can see the results inside of the experiment_results/ folder."
