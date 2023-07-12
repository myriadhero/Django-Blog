import json
def validate(filename):
    with open(filename) as file:
        try:
            json_parsed = json.load(file)
            print("parsed")
            return json_parsed
        except json.decoder.JSONDecodeError:
            print("Invalid JSON") # in case json is invalid
        else:
            print("Valid JSON") # in case json is valid
        finally:
            print("closing")

file_name = "/home/kirill/raw-data-2023-07-04.json"

validate(file_name)
