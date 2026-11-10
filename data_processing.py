import csv
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))
)

class DataLoader:
    """Class responsible for loading data from external files."""
    
    @staticmethod
    def load_csv(filepath):
        """Loads a CSV file and returns a list of dictionaries."""
        data = []
        with open(filepath, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(dict(row))
        return data


class Table:
    """Class representing a data table with filtering and aggregation operations."""

    def __init__(self, table_name, dict_list):
        self.table_name = table_name
        self.dict_list = dict_list

    def filter(self, condition):
        """
        Returns a new Table containing only items where condition(item) is True.
        Returning a Table instance enables method chaining.
        """
        filtered_data = [item for item in self.dict_list if condition(item)]
        return Table(self.table_name, filtered_data)

    def aggregate(self, aggregation_key, aggregation_function):
        """
        Extracts values for aggregation_key, casts numerical values,
        and applies aggregation_function.
        """
        values = [float(item[aggregation_key]) for item in self.dict_list]
        return aggregation_function(values)

    def __str__(self):
        return f"Table('{self.table_name}', {len(self.dict_list)} rows)"


cities_data = DataLoader.load_csv(os.path.join(__location__, 'Cities.csv'))
cities_table = Table("Cities", cities_data)

# Print the average temperature of all the cities
avg_all = cities_table.aggregate('temperature', lambda temps: sum(temps) / len(temps))
print(f"Average temperature of all cities: {avg_all:.2f}°C")

# Print all cities in Germany
germany_table = cities_table.filter(lambda c: c['country'] == 'Germany')
germany_city_names = [c['city'] for c in germany_table.dict_list]
print(f"\nCities in Germany ({len(germany_city_names)}): {germany_city_names}")

# Print all cities in Spain with temperature above 12°C
spain_warm_table = cities_table.filter(
    lambda c: c['country'] == 'Spain' and float(c['temperature']) > 12
)
spain_warm_cities = [c['city'] for c in spain_warm_table.dict_list]
print(f"\nCities in Spain with temp > 12°C ({len(spain_warm_cities)}): {spain_warm_cities}")

# Count the number of unique countries
unique_countries = len(set(c['country'] for c in cities_table.dict_list))
print(f"\nNumber of unique countries: {unique_countries}")

# Print the average temperature for all the cities in Germany (using method chaining)
avg_germany = cities_table.filter(lambda c: c['country'] == 'Germany') \
                          .aggregate('temperature', lambda temps: sum(temps) / len(temps))
print(f"\nAverage temperature in Germany: {avg_germany:.2f}°C")

# Print the max temperature for all the cities in Italy (using method chaining)
max_italy = cities_table.filter(lambda c: c['country'] == 'Italy') \
                        .aggregate('temperature', max)
print(f"Max temperature in Italy: {max_italy:.2f}°C")