import math

roomPaddingX = 10
roomPaddingZ = 10

museum_rooms = [
    {
        (0, 0): "Entrance",
        (-1, 3) : "Ceiling Fan",
        (-3, 3) : "Outside Rain",
        (-3, 1) : "Caged Lion",
    },
    {
        (0, 0): "Entrance",
        (0, 3) : "Cauldron Boiling",
        (-3, 2) : "Cave Dripping",
        (-1, 4) : "Dinosaur Roaring",
    }
]

museum_tasks = [
    [
        (0, 0),
        (-1, 3),
        (-3, 3),
        (1, 3),
        (0, 0)
    ],
    [
        (0, 0),
        (0, 3),
        (-3, 2),
        (-1, 4),
        (0, 0)
    ]
]

def find_first_task_after_index(museum, rooms, task, index):
    for i in range(index, len(rooms)):
        if rooms[i] == museum_tasks[museum][task]:
            return i
    return -1

def get_rooms_per_task(file, museum):
    
    # Read the file
    raw_data = ""
    try:
        with open(file, 'r') as f:
            raw_data = f.read()
    except FileNotFoundError:
        print("File not found")
    except Exception as e:
        print(e)

    lastRoom = (0, 0)
    roomsVisited = [lastRoom]

    # Convert the raw data into a list of rooms visited
    for line in raw_data.split("\n"):
        if(line == ""):
            continue
        
        values = line.split(",")

        location = [float(values[i]) for i in [1,2,3]]
        room = (math.floor((location[0] + roomPaddingX)/300), math.floor((location[2] + roomPaddingZ)/600))
        
        if(room != lastRoom):
            roomsVisited.append(room)
            lastRoom = room

    # Used for debugging
    # print(roomsVisited)

    # Find the first instance of the required room entered after task commence
    task_finished_after_visit = [find_first_task_after_index(museum, roomsVisited, 0, 12)]
    for i in range(1, len(museum_tasks[museum])):
        task_finished_after_visit.append(find_first_task_after_index(museum, roomsVisited, i, task_finished_after_visit[i-1]))

    # The number of rooms visited per task
    rooms_per_task = [task_finished_after_visit[0]] + [task_finished_after_visit[i] - task_finished_after_visit[i-1] for i in range(1, len(task_finished_after_visit))]
    return rooms_per_task

# The scenario participant i was placed in
scenarios = [
    1, 2, 3, 4, 
    1, 2, 3, 4,
    1, 2, 3,
    2, 1, 4,
    1, 2, 3, 4,
    3, 4, 1
]


for i in range(0, len(scenarios)):
    if scenarios[i] == 1:
        print("Participant " + str(i + 1) + " in scenario " + str(scenarios[i]) + " " +
              "Museum 1 No Propagation : " + str(get_rooms_per_task(f"Museum1-NoPropagation/{i+1}.txt", 0)) + " " +
              "Museum 2 Propagation    : " + str(get_rooms_per_task(f"Museum2-Propagation/{i+1}.txt", 1)))
    elif scenarios[i] == 2:
        print("Participant " + str(i + 1) + " in scenario " + str(scenarios[i]) + " " +
              "Museum 1 Propagation :    " + str(get_rooms_per_task(f"Museum1-Propagation/{i+1}.txt", 0)) + " " +
              "Museum 2 No Propagation : " + str(get_rooms_per_task(f"Museum2-NoPropagation/{i+1}.txt", 1)))
    elif scenarios[i] == 3:
        print("Participant " + str(i + 1) + " in scenario " + str(scenarios[i]) + " " +
              "Museum 2 No Propagation : " + str(get_rooms_per_task(f"Museum2-NoPropagation/{i+1}.txt", 1)) + " " +
              "Museum 1 Propagation    : " + str(get_rooms_per_task(f"Museum1-Propagation/{i+1}.txt", 0)))
    elif scenarios[i] == 4:
        print("Participant " + str(i + 1) + " in scenario " + str(scenarios[i]) + " " +
              "Museum 2 Propagation    : " + str(get_rooms_per_task(f"Museum2-Propagation/{i+1}.txt", 1)) + " " +
              "Museum 1 No Propagation : " + str(get_rooms_per_task(f"Museum1-NoPropagation/{i+1}.txt", 0)))
    else:
        print("Invalid scenario")
            