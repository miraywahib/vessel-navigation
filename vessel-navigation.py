import math
import random

MIN_LAT=-90 #LAT=latitude
MAX_LAT=90
MIN_LONG=-180 #LONG=longitude
MAX_LONG=180
EARTH_RADIUS=6371 #in kilometers

RZONE_LAT=25 #latitude of restricted zone
RZONE_LONG=-71 #longitude of restricted zone
RZONE_RADIUS=400 #radius around coordinates that constitutes restricted zone
HAZARD_LAT_MIN=40 #minimum latitude of hazardous zone
HAZARD_LAT_MAX=41 #maximum latitude of hazardous zone
HAZARD_LONG_MIN=-71 #minimum longitude of hazardous zone
HAZARD_LONG_MAX=-70 #maximum longitude of hazardous zone

def meter_to_feet(meter):
    """
    Converts a measurement from meters to feet.

    Parameters:
        meter (float): The measurement in meters to be converted to feet.
    Returns:
        float: The measurement converted to feet, rounded to 2 decimal places.

    Examples:
    >>> meter_to_feet(1.0)
    3.28
    >>> meter_to_feet(2.5)
    8.20
    >>> meter_to_feet(0.75)
    2.46
    """
    return round(meter*3.28,2)

def degrees_to_radians(degrees):
    """
    Converts an angle from degrees to radians.

    Parameters:
        degrees (float): The angle in degrees to be converted to radians.
    Returns:
        float: The angle converted to radians, rounded to 2 decimal places.

    Examples:
    >>> degrees_to_radians(90)
    1.57
    >>> degrees_to_radians(45)
    0.79
    >>> degrees_to_radians(180)
    3.14
    """
    return round(degrees*(math.pi/180),2)

def get_vessel_dimensions():
    """
    Gets dimensions of a vessel from the user and returns them in feet.

    Parameters: None
    Returns:
        float: The vessel's length in feet.
        float: The vessel's width in feet.

    Examples:
    >>> get_vessel_dimensions()
    (32.8, 16.4)
    >>> get_vessel_dimensions()
    (24.6, 10.5)
    >>> get_vessel_dimensions()
    (49.2, 27.88)
    """
    length=float(input("Enter the vessel length (in meter): "))
    width=float(input("Enter the vessel width (in meter): "))
    return (meter_to_feet(length), meter_to_feet(width))

def get_valid_coordinate(val_name,min_float,max_float):
    """
    Gets a valid coordinate value within a specified range from the user.

    Parameters:
        val_name (str): The name of the coordinate value 
        min_float (float): The minimum allowable value for the coordinate.
        max_float (float): The maximum allowable value for the coordinate.
    Returns:
        float: The valid coordinate value entered by the user.

    Examples:
    >>> get_valid_coordinate("latitude", -90, 90)
    What is your latitude? 100
    Invalid latitude
    What is your latitude? -80
    -80.0
    >>> get_valid_coordinate("longitude", -180, 180)
    What is your longitude? 200
    Invalid longitude
    What is your longitude? -170
    -170.0
    >>> get_valid_coordinate("y-coordinate", 0, 100)
    What is your depth? 120
    Invalid depth
    What is your depth? 80
    80.0
    """
    #Prompt user for the coordinate value using the provided val_name
    coordinate=float(input("What is your "+str(val_name)+" ?"))

    #Loop until a valid coordinate within the specified range is entered
    while coordinate<min_float or coordinate>max_float:
        print("Invalid",val_name)
        coordinate=float(input("What is your "+str(val_name)+" ?"))

    #Return the valid coordinate value
    return coordinate

def get_gps_location():
    """
    Gets the GPS location coordinates of a vessel.
    
    Returns:
        float: The latitude coordinate of the vessel.
        float: The longitude coordinate of the vessel.

    Examples:
    >>> get_gps_location()
    What is your latitude? 40.7128
    What is your longitude? -74.0060
    40.7128
    -74.006
    >>> get_gps_location()
    What is your latitude? 45.0
    What is your longitude? 200
    Invalid longitude
    What is your longitude? -122.3321
    45.0
    -122.3321
    >>> get_gps_location()
    What is your latitude? -95
    Invalid latitude
    What is your latitude? 35.6895
    What is your longitude? 300
    Invalid longitude
    What is your longitude? 139.6917
    35.6895
    139.6917
    """
    #Gets latitude and longitude using the 'get_valid_coordinate' function
    latitude=get_valid_coordinate("latitude",MIN_LAT,MAX_LAT)
    longitude=get_valid_coordinate("longitude",MIN_LONG,MAX_LONG)

    #Returns the valid coordinates
    return (latitude, longitude)

