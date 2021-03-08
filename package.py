# Laron Lemon, Student ID: #000927228

# import libraries and modules
import csv
import time
from datetime import datetime
import datetime
from operator import itemgetter, attrgetter
from truck import *
from hashtable import *


# class to create package object(s)
class Package:
    def __init__(self, package_id, address, city, state, zip_code, delivery_time, weight, special_notes):
        self.packageId = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zipCode = zip_code
        self.deliveryTime = delivery_time
        self.weight = weight
        self.specialNotes = special_notes
        self.delivery_status = "Hub"

        self.next_address = ''

# function to load data into hash table using package objects
    @staticmethod
    def package_data(csv_file, hash_table):
        with open(csv_file) as package_table:
            read_package_table = csv.reader(package_table)
            for row in read_package_table:
                package = Package(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
                value = [package.address, package.city, package.zipCode,
                         package.weight, package.deliveryTime, package.delivery_status, package.specialNotes]
                hash_table.insert(package.packageId, value)

# package search function - user input (# and search term) to determine results from hash table
    @staticmethod
    def search_packages(selection, user_input, hash_table):
        num_input = selection

        # searching by package ID number
        if num_input == 1:
            result = [hash_table.search(str(user_input))]
            result.insert(0, user_input)
            print(result)

        # searching by delivery address
        if num_input == 2:
            i = 1
            found = False
            while i < hash_table.size:
                result = hash_table.search('%s' % i)
                if result[0] == str(user_input):
                    found = True
                    print(result)
                i += 1
            if not found:
                print("No result")

        # searching by delivery city
        if num_input == 3:
            i = 1
            found = False
            while i < hash_table.size:
                result = hash_table.search('%s' % i)
                if result[1] == str(user_input):
                    found = True
                    print(result)
                i += 1
            if not found:
                print("No result")

        # searching by delivery zip code
        if num_input == 4:
            i = 1
            found = False
            while i < hash_table.size:
                result = hash_table.search('%s' % i)
                if result[2] == str(user_input):
                    found = True
                    print(result)
                i += 1
            if not found:
                print("No result")

        # searching by package weight
        if num_input == 5:
            i = 1
            found = False
            while i < hash_table.size:
                result = hash_table.search('%s' % i)
                if result[3] == str(user_input):
                    found = True
                    print(result)
                i += 1
            if not found:
                print("No result")

        # searching by delivery deadline
        if num_input == 6:
            i = 1
            found = False
            while i < hash_table.size:
                result = hash_table.search('%s' % i)
                if result[4] == str(user_input):
                    found = True
                    print(result)
                i += 1
            if not found:
                print("No result")

        # searching by  delivery status
        if num_input == 7:
            i = 1
            found = False
            while i < hash_table.size:
                result = hash_table.search('%s' % i)
                if result[5] == str(user_input):
                    found = True
                    print(result)
                i += 1
            if not found:
                print("No result")

# define restrictions to limit how to sort packages
    @staticmethod
    def restriction_s(package_table):
        required_together = []
        delivery_time = []
        delayed = []
        no_restrictions = []
        i = 1

    # loads data into restrictions arrays
        while i < package_table.size:
            priority = 0
            result = package_table.search('%s' % i)
            sorting_data = [str(i), result[0], result[3], result[4], result[6], priority]
            if result[6] == 'Wrong address listed':
                no_restrictions.append(sorting_data)
            elif str(i) in ('13', '14', '15', '16', '19', '20'):
                required_together.append(sorting_data)
            elif result[6] == 'Delayed on flight---will not arrive to depot until 9:05 am':
                delayed.append(sorting_data)
            elif result[4] not in ('EOD', None):
                delivery_time.append(sorting_data)
            else:
                no_restrictions.append(sorting_data)
            i += 1

        # sorts by expected delivery time and assigns a value
        required_together.sort(key=itemgetter(2), reverse=True)
        min_time = datetime.datetime.strptime('11:59 PM', '%H:%M %p').strftime('%I:%M %p')
        for item in required_together:
            if item[3] not in ('EOD', None):
                curr_time = datetime.datetime.strptime(item[3], '%H:%M %p').strftime('%I:%M %p')
                if curr_time < min_time:
                    item[5] += 200
                    min_time = curr_time
                else:
                    item[5] += 100
                    min_time = curr_time

        # sorts by expected delivery time and assigns a value
        delivery_time.sort(key=itemgetter(2), reverse=True)
        for item in delivery_time:
            curr_time = datetime.datetime.strptime(item[3], '%H:%M %p').strftime('%I:%M %p')
            if curr_time < min_time:
                item[5] += 200
                min_time = curr_time
            else:
                item[5] += 100
                min_time = curr_time

        # sorts by expected delivery time and assigns a value
        delayed.sort(key=itemgetter(2), reverse=True)
        for item in delayed:
            if item[3] not in ('EOD', None):
                curr_time = datetime.datetime.strptime(item[3], '%H:%M %p').strftime('%I:%M %p')
                if curr_time < min_time:
                    item[5] += 200
                    min_time = curr_time
                else:
                    item[5] += 100
                    min_time = curr_time
        # sorts each list by priority value
        required_together.sort(key=itemgetter(5), reverse=True)
        delayed.sort(key=itemgetter(5))
        delivery_time.sort(key=itemgetter(5))
        no_restrictions.sort(key=itemgetter(4))
        return required_together, delivery_time, no_restrictions, delayed

# greedy algorithm - sorts packages by zip code and restrictions
# assumption is zip code will group closest packages
    @staticmethod
    def package_selection(package_table, restrictions):
        selected_packages = []
        loaded_zip = []
        truck_2 = []
        sort_last = []

        for index in restrictions[0]:
            result = [index[0]] + package_table.search(index[0])
            zip_code = result[3]
            loaded_zip.append(zip_code)
            selected_packages.append(result)

        for index in restrictions[1]:
            result = [index[0]] + package_table.search(index[0])
            if result[3] in loaded_zip:
                selected_packages.append(result)
            else:
                sort_last.append(result)

        for index in restrictions[2]:
            result = [index[0]] + package_table.search(index[0])
            if result[3] in loaded_zip:
                selected_packages.append(result)
            elif result[7] == 'Can only be on truck 2':
                truck_2.append(result)
            else:
                sort_last.append(result)

        for index in sort_last:
            selected_packages.append(index)

        for index in truck_2:
            selected_packages.insert(22, index)

        for index in restrictions[3]:
            result = [index[0]] + package_table.search(index[0])
            selected_packages.insert(16, result)

        return selected_packages

# determine zip codes of packages
    @staticmethod
    def zip_code(packages):
        zip_codes = []
        for item in packages:
            zip_codes.append(int(item[3]))
        zip_set = set(zip_codes)
        zip_codes = list(map(str, zip_set))
        return zip_codes

