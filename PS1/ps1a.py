###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time
import copy

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    cows_dic = {}
    with open(filename,'r') as f:
        while True:
            line = f.readline()
            if line:
                cows_dic[line.split(',')[0].strip()] = line.split(',')[1].strip()
            else:
                break
    return cows_dic

# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    cows_copy = copy.copy(cows)
    new_cows = {key: val for (key,val) in sorted(cows_copy.items(), key = lambda t:  t[1], reverse = True)}
    result = []
    while len(new_cows) > 0:
        totalWeight = 0
        trip_result = []
        for key in new_cows.keys():
            if (totalWeight + int(new_cows.get(key))) <= limit:
                trip_result.append(key)
                totalWeight += int(new_cows.get(key))
        for key in trip_result:
            if key in new_cows:
                del new_cows[key]
        result.append(trip_result)
    return result

# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    dicTotalWeight = sum([int(i) for i in cows.values()])
    for partition in sorted(get_partitions(cows.keys()), key= lambda l: len(l), reverse = False):
        partitionTotalWeight = 0
        for comb in partition:
            totalWeight = 0
            for cow in comb:
                totalWeight+= int(cows.get(cow))
            if totalWeight <= 10:
                partitionTotalWeight +=totalWeight
            else:
                break
        if partitionTotalWeight == dicTotalWeight:
            return partition
        
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    cows_dic = load_cows('ps1_cow_data.txt')
    print (cows_dic)
    start_time = time.time()
    print ('greedy cow transport: ', greedy_cow_transport(cows_dic))
    print ('--- %s seconds ---' %(time.time() - start_time))
    start_time = time.time()
    print ('brute force cow transport: ', brute_force_cow_transport(cows_dic))
    print ('--- %s seconds ---' %(time.time() - start_time))

def main():
    compare_cow_transport_algorithms()

if __name__ == '__main__':
    main()