def distance_two_points(lat1,long1,lat2,long2):
    """
    Calculates the distance between two points on a spherical surface
    such as that of the Earth using the Haversine formula.

    Parameters:
        lat1 (float): Latitude of the first location in degrees.
        long1 (float): Longitude of the first location in degrees.
        lat2 (float): Latitude of the second location in degrees.
        long2 (float): Longitude of the second location in degrees.
    Returns:
        float: The computed distance between the two locations in 
               kilometers, rounded to 2 decimal places.

    Examples:
    >>> distance_two_points(32.3964, -64.6829, 45.3346, -123.9531)
    5170.21
    >>> distance_two_points(-14.0326, 123.0907, -19.2441, 141.6055)
    2053.21
    >>> distance_two_points(57.8105, -5.8353, 41.3439, 9.0991)
    2126.63
    """
    #Convert latitude and longitude from degrees to radians
    LAT1=degrees_to_radians(lat1)
    LONG1=degrees_to_radians(long1)
    LAT2=degrees_to_radians(lat2)
    LONG2=degrees_to_radians(long2)
    
    #Calculate absolute differences in latitude and longitude
    DIFF_LAT=abs(LAT2-LAT1)
    DIFF_LONG=abs(LONG2-LONG1)
    
    #Compute Haversine formula components
    a=(math.sin(DIFF_LAT/2)**2)+math.cos(LAT1)*math.cos(LAT2)\
      *(math.sin(DIFF_LONG/2)**2)
    c=2*math.atan2(math.sqrt(a),math.sqrt(1-a))
    d=EARTH_RADIUS*c

    #Return the distance rounded to 2 decimal places
    return round(d,2)

def check_safety(lat,long):
    """
    Checks the safety status of the vessel's location based on
    its proximity to a restricted zone or a hazardous area.

    Parameters:
        lat (float): Latitude of the vessel in degrees.
        long (float): Longitude of the vessel in degrees.
    Returns: None.

    Examples:
    >>> check_safety(24, -70)
    Error: Restricted zone!
    >>> check_safety(40.5, -70.5)
    Warning: Hazardous area! Navigate with caution.
    >>> check_safety(45, -75)
    Safe navigation.
    """
    #Check if the vessel's location is within the restricted zone
    if distance_two_points(lat,long,RZONE_LAT,RZONE_LONG)<=RZONE_RADIUS:
        print("Error: Restricted zone!")

    #Check if the vessel's location is within the hazardous area
    elif (lat>=HAZARD_LAT_MIN and lat<=HAZARD_LAT_MAX) \
         and (long>=HAZARD_LONG_MIN and long<=HAZARD_LONG_MAX):
        print("Warning: Hazardous area! Navigate with caution.")
    else:
        #If the vessel's location is safe
        print("Safe navigation.")
        
def get_max_capacity(length,width):
    """
    Calculates the maximum number of adults a vessel can carry.

    Parameters:
        length (float): The length of the vessel in feet.
        width (float): The width of the vessel in feet.
    Returns:
        int: The maximum number of passengers the vessel can carry.

    Examples:
    >>> get_max_capacity(20, 8)
    10
    >>> get_max_capacity(30, 10)
    32
    >>> get_max_capacity(35, 12)
    55
    """
    if length<=26:
        capacity=length*(width/15)
    else:
        capacity=length*(width/15)+(length-26)*3
    return int(capacity)

def passengers_on_boat(length,width,num_passengers):
    """
    Checks if all passengers can fit on the boat with a balanced 
    seating arrangement where the passengers are distributed equally 
    across the four corners of the vessel. If this is not the case, the 
    function returns False.

    Parameters:
        length (float): The length of the vessel in feet.
        width (float): The width of the vessel in feet.
        num_passengers (int): The number of passengers to put on the vessel.
    Returns:
        bool: True if all passengers can fit properly, False otherwise.

    Examples:
    >>> passengers_on_boat(18, 6, 6)
    False
    >>> passengers_on_boat(20, 6, 8)
    True
    >>> passengers_on_boat(24, 8, 7)
    False
    """
    if get_max_capacity(length,width)>=num_passengers and num_passengers%4==0:
        return True
    return False

