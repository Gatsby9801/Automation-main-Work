import random
import string

#Server to run tests
server = "uat"
base_url = "https://"+server+".fleetpanda.com" #dont change
client_url = "https://client."+server+".fleetpanda.com/customers" #dont change

#Tenant
tenant = "Tootopia"
slugname = "TOO"

#Web login
dispatcher_number = "9745697713"
dispatcher_password = "password"

#Mobile login
driver_number = "9998887775"
driver_password = "changeme" #dont change

#driver name
motorist = "Automation Driver"

#Driver data
driver_name = ''.join(random.choices(string.ascii_letters, k=10))
erp_id = str(random.randint(1, 99999))
random_part = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
email = random_part + "@example.com"
driver_number = ''.join(random.choice(string.digits[2:]) for _ in range(10))
asset_name = random.choice(string.ascii_letters.replace('A', '') + string.ascii_letters) + ''.join(random.choices(string.ascii_letters, k=9))
unique_id = str(random.randint(1, 99999))

#unassigned status
