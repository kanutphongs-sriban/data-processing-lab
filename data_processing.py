import csv
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))
)

cities = []
with open(os.path.join(__location__, 'Cities.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        cities.append(dict(r))

def filter_items(condition, dict_list):
    """Return a new list containing only dictionaries that satisfy condition(item)."""
    return [item for item in dict_list if condition(item)]

def aggregate(aggregation_key, aggregation_function, dict_list):
    """Aggregate numeric values of aggregation_key using aggregation_function."""
    values = [float(item[aggregation_key]) for item in dict_list]
    return aggregation_function(values)


# Average temperature of all cities
avg_all = aggregate('temperature', lambda vals: sum(vals) / len(vals), cities)
print(f"Average temperature of all cities: {avg_all:.2f}°C")

# Print all cities in Germany
germany_cities = filter_items(lambda c: c['country'] == 'Germany', cities)
print("\nCities in Germany:", [c['city'] for c in germany_cities])

# Print all cities in Spain with temp more than 12°C
spain_warm = filter_items(lambda c: c['country'] == 'Spain' and float(c['temperature']) > 12, cities)
print("\nCities in Spain with temp more than 12°C:", [c['city'] for c in spain_warm])

# Count unique countries
unique_countries = len(set(c['country'] for c in cities))
print(f"\nNumber of unique countries: {unique_countries}")

# Average temperature for cities in Germany
avg_germany = aggregate('temperature', lambda vals: sum(vals) / len(vals), germany_cities)
print(f"\nAverage temperature in Germany: {avg_germany:.2f}°C")

# Max temperature for cities in Italy
italy_cities = filter_items(lambda c: c['country'] == 'Italy', cities)
max_italy = aggregate('temperature', max, italy_cities)
print(f"\nMax temperature in Italy: {max_italy}°C")