def update_coordinate(position,min_float,max_float):
    """
    Updates a coordinate position within a specified range.

    Parameters:
        position (float): The original position of the coordinate.
        min_float (float): The minimum value allowed for the coordinate.
        max_float (float): The maximum value allowed for the coordinate.
    Returns:
        float: The new valid position of the coordinate, rounded to 2 decimals.

    Examples:
    >>> update_coordinate(2.0, -5.0, 5.0)
    1.23
    >>> update_coordinate(-15.0, -20.0, -10.0)
    -17.56
    >>> update_coordinate(150.0, 100.0, 200.0)
    155.42
    """
    random.seed(123) #Setting the seed for autograder purposes
    #Generate a random addition between -10 and 10
    addition=random.random()*20-10
    new_position=position+addition

    #Calculate the new position by adding the random addition
    while new_position>=max_float or new_position<=min_float:
        addition=random.random()*20-10
        new_position=position+addition
    
    #Return the updated position rounded to 2 decimals
    return round(new_position,2)

def wave_hit_vessel(latitude,longitude):
    """
    Simulates a wave hitting the vessel based on a random number
    and reorienting its position. After updating the coordinates, 
    the function calls 'check_safety' to check the safety of the 
    new location.

    Parameters:
        lat (float): The latitude of the vessel.
        long (float): The longitude of the vessel.
    Returns:
        float: The new computed latitude coordinate.
        float: The new computed longitude coordinate.

    Examples:
    >>> wave_hit_vessel(40.0, -75.0)
    Safe navigation.
    (31.05, -83.95)
    >>> wave_hit_vessel(38.5, -72.0)
    Safe navigation.
    (29.55, -80.95)
    >>> wave_hit_vessel(49.42, -61.13)
    Warning: Hazardous area! Navigate with caution.
    (40.47, -70.08)
    """
    #Update latitude and longitude coordinates using 'update_coordinate'
    new_lat=update_coordinate(latitude,MIN_LAT,MAX_LAT)
    new_long=update_coordinate(longitude,MIN_LONG,MAX_LONG)
    #Check the safety of the new location
    check_safety(new_lat,new_long)
    #Return the new computed coordinates
    return (new_lat,new_long)

def vessel_menu():
    """
    Displays a menu for vessel management and execute user-selected actions.

    This function presents a menu to the user for managing vessel-related tasks. 
    It allows the user to perform actions such as checking the safety of the 
    boat, determining the maximum number of people it can hold, and updating 
    the boat's position. Each option is executed accordingly, and the menu 
    continues to be displayed until the user chooses to exit.

    Parameters: None
    Returns: None
    """
    # Welcome message and retrieval of initial vessel location and dimensions
    print("Welcome to the boat menu!")
    (latitude,longitude)=get_gps_location()
    print("Your current position is at latitude",latitude,"and longitude",longitude)
    (length,width)=get_vessel_dimensions()
    print("Your boat measures",length,"feet by",width,"feet")
    
    # Menu loop to continuously prompt the user until they choose to exit
    option=0
    while option!=4:
        print("Please select an option below: ")
        print("1. Check the safety of your boat")
        print("2. Check the maximum number of people that can fit on the boat")
        print("3. Update the position of your boat")
        print("4. Exit boat menu")
        option=int(input("Your selection: "))
        
        # Option 1: Check the safety of the boat
        if option==1:
            check_safety(latitude,longitude)
            
        # Option 2: Check the maximum number of people that can fit on the boat
        elif option==2:
            adults=int(input("How many adults go on the boat? "))
            if passengers_on_boat(length,width,adults)==True:
                print("Your boat can hold",adults,"adults")
            else:
                print("Your boat cannot hold",adults,"adults")
                
        # Option 3: Update the position of the boat
        elif option==3:
            (latitude,longitude)=wave_hit_vessel(latitude,longitude)
            print("Your new position is latitude of",latitude,"and longitude of",longitude)
    
    # Exiting the menu
    print("End of boat menu.")
    return None