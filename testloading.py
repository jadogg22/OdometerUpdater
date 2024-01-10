from time import sleep
from random import randint
from alive_progress import alive_bar

# Simulate equipment data
equipment_data = list(range(50))

def update_equipment(truck_id, distance):
    print(f'Truck {truck_id} travelled {distance} miles')

with alive_bar(len(equipment_data)) as bar:

    for key in equipment_data:

        # Simulate processing 
        process_time = randint(1,4)
        sleep(process_time)

        # Do processing
        distance = randint(10, 50) 
        update_equipment(key, distance)

        # Update progress bar 
        bar()

print('Done processing all trucks!')

