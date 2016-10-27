__author__ = 'tingxxu'

from singleton import Singleton
from pymongo import MongoClient
from commonstring import *
import time


class DBManager(Singleton):
    def __init__(self):
        self.client = MongoClient()
        self.car = self.client.car
        self.updateRecord = self.car.updateRecord

        self.__collections = {}

        self.__collections[speed_str] = self.car.speed
        self.__collections[acceleration_str] = self.car.acceleration
        self.__collections[engine_str] = self.car.engine_rpm
        self.__collections[fuel_str] = self.car.fuel
        self.__collections[throttle_str] = self.car.throttle
        self.__collections[distance_str] = self.car.distance
        self.__collections[longitude_str] = self.car.longitude
        self.__collections[latitude_str] = self.car.latitude

    def get_history(self, keys, before_seconds):
        now = time.time()
        time_key = now - before_seconds
        api_keys = self.__collections.keys()
        result = {}
        for key in keys:
            if key in api_keys:
                result[key] = []
                for record in self.__collections[key].find({time_str: {"$gte": time_key}}, {'_id': 0}):
                    result[key].append(record)
        return result

    def save_engine_rpm(self, time_seconds, data):
        engine_rpm = {time_str: time_seconds, value_str: data}
        self.__collections[engine_str].insert_one(engine_rpm)

    def save_speed(self, time_seconds, data):
        speed = {time_str: time_seconds, value_str: data}
        self.__collections[speed_str].insert_one(speed)

    def save_acceleration(self, time_seconds, data):
        acceleration = {time_str: time_seconds, value_str: data}
        self.__collections[acceleration_str].insert_one(acceleration)

    def save_throttle(self, time_seconds, data):
        throttle = {time_str: time_seconds, value_str: data}
        self.__collections[throttle_str].insert_one(throttle)

    def save_fuel(self, time_seconds, data):
        fuel = {time_str: time_seconds, value_str: data}
        self.__collections[fuel_str].insert_one(fuel)

    def save_longitude(self, time_seconds, data, stay_minutes, stay_seconds):
        pos = {time_str: time_seconds, value_str: data, stay_minutes_str: stay_minutes, stay_seconds_str: stay_seconds}
        self.__collections[longitude_str].insert_one(pos)

    def save_latitude(self, time_seconds, data, stay_minutes, stay_seconds):
        pos = {time_str: time_seconds, value_str: data, stay_minutes_str: stay_minutes, stay_seconds_str: stay_seconds}
        self.__collections[latitude_str].insert_one(pos)

manager = DBManager()





