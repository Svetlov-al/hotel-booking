import pandas as pd

df = pd.read_csv('hotels.csv', dtype={'id': str})
df_card = pd.read_csv('cards.csv', dtype=str).to_dict(orient='records')
df_card_security = pd.read_csv('card_security.csv', dtype=str)


class Hotel:
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


class SpaHotel(Hotel):
    def book_spa_package(self):
        pass


class ReservationTicket:
    def __init__(self, customer_name, hotel_object):
        self.customer = customer_name
        self.hotel = hotel_object

    def generate(self):
        content = f"""
        Thank you for your reservation
        Here are your booking data: 
        Name : {self.customer}
        Hotel name: {self.hotel.name}
        City: {self.hotel.city}"""
        return content


class CreditCard:
    def __init__(self, number):
        self.number = number

    def validate(self, expiration, holder, cvc):
        card_data = {'number': self.number,
                     "expiration": expiration,
                     'cvc': cvc,
                     'holder': holder,
                     }
        if card_data in df_card:
            return True
        else:
            return False


class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        user_password = df_card_security.loc[df_card_security['number'] == self.number, 'password'].squeeze()
        if user_password == given_password:
            return True
        else:
            return False


class SpaReservationTicket:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate(self):
        content = f"""
        Thank you for your SPA reservation!
        Here are your SPA booking data: 
        Name : {self.customer_name}
        Hotel name: {self.hotel.name}
        City: {self.hotel.city}"""
        return content


print(df)

hotel_iD = input('Enter id of the Hotel: ')

hotel = SpaHotel(hotel_iD)

if hotel.available():

    credit_card = SecureCreditCard(number='1234567890123456')

    if credit_card.validate(expiration='12/26', holder='JOHN SMITH', cvc='123'):
        password = input('Enter your password: ')
        if credit_card.authenticate(given_password=password):
            hotel.book()
            name = input("Enter your name: ")
            reservation_ticket = ReservationTicket(name, hotel)
            print(reservation_ticket.generate())

            spa = input('Would you like to order spa pocket? ')
            if spa == 'yes':
                hotel.book_spa_package()
                reservation_spa = SpaReservationTicket(name, hotel)
                print(reservation_spa.generate())
            else:
                print('Ok! No problem! Have a nice day!')
        else:
            print('Credit card authentication failed')
    else:
        print('There is a problem with your card.')
else:
    print('Hotel is not free.')
