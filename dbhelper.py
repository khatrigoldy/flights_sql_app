import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()  # loads .env from current directory



class DB:
    def __init__(self):
        #connect to the database
        try:

            self.conn = mysql.connector.connect(
                                        user = os.getenv("DB_USER"),
                                        password = os.getenv("DB_PASSWORD"),
                                        host = os.getenv("DB_HOST"),
                                        db = os.getenv("DB_NAME")
                                                        )
            self.mycursor = self.conn.cursor()
            print("connection established")
        except:
            print("connection error")

    def fetch_city_name(self):
        city=[]
        self.mycursor.execute("""
        SELECT DISTINCT(Destination) FROM flights.flights
        UNION
        SELECT DISTINCT(Source) FROM flights.flights
        """)

        data = self.mycursor.fetchall()

        for item in data:
            city.append(item[0])

        return city

    def fetch_all_flights(self,source,destination):

        self.mycursor.execute("""
        SELECT Airline, Route, Dep_Time, Duration,Price FROM flights
        WHERE Source = '{}' AND Destination = '{}'
        """.format(source,destination))
        data = self.mycursor.fetchall()

        return data

    def fetch_airline_frequency(self):

        airline = []
        frequency =[]
        self.mycursor.execute("""
        SELECT Airline , Count(*) FROM flights
        GROUP BY Airline""")

        data = self.mycursor.fetchall()

        for item in data:
            airline.append(item[0])
            frequency.append([item[1]])
        return airline,frequency

    def busy_airport(self):

        city = []
        frequency = []
        self.mycursor.execute("""
        SELECT source, count(*) FROM ( SELECT source FROM flights
        UNION ALL 
        SELECT Destination FROM flights) t
        GROUP BY t.source
        ORDER BY COUNT(*) DESC""")

        data = self.mycursor.fetchall()

        for item in data:
            city.append(item[0])
            frequency.append([item[1]])
        return city, frequency


    def daily_frequency(self):

        date = []
        frequency = []
        self.mycursor.execute("""
        SELECT Date_of_Journey, count(*) FROM flights
        GROUP BY Date_of_Journey""")

        data = self.mycursor.fetchall()

        for item in data:
            date.append(item[0])
            frequency.append([item[1]])
        return date, frequency