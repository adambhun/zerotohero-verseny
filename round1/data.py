import csv
import pandas
import re
import string

central_data = pandas.read_csv("central_data.csv", sep = ";", header = 0)
clients_data = pandas.read_csv("clients.csv", sep = ";", header = 0)

merged_data = pandas.merge(central_data, clients_data)

suspicious_data = pandas.merge(clients_data, merged_data, how = "outer", indicator = True)
suspicious_data = suspicious_data[suspicious_data._merge == "left_only"]
suspicious_data.drop(["_merge"], axis = 1, inplace = True)

trimmed_central_data = pandas.merge(central_data, merged_data, how = "outer", indicator = True)
trimmed_central_data.drop(["Bal első kerék nyomása", "Jobb első kerék nyomása", "Bal hátsó kerék nyomása", "Jobb hátsó kerék nyomása"], axis = 1, inplace = True)
trimmed_central_data = trimmed_central_data[trimmed_central_data._merge == "left_only"]
trimmed_central_data.drop(["_merge"], axis = 1, inplace = True)

def condition(cell, character):
  if re.match("[%c]{1}[A-Z]{2}[-][0-9]{3}" %character, cell):
    return True
  else:
    return False

def get_dictionary(dataframe, is_central):
  alphabet = list(string.ascii_uppercase)
  dictionary = {}
  columns = ["Rendszám", "Tulaj", "Típus", "Lopottnak jelentve", "Bal első kerék nyomása", "Jobb első kerék nyomása", "Bal hátsó kerék nyomása", "Jobb hátsó kerék nyomása"]
  if is_central:
    columns = ["Rendszám", "Tulaj", "Típus", "Lopottnak jelentve"]
  for i in alphabet:
    dictionary[i] = dataframe [ dataframe.Rendszám.apply(func = condition, args = i)]
    dictionary[i] = pandas.DataFrame(dictionary[i], columns = columns)
    dictionary[i].sort_values(by = ["Lopottnak jelentve"], inplace = True, ascending = False)
  return dictionary

merged = get_dictionary(merged_data, False)
suspicious = get_dictionary(suspicious_data, False)
central = get_dictionary(trimmed_central_data, True)

def search(license_plate, database):
  dataframe = database[license_plate[0]]
  return dataframe.loc[dataframe.Rendszám == license_plate]

# TODO: FOR TESTING PURPOSES
merged_data.to_csv("merged.csv", index = False)
suspicious_data.to_csv("suspicious.csv", index = False)
trimmed_central_data.to_csv("trimmed.csv", index = False)
