

#Easy script for getting historical data and looping through it to fill a series of data points from a starting date until an ending date of choice
#Refer to the documentation here from microsoft for specific parameters for query: https://learn.microsoft.com/en-us/rest/api/maps/weather/get-daily-historical-records?view=rest-maps-2024-04-01&tabs=HTTP

df = pd.read_csv("list_of_latitudes_and_longitudes.csv", index_col=False)
df = df.drop_duplicates()

megaarray = []

enddateofchoice = ?
startdateofchoice = ?

def get_forecast(row):
    #This gets the property value from the second property name, which is necessarily battery charge
    #Gets location
    startDate = datetime.strptime(startdateofchoice, "%Y-%m-%d")
    endDate = (startDate + timedelta(days=30)).date()
    #Presumably this is your latitude and longitude column in the format "39.952583,-75.165222"
    if row["latlong"] != "":
        print(f"Now on location: {row["latlong"]}")
        latlong = str(row["combine_latlong"])
        #Get subscription key to Azure maps account
        api_key = os.environ.get('subscription_key_azure')
        while pd.to_datetime(endDate)<pd.to_datetime(enddateofchoice):
            startDate = startDate.strftime("%Y-%m-%d")
            endDate = endDate.strftime("%Y-%m-%d")
            #If you'd like you can change the unit from imperial to metric
            response = requests.get(f'https://atlas.microsoft.com/weather/historical/records/daily/json?api-version=1.1&query={latlong}&startDate={str(startDate)}&endDate={str(endDate)}&unit=imperial&subscription-key={api_key}')
            json_response = response.json()
            #Uncomment this to debug/see what is happening
            #print(json.dumps(json_response, indent=4, sort_keys=True))
            if response.status_code == 200:
                day_array = []
                temp_array = []
                query_location_array = []
                query_location = row['combine_latlong']
                # Parse the JSON response
                #Here we are just getting temperature lows for the day, but you could select anything you want (or multiple dfferent items) 
                for sub_json in json_response["results"]:
                    if "minimum" in sub_json["temperature"]:
                        day = sub_json["date"]
                        temperature_low = sub_json["temperature"]["minimum"]["value"]
                        day_array.append(day)
                        temp_array.append(temperature_low)
                        query_location_array.append(query_location)
                dataframe = pd.DataFrame({
                    'lat_long': query_location_array,
                    'day': day_array,
                    'temperature': temp_array
                })
                megaarray.append(dataframe)
            #Need to parse between types to use the variable and change it (as datetime) and to use it in the query (as string)
            startDate = datetime.strptime(startDate, "%Y-%m-%d")
            startDate = startDate + timedelta(days=30)
            endDate = datetime.strptime(endDate, "%Y-%m-%d")
            endDate = (startDate + timedelta(days=30)).date()


df = df.apply(get_forecast, axis=1)
df = pd.concat(megaarray, ignore_index=True)
df.to_csv("finished_lows.csv")
print(df.head(5))









