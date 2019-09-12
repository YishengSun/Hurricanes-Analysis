"""
Tips: You should pip install these libraries before run our program: pygeodesy, prettytable and copy.
"""

import sys
from pygeodesy import ellipsoidalVincenty as ev
from prettytable import PrettyTable
import math
import copy
results_and_aggregate_report=open("Atlantic Results and Aggregate report.txt", 'w+')
# results_and_aggregate_report=open("Pacific Results and Aggregate report.txt", 'w+')

f = open('hurdat2-1851-2017-050118.txt')
# f = open('hurdat2-nepac-1949-2017-050418.txt')

line = f.readline()
Storm_Id_list = []  # record all the storms' IDs
time_list = []
# record the interval time between current data line and previous data line of each storm
# (will be 0 if it is first line data of a storm)
area_list = []  # record the hurricane surface area for each storm
distance_list = []  # record the move distance for each storm
max_speed_list = []  # record max speed for each storm
mean_speed_list = []  # record mean speed for each storm
relative_power = []  # record relative power for each data row
best_tracks_list = []  # record the number of data rows for each storm
relative_energy = []  # record relative energy for each data row


def distance_cal(locations):
    """
    calculate the distance in nautical miles by longitude and the latitude
    :param locations: a list of nodes containing the longitude and the latitude of locations
    :return:total distance between locations
    """
    if len(locations) == 1:
        t_dis = 0
    else:
        node = []
        i = 0
        while i < len(locations):
            node.append(ev.LatLon(locations[i][0], locations[i][1]))
            i += 1
        j = 0
        temp_dis = []
        while j < (len(locations) - 1):
            temp_dis.append(node[j].distanceTo(node[j + 1]))
            j += 1
        t_dis = sum(temp_dis)/1852.0
    return t_dis


def speed_cal(locations, time):
    """
    calculate the speed of the storm
    :param locations: a list of nodes containing the longitude and the latitude of locations
    :param time: a list of time containing the time that a storm travels from one spot to another
    :return: a list of storm speed
    """
    if len(locations) == 1:
        speed1 = 0
    else:
        node = []
        p = 0
        while p < len(locations):
            node.append(ev.LatLon(locations[p][0], locations[p][1]))
            p += 1
        j = 0
        temp_dis = []
        while j < (len(locations) - 1):
            temp_dis.append(node[j].distanceTo(node[j + 1]))
            j += 1

        speed1 = []
        for p in range(len(time)):
            if time == 0:
                speed1.append(0)
            else:
                speed1.append((int(temp_dis[p])/1852.0)/time[p])
    return speed1


def time_cal(time):
    """
    calculate the time that a storm used from one location to another
    :param time: a list of time with format as "0000" representing for the hour and minute
    :return: the actual time a storm used from one location to another in the format "600"
    """
    if len(time) == 1:
        storm_time = [0]
    else:
        time_rows = []
        k = 0
        while k < (len(time)-1):
            if (time[k + 1] == "0000") & (int(time[k])% 100 != 0):
                time_rows.append(2360 - int(time[k]))
            elif (time[k + 1] == "0000") & (int(time[k])% 100 == 0):
                time_rows.append(2400 - int(time[k]))
            elif (time[k+1] != "0000") & (int(time[k+1])% 100 == 0) & (int(time[k])%100 != 0):
                time_rows.append((int(time[k + 1]) - 40) - int(time[k]))
            else:
                time_rows.append(int(time[k + 1]) - int(time[k]))
            k += 1
        storm_time = time_rows
    return storm_time


def time_transform(time):
    """
    change the format of time from "600" to 6 hours.
    :param time: time in the format as "600"
    :return: time in hour
    """
    if time == 0:
        storm_time = 0
    else:
        storm_time = []
        for i in range(len(time)):
            hour = time[i] // 100
            l2_digits = time[i]%100
            if l2_digits == 0:
                minute = 0
            else:
                minute = l2_digits/60
            real_time = hour + minute
            storm_time.append(real_time)
    return storm_time


def time_cal1(time):
    """
    calculate the time that a storm used from one location to another
    :param time: a list of time with format as "0000" representing for the hour and minute
    :return: the actual time a storm used from one location to another in the format "600"
    """
    if len(time) == 1:
        storm_time = [0]
    else:
        time_rows = [0]
        k = 0
        while k < (len(time)-1):
            if (time[k + 1] == "0000") & (int(time[k])% 100 != 0):
                time_rows.append(2360 - int(time[k]))
            elif (time[k + 1] == "0000") & (int(time[k])% 100 == 0):
                time_rows.append(2400 - int(time[k]))
            elif (time[k+1] != "0000") & (int(time[k+1])% 100 == 0) & (int(time[k])%100 != 0):
                time_rows.append((int(time[k + 1]) - 40) - int(time[k]))
            else:
                time_rows.append(int(time[k + 1]) - int(time[k]))
            k += 1
        storm_time = time_rows
    return storm_time


def sum_add(a_list):
    """To calculate the value of each position of a list of integers to
    the sum of all previous Numbers.Like a=[1,2,3] -> a1=[1,3,6]

    :param a_list: a list contains integers
    :return: a new list after the calculation
    """
    n = 1
    list1 = copy.deepcopy(a_list)
    sum_add_list = [list1[0]]
    while n < len(list1):
        list1[n] += list1[n - 1]
        sum_add_list.append(list1[n])
        n += 1
    return sum_add_list


def piece_calculation(data, indices):
    """Sum the incoming data according to the indices
     and store it in a new list. like data=[1,2,3,4,5],
     indices=[2,3] then return [3,12] which means sum
     the first 2 elements and last 3 separately.


    :param data: a list of numbers
    :param indices: a list of numbers as indices
    :return: a list after the piece calculation
    """

    z = 0
    sum1 = [sum(data[0:indices[0]])]
    indices_sum = sum_add(indices)
    while z < len(indices_sum) - 1:
        add = sum(data[indices_sum[z]:indices_sum[z + 1]])
        sum1.append(add)
        z += 1
    return sum1


