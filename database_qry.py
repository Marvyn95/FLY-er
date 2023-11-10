import mysql.connector

def database_sync(site_data = None):
    """
    site_data: dictionary argument containing location data
    decription: receives dictionary argument within location data, and returns a list of tuples
    with sorrounding airfield location data
    """    
    print("querying database for airfields available")
    
    #checking input parameter
    if site_data is None:
        return {"Error": "Please enter valid argument"}
        
    #connecting to database server
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Romans116.",
        database="flyer"
    )
    #checking database connection status
    if not conn.is_connected:
        return {"ERROR": "Database connection failed, Try again"}
    
    crs = conn.cursor()
    
    print("getting convenient airfelds within district")
    
    #querying for airfield data from data base for airfields within location district
    query = "SELECT Airfield_name, Town, Latitude, Longitude, District_name, ICAO, IATA FROM airfield_data JOIN district_data on airfield_data.District_id = district_data.District_id WHERE District_name = %s"
    crs.execute(query, (site_data["District"],))
    
    #checking if theres any within district
    Available_airfields = []
    for line in crs:
            Available_airfields.append(line)
    
    if len(Available_airfields) != 0:
        conn.close()
        return Available_airfields
    
    
    elif len(Available_airfields) == 0:
        print("getting convenient airfields within region")
        #querying for airfield data from database for airfields within location region
        query = "SELECT Airfield_name, Town, Latitude, Longitude, Region_name, ICAO, IATA FROM airfield_data JOIN region_data on airfield_data.Region_id = region_data.Region_id WHERE Region_name = %s"
        crs.execute(query, (site_data["Region"],))
        
        #checking if theres any airfields in region
        for line in crs:
            Available_airfields.append(line)
        if len(Available_airfields) != 0:
            conn.close()
            return Available_airfields
        conn.close()   
        return None