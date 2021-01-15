#!/usr/bin/env python

import glob
import os
import sys

# try:
#     sys.path.append(glob.glob('../../carla/dist/carla-*%d.%d-%s.egg' % (
#         sys.version_info.major,
#         sys.version_info.minor,
#         'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
# except IndexError:
#     pass


import carla
import argparse
import math


def clamp(value, minimum=0.0, maximum=100.0):
    return max(minimum, min(value, maximum))


class Sun(object):
    def __init__(self, azimuth, altitude):
        self._t = 0.0
        self.azimuth = azimuth
        self.altitude = altitude
        self.clouds = 0.0
        self.rain = 0.0
        self.wetness = 0.0
        self.puddles = 0.0
        self.wind = 0.0
        self.fog = 0.0

    def tick(self, delta_seconds):
        self._t += 0.008 * delta_seconds
        self._t %= 2.0 * math.pi
        self.azimuth += 0.25 * delta_seconds
        self.azimuth %= 360.0
        self.altitude = (70 * math.sin(self._t)) - 20

    def __str__(self):
        return 'Sun(alt: %.2f, azm: %.2f)' % (self.altitude, self.azimuth)


class Storm(object):
    def __init__(self, precipitation):
        self._t = precipitation if precipitation > 0.0 else -25.0
        self._increasing = True
        self.clouds = 0.0
        self.rain = 0.0
        self.wetness = 0.0
        self.puddles = 0.0
        self.wind = 0.0
        self.fog = 0.0
        self.azimuth = 0
        self.altitude = 0

    def tick(self, delta_seconds):
        delta = (1.3 if self._increasing else -1.3) * delta_seconds
        self._t = clamp(delta + self._t, -20.0, 100.0)
        self.clouds = clamp(self._t + 40.0, 0.0, 90.0)
        self.rain = clamp(self._t, 0.0, 80.0)
        delay = -10.0 if self._increasing else 90.0
        self.puddles = clamp(self._t + delay, 0.0, 85.0)
        self.wetness = clamp(self._t * 5, 0.0, 100.0)
        self.wind = 5.0 if self.clouds <= 20 else 90 if self.clouds >= 70 else 40
        self.fog = clamp(self._t - 10, 0.0, 30.0)
        if self._t == -20.0:
            self._increasing = True
        if self._t == 100.0:
            self._increasing = False

    def __str__(self):
        return 'Storm(clouds=%d%%, rain=%d%%, wind=%d%%)' % (self.clouds, self.rain, self.wind)


class Weather(object):
    def __init__(self, weather, weatherConf):
        self.weather = weather
        print("precipitation")
        print(weather.precipitation)
        self._chosedWeather = Sun(
            weather.sun_azimuth_angle, weather.sun_altitude_angle) if weatherConf == 'sun' else Storm(weather.precipitation)

    def tick(self, delta_seconds):
        self._chosedWeather.tick(delta_seconds)
        self.weather.cloudiness = self._chosedWeather.clouds
        self.weather.precipitation = self._chosedWeather.rain
        self.weather.precipitation_deposits = self._chosedWeather.puddles
        self.weather.wind_intensity = self._chosedWeather.wind
        self.weather.fog_density = self._chosedWeather.fog
        self.weather.wetness = self._chosedWeather.wetness
        self.weather.sun_azimuth_angle = self._chosedWeather.azimuth
        self.weather.sun_altitude_angle = self._chosedWeather.altitude

    def __str__(self):
        return '%s' % (self._chosedWeather)


async def init_storm_weather():
    print('opa')

    args = {
        'host': '127.0.0.1',
        'port': 2000,
        'speed': 1.0,
        'weather': 'storm',
    }

    speed_factor = args.speed
    update_freq = 0.1 / speed_factor

    client = carla.Client(args.host, args.port)
    client.set_timeout(2.0)
    world = client.get_world()

    print('ta indo')

    weather = Weather(world.get_weather(), args.weather)

    elapsed_time = 0.0

    while True:
        timestamp = world.wait_for_tick(seconds=30.0).timestamp
        elapsed_time += timestamp.delta_seconds
        if elapsed_time > update_freq:
            weather.tick(speed_factor * elapsed_time)
            world.set_weather(weather.weather)
            sys.stdout.write('\r' + str(weather) + 12 * ' ')
            sys.stdout.flush()
            elapsed_time = 0.0
        else:
            print("acabou aqui")
            print(elapsed_time)
            print(update_freq)


def main():
    argparser = argparse.ArgumentParser(description=__doc__)

    argparser.add_argument(
        '--host',
        metavar='H',
        default='127.0.0.1',
        help='IP of the host server (default: 127.0.0.1)')
    argparser.add_argument(
        '-p', '--port',
        metavar='P',
        default=2000,
        type=int,
        help='TCP port to listen to (default: 2000)')
    argparser.add_argument(
        '-s', '--speed',
        metavar='FACTOR',
        default=1.0,
        type=float,
        help='rate at which the weather changes (default: 1.0)')
    argparser.add_argument(
        '-w', '--weather',
        metavar='W',
        default='sun',
        choices=['sun', 'storm', 'fog', 'rain'],
        help='Param to change the weather'
    )
    args = argparser.parse_args()

    speed_factor = args.speed
    update_freq = 0.1 / speed_factor

    client = carla.Client(args.host, args.port)
    client.set_timeout(2.0)
    world = client.get_world()

    print('ta indo')

    weather = Weather(world.get_weather(), args.weather)

    elapsed_time = 0.0

    while True:
        timestamp = world.wait_for_tick(seconds=30.0).timestamp
        elapsed_time += timestamp.delta_seconds
        if elapsed_time > update_freq:
            weather.tick(speed_factor * elapsed_time)
            world.set_weather(weather.weather)
            sys.stdout.write('\r' + str(weather) + 12 * ' ')
            sys.stdout.flush()
            elapsed_time = 0.0


if __name__ == '__main__':

    main()
