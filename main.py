# Laron Lemon, Student ID: #000927228


from hashtable import *
from mapgraph import *
from package import *
from mapgraph import *
from truck import *
from clock import *
from enum import Enum
import datetime
import os
import pprint


# 3 states the app can be in
class AppState(Enum):
    running = 0
    paused = 1
    stopped = 2


# main class of application
class Application:
    def __init__(self):
        self.state = AppState.running
        self.key_bindings = {
            'p': self.print_package_table,
            't': self.time_print,
            's': self.package_search,
            'a': self.advanced_search,
            'r': self.resume,
            'q': self.quit
        }

        # delivery map and map data
        self.delivery_map = None
        self.map_datafile = 'WGUPS Distance Table.csv'

        # hash table and package data
        self.package_table = None
        self.package_datafile = 'WGUPS Package File.csv'
        self.restrictions = None
        self.sorted_packages = None

        # trucks
        self.truck_1 = None
        self.truck_2 = None
        self.truck_3 = None

        # clocks
        self.clock_1 = None
        self.clock_2 = None
        self.clock_3 = None

# starts program
    def start(self):
        if __name__ == '__main__':
            self.main_operations()

# loads classes, methods and data
    def load(self):

        # create hash table
        print('Generating package hash table...\n')
        self.package_table = HashTable()
        time.sleep(5)

        # create graph
        print('Generating delivery map...\n')
        self.delivery_map = Graph()
        time.sleep(5)

        # create and sort packages
        print('Creating packages...\n')
        Package.package_data(self.package_datafile, self.package_table)
        time.sleep(5)
        print('Sorting packages...\n')
        self.restrictions = Package.restriction_s(self.package_table)
        self.sorted_packages = Package.package_selection(self.package_table, self.restrictions)
        time.sleep(5)

        # create location objects and load data into graph
        print('Loading delivery map data...\n')
        Graph.map_data(self.map_datafile, self.delivery_map)
        time.sleep(5)

        # create truck objects
        print('Creating trucks...\n')
        self.truck_1 = Truck(1, 'driver 1', 16, 'Western Governors University')
        self.truck_2 = Truck(2, 'driver 2', 16, 'Western Governors University')
        self.truck_3 = Truck(3, 'driver 1', 16, 'Western Governors University')
        time.sleep(5)

        # creating clocks
        self.clock_1 = Clock(8, 00)
        self.clock_2 = Clock(9, 5)
        print('Truck 1 start time: %s' % self.clock_1.curr_time)
        print('Truck 2 start time: %s' % self.clock_2.curr_time)
        print('')
        time.sleep(5)

        # load trucks
        print('Loading trucks...\n')
        Truck.load_truck(self.truck_1, self.sorted_packages)
        Truck.load_truck(self.truck_2, self.sorted_packages)
        Truck.load_truck(self.truck_3, self.sorted_packages)
        time.sleep(5)

        # update status to "En route"
        print('Updating package status to En route...\n')
        self.truck_1.update_loaded(self.package_table)
        self.truck_2.update_loaded(self.package_table)
        self.truck_3.update_loaded(self.package_table)
        time.sleep(5)

# pauses program
    def pause(self):
        self.state = AppState.paused

# stops program
    def stop(self):
        self.state = AppState.stopped

# resumes program
    def resume(self):
        self.state = AppState.running
        self.main_operations()
        return True

# displays total miles driven by trucks and shuts down program
    def complete(self):
        # calculates total miles traveled
        miles_travelled = self.truck_1.total_distance + self.truck_2.total_distance + self.truck_3.total_distance
        print('Deliveries completed.\n')
        # prints delivery confirmation (package_id, time_delivered)
        print('Truck 1 delivery confirmations:')
        print(self.truck_1.delivery_confirmation)
        print('Truck 2 delivery confirmations:')
        print(self.truck_2.delivery_confirmation)
        print('Truck 3 delivery confirmations:')
        print(self.truck_3.delivery_confirmation)
        packages_delivered = \
            len(self.truck_1.delivery_confirmation) + len(self.truck_2.delivery_confirmation) +\
            len(self.truck_3.delivery_confirmation)
        print('Total packages delivered: %s' % packages_delivered)
        print('')
        print('Total miles traveled: %s' % miles_travelled)
        print('')
        time.sleep(5)

        self.print_package_table()
        time.sleep(5)

        self.quit()

# quits program
    def quit(self):
        self.stop()
        print('Exiting application')
        return True

# prints hash table
    def print_package_table(self):
        print('HashTable:')
        self.package_table.print()
        return False

