import argparse
from argparse import RawTextHelpFormatter

from leaderboard.leaderboard_evaluator import start_evaluation


TEST_ROUTES = [
    'leaderboard/data/routes_training/route_10.xml',
    'leaderboard/data/routes_training/route_11.xml',
    'leaderboard/data/routes_training/route_12.xml',
    'leaderboard/data/routes_training/route_13.xml',
]


def main():
    print("opa")
    description = "CARLA AD Leaderboard Evaluation: evaluate your Agent in CARLA scenarios\n"

    # general parameters
    parser = argparse.ArgumentParser(
        description=description, formatter_class=RawTextHelpFormatter)
    parser.add_argument('--host', default='localhost',
                        help='IP of the host server (default: localhost)')
    parser.add_argument('--port', default='2000',
                        help='TCP port to listen to (default: 2000)')
    parser.add_argument('--trafficManagerPort', default='8000',
                        help='Port to use for the TrafficManager (default: 8000)')
    parser.add_argument('--trafficManagerSeed', default='0',
                        help='Seed used by the TrafficManager (default: 0)')
    parser.add_argument('--debug', type=int,
                        help='Run with debug output', default=0)
    parser.add_argument('--record', type=str, default='',
                        help='Use CARLA recording feature to create a recording of the scenario')
    parser.add_argument('--timeout', default="60.0",
                        help='Set the CARLA client timeout value in seconds')

    # simulation setup
    # The routes will be setted for each execution on TEST_ROUTES
    # parser.add_argument('--routes',
    #                     help='Name of the route to be executed. Point to the route_xml_file to be executed.',
    #                     required=True)
    parser.add_argument('--scenarios',
                        help='Name of the scenario annotation file to be mixed with the route.',
                        required=True)
    parser.add_argument('--repetitions',
                        type=int,
                        default=1,
                        help='Number of repetitions per route.')

    # agent-related options
    parser.add_argument("-a", "--agent", type=str,
                        help="Path to Agent's py file to evaluate", required=True)
    parser.add_argument("--agent-config", type=str,
                        help="Path to Agent's configuration file", default="")

    parser.add_argument("--track", type=str, default='SENSORS',
                        help="Participation track: SENSORS, MAP")
    parser.add_argument('--resume', type=bool, default=False,
                        help='Resume execution from last checkpoint?')
    parser.add_argument("--checkpoint", type=str,
                        default='./simulation_results.json',
                        help="Path to checkpoint used for saving statistics and resuming")

    arguments = parser.parse_args()

    print("trying to add a new route")

    arguments.routes = TEST_ROUTES[0]

    print(arguments)
    start_evaluation(arguments)


if __name__ == '__main__':
    main()
