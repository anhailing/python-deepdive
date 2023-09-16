import numbers
from datetime import timedelta
import itertools

class Account:

    interest_rate: float = 0.005
    transaction_counter = itertools.count(100)

    def __init__(self, account_number: int, first_name: str, last_name: str,
                timezone: TimeZone | None = None,  initial_balance: float = 0):
        self._account_number = account_number
        self.first_name = first_name
        self.last_name = last_name
        if timezone is None:
            timezone = TimeZone('UTC', 0, 0)
        self.timezone = timezone
        self._balance = initial_balance


    @property
    def account_number(self):
        return self._account_number
    
    @property
    def first_name(self):
        return self._first_name
    
    @first_name.setter
    def first_name(self, value):
        self._first_name = self.validate_name(value, "First name")

    @property
    def last_name(self):
        return self._last_name
    
    @last_name.setter
    def last_name(self, value):
        self._last_name = self.validate_name(value, "Last name")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def balance(self):
        return self._balance
    
    @property
    def timezone(self):
        return self._timezone
    
    @timezone.setter
    def timezone(self, value):
        if not isinstance(value, TimeZone):
            raise ValueError("Timezone must be a valid TimeZone object")
        self._timezone = value
        
   

    @staticmethod
    def validate_name(value, field_title):
        if not isinstance(value, str):
            raise TypeError(f"{field_title} must be a string")
        if len(value.strip()) == 0:
            raise ValueError(f"{field_title} cannot be empty")
        return value.strip()
    
    def withdraw(self, amount):
        self.balance = self.balance - amount
        transaction_id = next(Account.transaction_counter)
        return transaction_id
    
    def deposit(self, amount):
        self.balance = self.balance + amount 
        transaction_id = next(Account.transaction_counter)
        return transaction_id
    
    # @property
    # def balance(self):
    #     return self.balance + self.calculate_interest()

    def pay_interest(self):
        return self.balance * Account.monthly_interest_rate
    
    def parse_confirmation_code():
        ...

    
    # def commit(self):
    #     """ 
    #     - the account number, transaction code (D, W, etc), datetime (UTC format), date time (in whatever timezone is specified in te argument, but more human readable), the transaction ID
    #     - make it so it is a nicely structured object (so can use dotted notation to access these three attributes)
    #     - I purposefully made it so the desired timezone is passed as an argument. Can you figure out why? (hint: does this method require any information from any instance?)
    #     """


class TimeZone:
    def __init__(self, name, offset_hours, offset_minutes):
        if name is None or len(str(name).strip()) == 0:
            raise ValueError('Timezone name cannot be empty.')
            
        self._name = str(name).strip()
        
        if not isinstance(offset_hours, numbers.Integral):
            raise ValueError('Hour offset must be an integer.')
        
        if not isinstance(offset_minutes, numbers.Integral):
            raise ValueError('Minutes offset must be an integer.')
            
        if offset_minutes < -59 or offset_minutes > 59:
            raise ValueError('Minutes offset must between -59 and 59 (inclusive).')
            
        # for time delta sign of minutes will be set to sign of hours
        offset = timedelta(hours=offset_hours, minutes=offset_minutes)

        # offsets are technically bounded between -12:00 and 14:00
        # see: https://en.wikipedia.org/wiki/List_of_UTC_time_offsets
        if offset < timedelta(hours=-12, minutes=0) or offset > timedelta(hours=14, minutes=0):
            raise ValueError('Offset must be between -12:00 and +14:00.')
            
        self._offset_hours = offset_hours
        self._offset_minutes = offset_minutes
        self._offset = offset
        
    @property
    def offset(self):
        return self._offset
    
    @property
    def name(self):
        return self._name
    
    def __eq__(self, other):
        return (isinstance(other, TimeZone) and 
                self.name == other.name and 
                self._offset_hours == other._offset_hours and
                self._offset_minutes == other._offset_minutes)
    def __repr__(self):
        return (f"TimeZone(name='{self.name}', "
                f"offset_hours={self._offset_hours}, "
                f"offset_minutes={self._offset_minutes})")