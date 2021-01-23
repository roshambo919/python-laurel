# -*- coding: utf-8 -*-
# @Author: spencer
# @Date:   2021-01-23
# @Last Modified by:   Spencer H
# @Last Modified date: 2021-01-23
# @Description: 
"""
Testing script
"""

import laurel

with open('../login.txt') as f:
    login_data = f.read()
username = login_data.split(',')[0]
password = login_data.split(', ')[1]

print('Logging in...')
devices = laurel.laurel(username, password)
print('Successfully logged in!')
devices = devices.devices

idx = 5
print('Name: {}\nMAC: {}\nType: {}\nBrightness: {}\nTemperature: {}\n'.format(
    devices[idx].name,
    devices[idx].mac,
    devices[idx].type,
    devices[idx].brightness,
    devices[idx].temperature))

print('Connecting...')
devices[idx].network.connect(idx_start = idx)

print('Setting brightness')
devices[idx].set_brightness(10)