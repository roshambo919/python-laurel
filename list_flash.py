#!/usr/bin/env python3
# flashy_lights.py
# William Kenny
# william.j.kenny.ak@gmail.com
# 
# Utility to flash "holiday" lights using C by GE Smart Plugs
# Load up required modules first...
import laurel #module to communicate with C by GE products
import time
import random
import sys
import shelve
import argparse

with open('../login.txt') as f:
    login_data = f.read()
username = login_data.split(',')[0]
password = login_data.split(', ')[1]

# Let's deal with command line variables...
parser = argparse.ArgumentParser()
parser.add_argument("-tm","--timing_min", type=float, default=0.1, help='time lights will be flashed on for (0.1)')
parser.add_argument("-tmm","--timing_max", type=float, default=0.6, help='time lights will be flashed off for (0.6)')
parser.add_argument("-lm","--loop_min", type=int, default=3, help='min number of times lights will be flashed (3)')
parser.add_argument("-lmm","--loop_max", type=int, default=7, help='max number of times lights will be flashed (7)')
parser.add_argument("-r","--resting_state",action='store_true',default=False, help='state lights will be in when not flashing -- True is on, False is off. (False)')
parser.add_argument("-rt","--run_time", type=int, default=5, help='time in minutes script will run for in minutes (5)')
parser.add_argument("-p","--print_args",action='store_true', help='print arguments (False)')
parser.add_argument("-t", "--test_timing",action='store_true', help='test timing functions only (False)')
parser.add_argument("-f", "--flash", action='store_true', help='flash the lights once for testing (False)')
parser.add_argument("-v", "--verbose", action='store_true', help='sets verbose mode (False)')
parser.add_argument("-l", "--loop", action='store_true', help='do one loop and exit (False)')
parser.add_argument("-blm", "--between_loops_min", type=int, default=5,help='minimum time between loops in seconds (5)')
parser.add_argument("-blmm", "--between_loops_max", type=int, default=15,help='maximum time between loops in seconds (25)')
args = parser.parse_args()

#List out the arguments if we tell it to...
if args.print_args == True or args.verbose == True:
    print(f'timing_min      = {args.timing_min}')
    print(f'timing_max      = {args.timing_max}')
    print(f'loop_min        = {args.loop_min}')
    print(f'loop_max        = {args.loop_max}')
    print(f'resting_state   = {args.resting_state}')
    print(f'run_time        = {args.run_time}')
    print(f'print_args      = {args.print_args}')
    print(f'test_timing     = {args.test_timing}')
    print(f'flash           = {args.flash}')
    print(f'verbose         = {args.verbose}')


idx_dev = 0
#Let's flash the lights
# function flash_it
#    turns light on, then off using predetermined lengths of on and off times
#    timing_on  - float - time lights will be on (resolution to 2 decimal points, no less than .10
#    timing_off - float - time lights will be off (resolution to 2 decimal points, no less than .10
def flash_it(timing_on,timing_off,v):
    #turn lights on
    if v == True:
        print(f' ON for {timing_on} seconds.')
    if args.test_timing == False:
        devices.devices[idx_dev].set_power(True)
    #wait before we turn it off for <timeon> seconds
    time.sleep(timing_on)
    #turn lights off
    if v == True:
        print(f' OFF for {timing_off} seconds.')
        print()
    if args.test_timing == False:
        devices.devices[idx_dev].set_power(False)
    #wait before we move on for <timeoff> seconds
    time.sleep(timing_off)

# function get_flash_it_timing
#    randomly generates timing for "flash_it" using 2 floating point numbers
#    tm - float - minimum time lights will be on/off
#    tmm - float - maximum time lights will be on/off
def get_flash_it_timing(tm,tmm):
    return round(random.uniform(tm,tmm),2)

# function get_loop_amount
#    randomly sets number of times "flash_it" will loop
#    loop_min - int - minimum times "flash_it" will loop
#    loop_max - int - maximum times "flash_it" will loop
def get_loop_amount(lm,lmm):
    return random.randint(lm,lmm)

# function get_loop_timing
#    randomly sets time between loops
#    between_loops_min - int - minimum time between loops
#    between_loops_max - int - maximum time between loops
def get_loop_timing(blm,blmm):
    return random.randint(blm,blmm)

# function cache_it
#    caches variables to file so we can save some time
#    file_name - path to file where data will be cached
param = ""
def cache_it(file_name):
    d = shelve.open(file_name)
    def decorator(func):
        def new_func(param):
            if param not in d:
                d[param] = func(param)
            return d[param]
        return new_func
    return decorator

# function get_devices(param) -- this is cached by using @chache_it(file_name)
#    This function will usually take 5-20 seconds depending on internet latency and server response times.
#    param - cached data...
#    Let's set our filename to use for caching our data...
file_name = "flashy_lights_devices.cache"
# @cache_it(file_name)
def get_devices(param):
    #I want to find a way to hash the password...  More to come...
    return(laurel.laurel(username, password))


# Let's get to it already!!!

#First, we need to connect...
if args.test_timing == False:
    devices = get_devices(param)
    devices.devices[idx_dev].network.connect(idx_start=idx_dev)
#Should we do a test flash?
if args.flash == True:
    timing_on = get_flash_it_timing(args.timing_min,args.timing_max)
    timing_off = get_flash_it_timing(args.timing_min,args.timing_max)
    flash_it(timing_on,timing_off,args.verbose)

if args.loop == True:
    num_loops = get_loop_amount(args.loop_min,args.loop_max)
    if args.verbose == True:
        print(f'looping {num_loops} times')
    i = 0
    while i < num_loops:
        timing_on = get_flash_it_timing(args.timing_min,args.timing_max)
        timing_off = get_flash_it_timing(args.timing_min,args.timing_max)
        flash_it(timing_on,timing_off,args.verbose)
        i+=1

if args.loop == True or args.flash == True:
    args.run_time = 0

if args.run_time > 0:
    if args.verbose == True:
        if args.resting_state == False:
            state = "off"
            if args.test_timing == False:
                devices.devices[idx_dev].set_power(False)
        else:
            state = "on"
            if args.test_timing == False:
                devices.devices[idx_dev].set_power(False)
        print(f'Lights will be {state} between flash_it loops.')
    t_end = time.time() + 60*args.run_time
    while time.time() < t_end:
        num_loops = get_loop_amount(args.loop_min,args.loop_max)
        if args.verbose == True:
            print(f'looping {num_loops} times')
        i = 0
        while i < num_loops:
            timing_on = get_flash_it_timing(args.timing_min,args.timing_max)
            timing_off = get_flash_it_timing(args.timing_min,args.timing_max)
            flash_it(timing_on,timing_off,args.verbose)
            i+=1
        pause_time = get_loop_timing(args.between_loops_min,args.between_loops_max)
        if args.verbose == True:
            print(f'Waiting for {pause_time} seconds.')
        time.sleep(pause_time)