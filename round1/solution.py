import re
from tkinter import Tk, StringVar, Label, Entry, Text, END, Button
# TODO: FOR TESSTING PURPOSES
import time
from data import (merged as merged,
  suspicious as suspicious,
  central as central,
  search as search)

window = Tk()

instruction=StringVar()
instruction.set("Keresett autó rendszámtáblája:")
instruction_element=Label(window, textvariable = instruction)
instruction_element.grid(row = 0, column = 0)

license_plate=StringVar(None)
license_plate_element=Entry(window,textvariable = license_plate,width = 16)
license_plate_element.grid(row = 1, column = 0)

buttonText="Keresés"
button=Button(window, text = buttonText, command = lambda: main(license_plate))
button.grid(row = 1, column = 1)

result=Text(window, height = 32, width = 32)
result.grid(row = 2, column = 0, columnspan = 2)

def main(license_plate):
  if not re.match("[A-Z]{3}[-][0-9]{3}", license_plate.get()):
    instruction.set("Elfogadott rendszámtábla formátuma:\"AAA-000\"\n")
  else:
    license_plate = license_plate.get()
    query_result = find_database(license_plate)
    array = get_array(query_result[0])
    if query_result[1] == True:
      array = check_central(array)
    if len(array) == 2:
      log_text = get_log_text(array)
      print_and_write(log_text)
    else:
      array = get_wheels_data(array)
      log_text = get_log_text(array)
      print_and_write(log_text)

def find_database(license_plate):
  print(license_plate)
  is_suspicious = False
  query_result = search(license_plate, merged)
  print(query_result)
  if query_result.empty:
    query_result = search(license_plate, suspicious)
    if query_result.empty:
      query_result = [license_plate, "Nem vásárló"]
      return [query_result, is_suspicious]
    else:
      is_suspicious = True
      return [query_result, is_suspicious]
  else:
    return [query_result, is_suspicious]

def get_array(query_result):
  array = []
  if len(query_result) == 2:
    array = query_result
  else:
    for index, row in query_result.iterrows():
      for i in row:
        array.append(i)
    if array[3] == "Lopott":
      array[3] = "Riasztás"
  return array

def check_central(array):
  # TODO: FOR TESSTING PURPOSES
  start = time.time()
  central_query_result = search(array[0], central)
  # TODO: FOR TESSTING PURPOSES
  end = time.time()
  print(end - start)
  central_result = get_array(central_query_result)
  owner = ""
  car_type = ""
  if array[1] != central_result[1]:
    owner = "Rossz sofőr"
  if array[2] != central_result[2]:
    car_type = "Rossz autómárka"
  if owner != "":
    array.append(owner)
  if car_type != "":
    array.append(car_type)
  array[3] = "Gyanús"
  return array

def get_wheels_data(data):
  front = equalize_pressure([data[4], data[5]])
  rear = equalize_pressure([data[6], data[7]])
  get_wheels_data = []
  for i in front:
    get_wheels_data.append(i)
  for i in rear:
    get_wheels_data.append(i)
  i = 3
  while i < 7:
    i += 1
    data[i] = get_wheels_data[i - 4]
  return data

def equalize_pressure(data):
  left = data[0]
  right = data[1]
  average = (left + right) / 2
  if average < 1.5 or average > 3:
    left = 2.25 - left
    right = 2.25 - right
  elif left != right:
    left = average - left
    right = average - right
  else:
    left = right = "Nem igényelt munkát"
    return left, right
  return "{0:.2f}".format(left), "{0:.2f}".format(right)

def get_log_text(data):
  if len(data) == 2:
    log_text = f"\n\n{data[0]} - {data[1]}"
  elif len(data) > 1:
    log_text = f"\n\n{data[0]}, {data[1]}:\n\
    Kerekek állapota:\n\
        Bal első: {data[4]}\n\
        Jobb első: {data[5]}\n\
        Bal hátsó: {data[6]}\n\
        Jobb hátsó: {data[7]}\n\
    Autó jogi státusza:\n\
        {data[3]}"
    if len(data) == 9:
      log_text += f"\n\
        {data[8]}"
    elif len(data) == 10:
      log_text += f"\n\
        {data[8]}\n\
        {data[9]}"
  return log_text

def print_and_write(log_text):
  print(log_text, file = open("log.txt", "a+"))
  result.insert(END, log_text)

window.mainloop()
