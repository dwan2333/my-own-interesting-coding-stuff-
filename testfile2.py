class Car: 
    def __init__(self, make, model, year): 
        """Initialize attributes to describe a car.""" 
        self.make = make 
        self.model = model 
        self.year = year 
        self.odometer_reading = 0 

    def get_descriptive_name(self):
        title = f'{self.make} {self.model} {self.year}'
        return(title.title())

    def read_odometer(self): 
        """Print a statement showing the car's mileage.""" 
        return(f"This car has {self.odometer_reading} miles on it.") 

my_new_car = Car('audi', 'a4', 2024) 
my_new_car.odometer_reading = 500
print(my_new_car.get_descriptive_name()) 
print(my_new_car.read_odometer())

