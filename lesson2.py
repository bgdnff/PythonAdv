import csv

CSV_DATA = [
        ['header1', 'header2', 'header3', 'header4'],
        ['data1', 'data2', 'data3', 'data4'],
        ['data1', 'data2', 'data3', 'data4'],
        ['data1', 'data2', 'data3', 'data4'],
        ['data1', 'data2', 'data3', 'data4'],
        ['data1', 'data2', 'data3', 'data4'],
        ['data1', 'data2', 'data3', 'data4'],
        ['data1', 'data2', 'data3', 'data4'],
        ['data1', 'data2', 'data3', 'data4'],
    ]


def write_csv(data, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)

def read_csv(filename):
    with open(filename) as file:
        reader = csv.reader(file)
        return list(reader)


write_csv(CSV_DATA, 'data/csv_file.csv')
print(read_csv('data/csv_file.csv'))

# JSON_____________________________________________
import json
from pprint import pprint


JSON_DATA = {
    "president": {
        "name": "Zaphod Beeblebrox",
        "species": "Betelgeusian"
    }
}


def write_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


def read_json(filename):
    with open(filename) as file:
        return json.load(file)


write_json(JSON_DATA, 'data/json_file.json')
pprint(read_json('data/json_file.json'))

# YAML_____________________________________


import yaml


YAML_DATA = {
    'attr1': 'value1',
    'attr2': 'value2',
    'attr3': 'value3',
    'attr4': ['value1', 'value2', 'value3'],
}


def write_yaml(data, filename):
    with open(filename, 'w') as file:
        yaml.dump(data, file, Dumper=yaml.Dumper)


def read_yaml(filename):
    with open(filename) as file:
        return yaml.load(file, Loader=yaml.Loader)


write_yaml(YAML_DATA, 'data/yaml_file.yml')
pprint(read_yaml('data/yaml_file.yml'))


def read_csv_dict(filename):
    data = read_csv(filename)
    my_list = []
    fieldnames = data[0]
    for values in data[1:]:
        inner_dict = dict(zip(fieldnames, values))
        my_list.append(inner_dict)
    return my_list


def csv2json(filename_csv, filename_json):
    write_json(read_csv_dict(filename_csv), filename_json)


def csv2yaml(filename_csv, filename_yaml):
    write_yaml(read_csv_dict(filename_csv), filename_yaml)


def json2yaml(filename_json, filename_yaml):
    write_yaml(read_json(filename_json), filename_yaml)


csv2json('data/csv_file.csv', 'data/csv.json')
csv2yaml('data/csv_file.csv', 'data/csv.yaml')
json2yaml('data/json_file.json', 'data/json.yml')