def split(somelist, ind_list):
    """split a list to several small lists according to
    the indices and record these new lists in a list.
    Like soimelist=[1,2,3,4,5], ind_list=[2,3]
    then we get [[1,2],[3,4,5]].

    :param somelist:
    :param ind_list:
    :return:a new list contains the lists generated by this split process
    """
    m = 0
    list0 = [somelist[0:ind_list[0]]]
    ind_list_sum = sum_add(ind_list)

    while m < len(ind_list_sum)-1:
        list0.append(somelist[ind_list_sum[m]:(ind_list_sum[m+1])])
        m += 1
    return list0


def list_multiply(list1, list2):
    """Multiply the Numbers in the two lists each by each

    :param list1: a list of numbers
    :param list2: a list of numbers which have same quantity as list1
    :return: a new list record the result of multiplication
    """
    list3 = []
    k = 0
    while k < len(list1):
        list3.append(list1[k]*list2[k])
        k += 1
    return list3


while line:

    if line[0].isalpha():
        i = 1  # Count how many data lines have been processed
        time_get = []
        location = []
        max_sustained_wind = 0
        wind_date = ""

        Storm_Id = line[0:8]
        Storm_Id_list.append(Storm_Id)
        Best_Tracks = int(line[34:36])
        best_tracks_list.append(Best_Tracks)

        while i < Best_Tracks + 1:  # read each storm's data line
            line = f.readline()
            time_get.append(line[10:14])
            location.append((line[23:28], line[31:36]))
            sustained_wind = int(line[38:41])
            if sustained_wind > 0:
                relative_power.append(sustained_wind**3)
            else:
                relative_power.append(0)
            NE_og = int(line[97:101].replace(" ", ""))
            SE_og = int(line[103:107].replace(" ", ""))
            SW_og = int(line[109:113].replace(" ", ""))
            NW_og = int(line[115:119].replace(" ", ""))
            if NE_og < 0:
                area = 0
            else:
                area = 0.25*math.pi*(NE_og**2+SE_og**2+SW_og**2+NW_og**2)
            area_list.append(area)
            i += 1
        row_time = time_transform(time_cal(time_get))
        row_time1 = time_transform(time_cal1(time_get))
        time_list = time_list + row_time1

        distance = distance_cal(location)
        distance_list.append(distance)

        speed = speed_cal(location, row_time)
        if speed == 0:
            max_speed = 0
            mean_speed = 0
        else:
            max_speed = max(speed)
            mean_speed = sum(speed) / len(speed)

        max_speed_list.append(max_speed)
        mean_speed_list.append(mean_speed)
    else:
        pass
    line = f.readline()

row_time = time_transform(time_cal(time_get))

relative_energy = list_multiply(relative_power, time_list)

TRSE = piece_calculation(relative_energy, best_tracks_list)

each_storm_all_area = split(area_list, best_tracks_list)
each_storm_max_area = []
for each_area in each_storm_all_area:
    each_storm_max_area.append(max(each_area))

table = PrettyTable()
table.align = "l"
table.add_column("Storm Id", Storm_Id_list)
table.add_column("Total Distance", distance_list)
table.add_column("Maximum Propagation Speed", max_speed_list)
table.add_column("Mean Propagation Speed", mean_speed_list)
table.add_column("TRSE", TRSE)
table.add_column("Maximum Hurricane Area", each_storm_max_area)

print(table)
print(table, file=results_and_aggregate_report)

ID_mean_speed = dict(zip(Storm_Id_list, mean_speed_list))
ID_TRSE = dict(zip(Storm_Id_list, TRSE))
ID_max_hurricane_area = dict(zip(Storm_Id_list, each_storm_max_area))

sorted_ID_mean_speed = sorted(ID_mean_speed.items(), key=lambda x: x[1], reverse=True)
top10_ID_mean_speed = sorted_ID_mean_speed[0:10]
top10_mean_speed_ID = []

for i in top10_ID_mean_speed:
    top10_mean_speed_ID.append(i[0])

sorted_ID_TRSE = sorted(ID_TRSE.items(), key=lambda x: x[1], reverse=True)
top10_TRSE = sorted_ID_TRSE[0:10]
top10_TRSE_ID = []

for i in top10_TRSE:
    top10_TRSE_ID.append(i[0])

sorted_ID_max_hurricane_area = sorted(ID_max_hurricane_area.items(), key=lambda x: x[1], reverse=True)
top10_max_hurricane_area = sorted_ID_max_hurricane_area[0:10]
top10_ID_max_hurricane_area = []


for i in top10_max_hurricane_area:
    top10_ID_max_hurricane_area.append(i[0])

print('The 10 fastest-propagating storms (from mean propagation), in descending order' + str(top10_mean_speed_ID) + '\n'
      + 'The 10 most-energetic storms (from TRSE), in descending order:' + str(top10_TRSE_ID) + '\n'
      + 'The 10 biggest hurricanes (from maximum hurricane-level surface area), in descending order: '
      + str(top10_ID_max_hurricane_area))
print('The 10 fastest-propagating storms (from mean propagation), in descending order' + str(top10_mean_speed_ID) + '\n'
      + 'The 10 most-energetic storms (from TRSE), in descending order:' + str(top10_TRSE_ID) + '\n'
      + 'The 10 biggest hurricanes (from maximum hurricane-level surface area), in descending order: '
      + str(top10_ID_max_hurricane_area), file=results_and_aggregate_report)

f.close()
results_and_aggregate_report.close()
sys.exit()













