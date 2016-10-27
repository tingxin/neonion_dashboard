__author__ = 'tingxxu'

import random
from commonstring import *
import time
from manager import manager
import json


class Application:
    def __init__(self):
        self.__speed = 0
        self.__speed_update_time = 0
        self.__acceleration = 0
        self.__fuel = 100
        self.__throttle = 57
        self.__distance = 0
        self.__engine_rpm = 0
        self.__longitude = {value_str: 0, stay_minutes_str: 0, stay_seconds_str: 0}
        self.__latitude = {value_str: 0, stay_minutes_str: 0, stay_seconds_str: 0}


        self.__diagnostic = self.get_diagnotic_data()

        self.__actions = {}
        self.__init_actions()

        self.__receivers = {}
        self.__init_receivers()

        self.speedToAccelerationRatio = 0.28

    def __init_receivers(self):
        self.__receivers[12] = self.receive_engine_rpm
        self.__receivers[13] = self.receive_speed
        self.__receivers[17] = self.receive_throttle
        self.__receivers[47] = self.receive_fuel
        self.__longitude[161] = self.receive_longitude
        self.__longitude[162] = self.receive_latitude

    def __init_actions(self):
        self.__actions[speed_str] = self.get_speed
        self.__actions[engine_str] = self.get_engine_rpm
        self.__actions[fuel_str] = self.get_fuel
        self.__actions[throttle_str] = self.get_throttle
        self.__actions[distance_str] = self.get_distance
        self.__actions[stop_str] = self.get_stops
        self.__actions[acceleration_str] = self.get_acceleration

    def receive(self, data):
        json_data = json.loads(data)
        if json_data["status"] == "ok":
            responses = json_data["responses"]
            keys = self.__receivers.keys()
            # from 1970-01-01 00:00:00
            time_seconds = time.time()
            for pid_item in responses:
                pid = pid_item["pid"]
                if pid in keys:
                    self.__receivers[pid](time_seconds, pid_item["data"])

    def get_data(self, key):
        if key is not None:
            if key in self.__actions:
                return self.__actions[key]()
            else:
                return None

    def get_data_in_keys(self, keys):
        result = {}
        for key in keys:
            if key in self.__actions:
                result[key] = self.__actions[key]()
        return result

    def get_diagnostics(self):
        return self.__diagnostic

    def get_diagnotic_data(self):
        result = []

        engine_status = {}
        engine_status["title"] = "David"
        engine_status["level"] = random.randint(3, 5)

        fuel_system_status = {}
        fuel_system_status["title"] = "Nermeen"
        fuel_system_status["level"] = random.randint(3, 5)

        brake_status = {}
        brake_status["title"] = "Jack"
        brake_status["level"] = random.randint(3, 5)

        tire_status = {}
        tire_status["title"] = "Edwin"
        tire_status["level"] = random.randint(3, 5)

        result.append(engine_status)
        result.append(fuel_system_status)
        result.append(brake_status)
        result.append(tire_status)
        return result

    def get_all(self):
        result = {}
        for key in self.__actions:
            result[key] = self.__actions[key]()

        return result

    def get_speed(self):
        return self.__speed

    def get_acceleration(self):
        return self.__acceleration

    def get_engine_rpm(self):
        return self.__engine_rpm

    def get_fuel(self):
        return self.__fuel

    def get_throttle(self):
        return self.__throttle

    def get_distance(self):
        return self.__distance

    def get_position(self):
        pass

    def get_coordinates(self):
        pass

    def get_stops(self):
        stops = []

        stop1 ={}
        stop1["time"] = "2:30 PM"
        stop1["stayTime"] = "5 minutes"
        stop1["x"] = 100
        stop1["y"] = 18

        stops.append(stop1)

        stop2 ={}
        stop2["time"] = "2:50 PM"
        stop2["stayTime"] = "6 minutes"
        stop2["x"] = 105
        stop2["y"] = 300

        stops.append(stop2)

        stop3 ={}
        stop3["time"] = "3:10 PM"
        stop3["stayTime"] = "1 minutes"
        stop3["x"] = 150
        stop3["y"] = 490

        stops.append(stop3)

        stop4 ={}
        stop4["time"] = "3:30 PM"
        stop4["stayTime"] = "2 minutes"
        stop4["x"] = 200
        stop4["y"] = 12

        stops.append(stop4)

        result ={}
        result[value_str] = stops
        return result



        return

    def get_history(self, keys, seconds):
        result = manager.get_history(keys, seconds)
        return result

    def get_speed_history(self, before_seconds):
        pass

    def get_engine_rpm_history(self):
        pass

    def get_fuel_history(self):
        pass

    def get_throttle_history(self):
        pass

    def get_position_history(self):
        pass

    def get_distance_history(self):
        pass

    def get_coordinates_history(self):
        pass

    # https://en.wikipedia.org/wiki/OBD-II_PIDs
    def receive_engine_rpm(self, time_seconds, data):
        param_a = data[0]
        param_b = data[1]
        rpm = (param_a*256 + param_b)/4
        self.__engine_rpm = rpm
        manager.save_engine_rpm(time_seconds, rpm)

    def receive_speed(self, time_seconds, data):
        param_a = data[0]
        speed = param_a

        manager.save_speed(time_seconds, speed)

        self.__acceleration = (speed - self.__speed)/(time_seconds - self.__speed_update_time)
        manager.save_acceleration(time_seconds, self.__acceleration)

        self.__speed = speed
        self.__speed_update_time = time_seconds

    def receive_throttle(self, time_seconds, data):
        param_a = data[0]
        throttle = param_a * 100 / 255
        self.__throttle = throttle
        manager.save_throttle(time_seconds, throttle)

    def receive_fuel(self, time_seconds, data):
        param_a = data[0]
        fuel = param_a * 100 / 255
        self.__fuel = fuel
        manager.save_fuel(time_seconds, fuel)

    def receive_longitude(self, time_seconds, data):

        degrees = data[0]
        minutes = data[1]
        seconds = data[2]
        self.__longitude = {value_str: degrees, stay_minutes_str: minutes, stay_seconds_str: seconds}
        manager.save_longitude(time_seconds, degrees, minutes, seconds)

    def receive_latitude(self, time_seconds, data):
        degrees = data[0]
        minutes = data[1]
        seconds = data[2]
        self.__longitude = {value_str: degrees, stay_minutes_str: minutes, stay_seconds_str: seconds}
        manager.save_latitude(time_seconds, degrees, minutes, seconds)




