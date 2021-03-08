# Laron Lemon, Student ID: #000927228

from clock import *
from package import *
from datetime import datetime
import datetime
import textwrap


# define class truck and attributes
class Truck:
    def __init__(self, truck_id, driver, capacity, hub_node):
        self.truck_id = truck_id
        self.driver = driver
        self.capacity = capacity
        self.hub_node = hub_node

        self.loaded_packages = []
        self.mph = 18
        self.driving_time = 0.0
        self.travel_distance = 0.0
        self.total_distance = 0.0
        self.delivery_confirmation = []

        self.next_address = ''
        self.current_node = hub_node
        self.next_node = hub_node

        self.min_node = ''
        self.min_miles = 30.0
        self.max_miles = 30.0

        self.route_complete = False

# load packages onto truck
    def load_truck(self, packages):
        i = 0
        for index in packages:
            self.loaded_packages.append(index)
            i += 1
            if i == self.capacity:
                break
        del(packages[0:self.capacity])

# calculate time to travel from current node to the next node
    def travel_time(self, map_graph):
        self.next_address = self.loaded_packages[0][1]

        # determine name of next node
        for item in map_graph.node_address:
            if self.next_address in item[1][0]:
                self.next_node = item[0]

        # determine distance to next node and time to travel there
        for k in map_graph.edge_weights:
            if self.current_node in k[0] and self.next_node in k[1]:
                self.travel_distance = float(map_graph.edge_weights[k])
                self.total_distance += self.travel_distance
                self.driving_time = round((self.travel_distance / float(self.mph) * 60))
                self.current_node = self.next_node
                return self.driving_time

# delivers package, updates status, removes from truck
    def package_delivery(self, packages, graph_map, clock):
        i = 0
        while i < self.capacity:
            if len(self.loaded_packages) != 0:
                if clock.curr_time == datetime.timedelta(hours=10, minutes=20):
                    self.update_address(packages, '9', '410 S State St.', 'Salt Lake City', '84111')
                self.travel_time(graph_map)
                clock.add_delivery_time(self.driving_time)
                confirmation = [self.loaded_packages[0][0], str(clock.curr_time)]
                self.delivery_confirmation.append(confirmation)
                self.update_delivered(packages)
                del (self.loaded_packages[0])
                self.address_match(clock, self.loaded_packages)
            i += 1
            print('Delivery complete. Press Ctrl + C for menu')
            time.sleep(5)
        print('')
        self.route_complete = True

# update package(s) status to en route
    def update_loaded(self, hash_table):
        for item in self.loaded_packages:
            package_id = item[0]
            result = hash_table.search(package_id)
            result[5] = 'En route'
            hash_table.insert(package_id, result)

# updates package(s) status to delivered
    def update_delivered(self, hash_table):
        for item in self.delivery_confirmation:
            package_id = item[0]
            result = hash_table.search(package_id)
            result[5] = 'Delivered'
            hash_table.insert(package_id, result)

# updates address in hash table and loaded packages list
    def update_address(self, packages, package_id, address, city, zip_code):
        result = packages.search(package_id)
        result[0] = address
        result[1] = city
        result[2] = zip_code
        result[6] = 'Address corrected'
        packages.insert(package_id, result)
        for item in self.loaded_packages:
            if item[0] == package_id:
                item[1] = address
                item[2] = city
                item[3] = zip_code
                item[7] = 'Address corrected'

# check to see if other packages on the truck have the same address and deliver them if they do
    def address_match(self, clock, loaded_packages):
        for item in loaded_packages:
            if item[1] == self.next_address:
                confirmation = [item[0], str(clock.curr_time)]
                self.delivery_confirmation.append(confirmation)
                self.loaded_packages.remove(item)

# check to make sure package 9 is updated before it is delivered
    def wrong_address_check(self):
        update_time = datetime.datetime.strptime('10:20 AM', '%H:%M %p').strftime('%H:%M')
        for item in self.delivery_confirmation:
            if item[0] == '9':
                time_delivered = datetime.datetime.strptime(item[1], '%H:%M:%S').strftime('%H:%M')
                if time_delivered > update_time:
                    print("Packaged 9 delivered to correct address")
                else:
                    print('Package 9 delivered to incorrect address before it was updated')

# compare delivery time with expected delivery time to make sure package is delivered on time
    def delivery_expectation(self, h):
        i = 0
        for item in self.delivery_confirmation:
            result = h.search(item[0])
            if result[4] not in ('EOD', None):
                expected_time = datetime.datetime.strptime(result[4], '%H:%M %p').strftime('%I:%M:%S %p')
                actual_time = datetime.datetime.strptime(item[1], '%H:%M:%S').strftime('%I:%M%S %p')
                if actual_time > expected_time:
                    print('Package ID: %s was late' % item[0])
                    i += 1
        if i == 0:
            print('All packages delivered on time!')

# capture status of packages at different times throughout the day. can be adjusted
# this can be inserted on line 70. removed to de-clutter output
    def capture_status(self, clock, packages):
        if clock.curr_time == datetime.timedelta(hours=9, minutes=5):
            print('Package status at 9:05 AM')
            packages.print()
            print('')
        if clock.curr_time == datetime.timedelta(hours=9, minutes=37):
            print('Package status at 9:37 AM')
            packages.print()
            print('')
        if clock.curr_time == datetime.timedelta(hours=12, minutes=20):
            print('Package status at 12:20 PM')
            packages.print()
            print('')
        return self.route_complete


'''
# greedy algorithm to load packages based on zip code, possibly even closes address...
# i would like to incorporate this in future iterations, except use address matching instead
    def greedy_load(self, i, zip_code, packages):
        package_count = i
        for item in packages:
            if item[3] == zip_code and package_count < self.capacity:
                self.loaded_packages.append(item)
                packages.remove(item)
                package_count += 1
        return package_count
'''

