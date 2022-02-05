import unittest
import mysql.connector


class DataIntegrity(unittest.TestCase):
    def setUp(self):
        self.__db = mysql.connector.connect(
            host="practicum1.c5r3vp6fuc73.us-east-2.rds.amazonaws.com",
            user="practicum1",
            passwd="practicum1",
            database="practicum1"
        )
        self.__cursor = self.__db.cursor()

    def test_airport_desc_table(self):
        self.__cursor.execute("SELECT * FROM AirportDesc")        
        airport_desc = self.__cursor.fetchall()

        origin_states = [desc[1] for desc in airport_desc]

        self.assertEqual(len(airport_desc), 61)
        self.assertEqual(len(set(origin_states)), len(airport_desc))

    def test_airport_table(self):
        self.__cursor.execute("SELECT * FROM Airport")
        airport_data = self.__cursor.fetchall()

        airport_state_ids = [data[1] for data in airport_data]
        airport_names = [data[2] for data in airport_data]

        self.assertEqual(len(airport_data), 1109)
        self.assertEqual(len(set(airport_state_ids)), 61)
        self.assertEqual(len(set(airport_names)), len(airport_data))

    def test_aircraft_desc_table(self):
        self.__cursor.execute("SELECT * FROM AircraftDesc")
        aircraft_desc = self.__cursor.fetchall()

        aircraft_num_engines = [desc[1] for desc in aircraft_desc]
        allowed_num_engines = ["1", "2", "3", "4", "", "C"]

        self.assertEqual(len(aircraft_desc), 6)
        self.assertEqual(len(set(aircraft_num_engines)), len(aircraft_desc))
        self.assertEqual(sorted(aircraft_num_engines), sorted(allowed_num_engines))

    def test_aircraft_table(self):
        self.__cursor.execute("SELECT * FROM Aircraft")
        aircraft_data = self.__cursor.fetchall()

        aircraft_desc_ids = [data[1] for data in aircraft_data]
        aircraft_type = [data[2] for data in aircraft_data]
        aircraft_is_large = [data[-1] for data in aircraft_data]

        self.assertEqual(len(aircraft_data), 1376)
        self.assertEqual(len(set(aircraft_desc_ids)), 6)
        self.assertEqual(list(set(aircraft_type))[0], "Airplane")
        self.assertEqual(len(set(aircraft_is_large)), 2)
        self.assertEqual(sorted(list(set(aircraft_is_large))), ["No", "Yes"])

    def test_flight_altitude_table(self):
        self.__cursor.execute("SELECT * FROM FlightAltitude")
        flight_altitude = self.__cursor.fetchall()

        flight_altitude_bin = [data[2] for data in flight_altitude]

        self.assertEqual(len(flight_altitude), 257)
        self.assertEqual(len(set(flight_altitude_bin)), 2)
        self.assertEqual(sorted(list(set(flight_altitude_bin))), ['< 1000 ft', '> 1000 ft'])

    def test_wildlife_desc_table(self):
        self.__cursor.execute("SELECT * FROM WildlifeDesc")
        wildlife_desc = self.__cursor.fetchall()

        wildlife_size = [data[1] for data in wildlife_desc]

        self.assertEqual(len(wildlife_desc), 3)
        self.assertEqual(len(set(wildlife_size)), len(wildlife_desc))
        self.assertEqual(sorted(wildlife_size), sorted(['Small', 'Medium', 'Large']))

    def test_wildlife_table(self):
        self.__cursor.execute("SELECT * FROM Wildlife")
        wildlife_data = self.__cursor.fetchall()

        wildlife_desc_ids = [data[1] for data in wildlife_data]
        species = [data[-1] for data in wildlife_data]

        self.assertEqual(len(wildlife_data), 363)
        self.assertEqual(len(set(wildlife_desc_ids)), 3)
        self.assertEqual(sorted(list(set(wildlife_desc_ids))), [1, 2, 3])
        self.assertEqual(len(set(species)), 345)

    def test_record_details_table(self):
        self.__cursor.execute("SELECT * FROM RecordDetails")
        record_details = self.__cursor.fetchall()

        wildlife_struck = list(set([data[1] for data in record_details]))

        self.assertEqual(len(record_details), 106)
        self.assertEqual(len(wildlife_struck), 4)
        self.assertEqual(sorted(wildlife_struck), sorted(['2 to 10', 'Over 100', '1', '11 to 100']))

        for record_detail in record_details:
            if record_detail[1] == '1':
                self.assertEqual(record_detail[0], 1)
            elif record_detail[1] == '2 to 10':
                self.assertTrue(record_detail[0] >= 2 and record_detail[0] < 11)
            elif record_detail[1] == '11 to 100':
                self.assertTrue(record_detail[0] >= 11 and record_detail[0] < 101)
            elif record_detail[1] == 'Over 100':
                self.assertTrue(record_detail[0] > 100)

    def test_records_table(self):
        self.__cursor.execute("SELECT * FROM Records")
        records = self.__cursor.fetchall()

        wildlife_ids = set([data[1] for data in records])
        wildlife_struck_actual = set([data[2] for data in records])

        self.assertEqual(len(records), 25428)
        self.assertEqual(len(set(wildlife_ids)), 363)
        self.assertEqual(len(set(wildlife_struck_actual)), 105)

    def test_flight_table(self):
        self.__cursor.execute("SELECT * FROM Flight")
        flight_data = self.__cursor.fetchall()

        aircraft_ids = set([data[1] for data in flight_data])
        airport_ids = set([data[2] for data in flight_data])
        altitude_ids = set([data[3] for data in flight_data])
        record_ids = set([data[4] for data in flight_data])
        sky_conditions = set([data[5] for data in flight_data])
        phase_of_flight = set([data[6] for data in flight_data])

        expected_phase_of_flight = ['Climb', 'Landing Roll', 'Approach', 'Take-off run', 'Descent',
       'Taxi', 'Parked']

        self.assertEqual(len(flight_data), 25428)
        self.assertEqual(len(aircraft_ids), 1376)
        self.assertEqual(len(airport_ids), 1109)
        self.assertEqual(len(altitude_ids), 257)
        self.assertEqual(len(record_ids), 25428)
        self.assertEqual(len(sky_conditions), 3)
        self.assertEqual(sorted(list(sky_conditions)), sorted(['No Cloud', 'Some Cloud', 'Overcast']))
        self.assertEqual(len(phase_of_flight), len(expected_phase_of_flight))
        self.assertEqual(sorted(list(phase_of_flight)), sorted(expected_phase_of_flight))

    def test_precipitation_table(self):
        self.__cursor.execute("SELECT * FROM Precipitation")
        precipitation = self.__cursor.fetchall()

        flight_ids = set([data[1] for data in precipitation])
        type = set([data[2] for data in precipitation])
        
        expected_type = ['Rain', 'Snow', 'Fog', 'None']

        self.assertEqual(len(precipitation), 25529)
        self.assertEqual(len(flight_ids), 25428)
        self.assertEqual(len(type), len(expected_type))
        self.assertEqual(sorted(list(type)), sorted(expected_type))