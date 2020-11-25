export PYTHONPATH=$PYTHONPATH:leaderboard
export PYTHONPATH=$PYTHONPATH:leaderboard/team_code
export PYTHONPATH=$PYTHONPATH:scenario_runner

if [ -d "$TEAM_CONFIG" ]; then
    CHECKPOINT_ENDPOINT="$TEAM_CONFIG/experiment_results/$(basename $ROUTES .xml).json"
else
    CHECKPOINT_ENDPOINT="$(dirname $TEAM_CONFIG)/experiment_results/$(basename $ROUTES .xml).json"
fi

python3 leaderboard/test_suite.py \
--track=SENSORS \
--scenarios=leaderboard/data/all_towns_traffic_scenarios_public.json  \
--agent=${TEAM_AGENT} \
--agent-config=${TEAM_CONFIG} \
--checkpoint=${CHECKPOINT_ENDPOINT} \
--port=${PORT}

echo "Done. See $CHECKPOINT_ENDPOINT for detailed results."
