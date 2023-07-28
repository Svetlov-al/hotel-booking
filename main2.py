import pandas as pd
from abc import ABC, abstractmethod

df = pd.read_csv('hotels.csv', dtype={'id': str})


class Hotel:
    watermark = 'Real Hotel'

    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df['id'] == self.hotel_id, 'name'].squeeze()
        self.city = df.loc[df['id'] == self.hotel_id, 'city'].squeeze()

    def book(self):
        """Books a hotel by changing its availability to 'no'"""
        df.loc[df['id'] == self.hotel_id, 'available'] = 'no'
        df.to_csv('hotels.csv', index=False)

    def available(self):
        """Check if the hotel is available"""
        availability = df.loc[df['id'] == self.hotel_id, 'available'].squeeze()
        print(availability)
        if availability == 'yes':
            return True
        else:
            return False

    @classmethod
    def get_hotel_count(cls, data):
        return len(data)


class Ticket(ABC):

    @abstractmethod
    def generate(self):
        pass


class ReservationTicket(Ticket):
    def __init__(self, customer_name, hotel_object):
        self.customer = customer_name
        self.hotel = hotel_object

    def generate(self):
        content = f"""
        Thank you for your reservation
        Here are your booking data: 
        Name : {self.the_customer_name}
        Hotel name: {self.hotel.name}
        City: {self.hotel.city}"""
        return content

    @property
    def the_customer_name(self):
        name = self.customer.strip()
        name = name.title()
        return name

    @staticmethod
    def convert(amount):
        return amount * 1.2

    def __eq__(self, other):
        if self.hotel == other.hotel:
            return True
        else:
            return False


hotel1 = Hotel(hotel_id='134')
hotel2 = Hotel(hotel_id='188')

print(hotel1.available())

print(hotel1.name)
print(hotel2.name)

print(Hotel.watermark)
print(hotel1.watermark)

print(Hotel.get_hotel_count(data=df))
print(hotel1.get_hotel_count(data=df))


ticket = ReservationTicket('john smith ', hotel1)

print(ticket.the_customer_name)
print(ticket.generate())

converted = ReservationTicket.convert(10)

converted_ticket = ticket.convert(20)

print(converted)
