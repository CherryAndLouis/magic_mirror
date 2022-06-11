# -*- coding: utf-8 -*-

class PublicMeth():
    # def __init__(self):

    def rmdup(self, list):
        list_temp = set()
        for data in list:
            list_temp.add(data)
        return list_temp