# prints hash table at a specific point in time entered by the user
    def time_print(self):
        print("Time is represented with a 24-hour clock")
        hours = int(input('Please enter a number from 1-23 for the hour: '))
        minutes = int(input('Please enter a number from 1-59 for the minutes: '))
        if self.clock_1.start_time <= datetime.timedelta(hours=hours, minutes=minutes) <= self.clock_1.curr_time:
            self.print_package_table()
        elif self.clock_2.start_time <= datetime.timedelta(hours=hours, minutes=minutes) <= self.clock_2.curr_time:
            self.print_package_table()
        else:
            print('Time entered is out of range.')

    def package_search(self):
        package_id = input('Please enter a package Id: ')
        result = self.package_table.search(str(package_id))
        print('Result of searching for package ID 1:\n%s' % result)

    def package_update(self):
        self.truck_2.update_address(self.package_table, '9', '410 S State St.', 'Salt Lake City', '84111')

    def main_operations(self):
        # Performs bulk of operations
        # Keyboard Interrupt
        try:
            while self.state != AppState.stopped:

                self.load()
                # drive route and update package to delivered
                self.truck_1.package_delivery(self.package_table, self.delivery_map, self.clock_1)
                self.truck_2.package_delivery(self.package_table, self.delivery_map, self.clock_2)
                self.truck_3.package_delivery(self.package_table, self.delivery_map, self.clock_1)

                # confirms package 9 address updated before it was delivered
                self.truck_1.wrong_address_check()
                self.truck_2.wrong_address_check()
                self.truck_3.wrong_address_check()
                print('')

                # confirms packages were delivered on time
                print('Truck 1:')
                self.truck_1.delivery_expectation(self.package_table)
                time.sleep(1)
                print('Truck 2:')
                self.truck_2.delivery_expectation(self.package_table)
                time.sleep(1)
                print('Truck 3:')
                self.truck_3.delivery_expectation(self.package_table)
                print('')
                time.sleep(1)
                self.complete()

        # if the user presses Ctrl + C the program is paused
        except KeyboardInterrupt:
            self.pause()
            terminated = False

            # Displays menu if program does not terminate
            while not terminated:
                print('Program paused')
                print('Press [p] to print all packages')
                print('Press [t] to print all packages at a given time')
                print('Press [s] to search all packages')
                print('Press [a] to advanced search all packages')
                print('Press [r] to resume program')
                print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
                print('Press [q] to quit program')
                print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
                user_input = input('+> ')
                try:
                    terminated = self.key_bindings[user_input.lower()]()
                except KeyError:
                    pass

# advanced search option
    def advanced_search(self):
        data_type = int(input('Please enter an an integer from  1-7: '))
        value = str(input('Please enter a search value/keyword: '))
        Package.search_packages(data_type, value, self.package_table)


Application().start()

# everything below this comment is code I used to create the application itself.
'''
# instantiate hash table
h = HashTable()

# instantiate map (graph)
delivery_map = Graph()

# load package csv, possibly obtain user input -> csv path and/or file name
package_datafile = 'WGUPS Package File.csv'

# option to automate program further - can use any csv file
package_datafile = input("Please enter the name of the csv file you want to use.\n")
while (not os.path.isfile(package_datafile)) or (not os.path.exists(package_datafile)):
    package_datafile = input("Invalid file name! Please enter the name of the file you'd like to use.\n")


# create package objects and load data into hash table
Package.package_data(package_datafile, h)

# print hash table
print('HashTable:')
h.print()
print('')

# print hash table size - should always be 1 more than # of rows in csv file
print('HashTable size: %s' % h.size)
print('')

# search hash table using the key; must be a string ''
result = h.search('1')
print('Result of searching for package ID 1:\n%s' % result)
print('')

# create restrictions nested lists for priority sorting
# option 1
restriction_s = Package.restriction_s(h)

# select packages to load onto the trucks
sorted_packages = Package.package_selection(h, restriction_s)

# creates a list of zip codes in packages
zip_codes = Package.zip_code(sorted_packages)
print(zip_codes)
print('')

# look-up/search function to search for data
# 1 = Package ID Number
# 2 = delivery address
# 3 = delivery city
# 4 = delivery zip code
# 5 = package weight
# 6 = delivery deadline
# 7 = delivery status
Package.search_packages(1, '38', h)
print('')

# load map csv, possibly obtain user input -> csv path/file name
map_datafile = 'WGUPS Distance Table.csv'

# option to automate program further - can use any csv file
map_datafile = input("Please enter the name of the csv file you want to use.\n")
while (not os.path.isfile(map_datafile)) or (not os.path.exists(map_datafile)):
    map_datafile = input("Invalid file name! Please enter the name of the file you'd like to use.\n")


# create location objects and load data into graph
Graph.map_data(map_datafile, delivery_map)

# start the clock
clock_1 = Clock(8, 00)
clock_2 = Clock(9, 5)
print('Truck 1 start time: %s' % clock_1.curr_time)
print('Truck 2 start time: %s' % clock_2.curr_time)
print('')

# create truck objects
truck_1 = Truck(1, 'driver 1', 16, 'Western Governors University')
truck_2 = Truck(2, 'driver 2', 16, 'Western Governors University')
truck_3 = Truck(3, 'driver 1', 16, 'Western Governors University')

# load trucks
Truck.load_truck(truck_1, sorted_packages)
Truck.load_truck(truck_2, sorted_packages)
Truck.load_truck(truck_3, sorted_packages)
print(truck_1.loaded_packages)
print(truck_2.loaded_packages)
print(truck_3.loaded_packages)
print('')


# update status to "En route"
truck_1.update_loaded(h)
truck_2.update_loaded(h)
truck_3.update_loaded(h)

# update address
truck_2.update_address(h, '9', '410 S State St.', 'Salt Lake City', '84111')

# drive route and update package to delivered
truck_1.package_delivery(h, delivery_map, clock_1)
truck_2.package_delivery(h, delivery_map, clock_2)
truck_3.package_delivery(h, delivery_map, clock_1)

# prints delivery confirmation (package_id, time_delivered)
print(truck_1.delivery_confirmation)
print(truck_2.delivery_confirmation)
print(truck_3.delivery_confirmation)
print('')

# confirms package 9 address updated before it was delivered
truck_1.wrong_address_check()
truck_2.wrong_address_check()
truck_3.wrong_address_check()
print('')

# confirms packages were delivered on time
truck_1.delivery_expectation(h)
truck_2.delivery_expectation(h)
truck_3.delivery_expectation(h)
print('')

# calculates total miles traveled
miles_travelled = truck_1.total_distance + truck_2.total_distance + truck_3.total_distance
print('Total miles traveled: %s' % miles_travelled)
'''



