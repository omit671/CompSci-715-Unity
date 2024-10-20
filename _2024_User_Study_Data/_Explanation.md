# Overview Explanation

Our user study evaluates the efficiency with which participants navigate through the virtual museum environment we place them in. We give them tasks to navigate from one room to another, and we record the path that they take.

Participants were place into of four scenarios:
1. 1st A no propagation, 2nd B propagation
2. 1st A propagation, 2nd B no propagation
3. 1st B no propagation, 2nd A propagation
4. 1st B propagation, 2nd A no propagation


# Pre-experiment Explanation

The spreadsheet called "pre_experiment_raw.csv" contains the raw information downloaded from Google Forms regarding the pre-experiment survey responses. A viewable pdf version of the pre-experiment survey can be found in the "Pre-experiment Survey.pdf" file. The "pre_experiment.csv" file is a modified version of the "pre_experiment_raw.csv" that is read by the "_Analyser.py" script. The first row in the "pre_experiment.csv" contains the text prompted to the user per question.

The following columns are analysed from the "pre_experiment.csv" file:
A: Research ID.
B to H: Demographics.
I: Scenario ID.
J: Experiment was Completed (Imcomplete experiments are discarded).


# Post-experiment Explanation

The spreadsheet called "post_experiment_raw.csv" contains the raw information downloaded from Google Forms regarding the post-experiment survey responses. A viewable pdf version of the post-experiment survey can be found in the "Post-experiment Survey.pdf" file. The "post_experiment.csv" file is a modified version of the "post_experiment_raw.csv" that is read by the "_Analyser.py" script. The first row in the "post_experiment.csv" contains the text prompted to the user per question.

The following contains categories of columns analysed from the "post_experiment.csv" file:
A: Research ID.
B: Open-ended first museum question.
C and D: Quantitative feedback questions about the first museum.
E: Open-ended second museum question.
F and G: Quantitative feedback questions about the second museum.
H: Open-ended preference question.
I: Feedback questions about motion sickness.
J: Open-ended improvement question.


# Game Data Explanation

Each of the "#.dat" and "#.txt" files in the 'ParticipantData' folder is a data file relating to a particular participant's user study. The subfolder represent the experiment condition e.g. Museum1-NoPropagation. The number in these files refer to a participant's research ID.
The ".dat" file type is an encoded save file that the SaveAndLoad script in this Unity project can directly read and write to as a custom class (LogData class).
The ".txt" file type displays information from the LogData class in a readable text format. This ".txt" file is automatically generated when a LogData class is saved in Unity via the SaveAndLoad script.

The ".txt" files contain data on various lines. The following explains the comma-seperated information stored per line:
- Time index in seconds since the start of recording (as float),
- X-axis information of the head's position at the given time index (as float, originated from Vector3),
- Y-axis information of the head's position at the given time index (as float, originated from Vector3),
- Z-axis information of the head's position at the given time index (as float, originated from Vector3),
- X-axis information of the head's rotation at the given time index (as float, originated from Quaternion),
- Y-axis information of the head's rotation at the given time index (as float, originated from Quaternion),
- Z-axis information of the head's rotation at the given time index (as float, originated from Quaternion),
- W-axis information of the head's rotation at the given time index (as float, originated from Quaternion)
The time index from line to line should always increase. Note that for a Unity Vector3, 1 unit is 1 meter.

Large distances in head position between subsequent time indexes indicate that a user traveled through a portal. Keep this in mind if you plan to infer certain results, such as total distance traveled.
Each room in the virtual museum is 3 meters wide in the x-axis and 6 meters wide in the z-axis.
The following list contains the room-grid-position of the center of each room for the first museum:
- "Entrance"     ,   0,  0
- "Kitchen"      ,   0,  1
- "Clocks"       ,   1,  1
- "Radio"        ,   0,  2
- "Spring"       ,   1,  2
- "Dog"          ,   2,  2
- "Lion"         ,   1,  3
- "Basketball"   ,   0,  3
- "Construction" ,  -1,  2
- "Office"       ,  -1,  3
- "Beach"        ,  -1,  4
- "Statues"      ,  -2,  2
- "Baby"         ,  -2,  3
- "Birds"        ,  -3,  2
- "Outside room" ,  -3,  3

The following list contains the room-grid-position of the center of each room for the second museum:
- "Entrance"     ,   0,  0
- "Blackboard"   ,   0,  1
- "Aquarium"     ,   1,  1
- "Studio"       ,   0,  2
- "Arcade"       ,   1,  2
- "Race car"     ,   2,  2
- "Frog"         ,   1,  3
- "Cauldron"     ,   0,  3
- "Waiting room" ,  -1,  2
- "Saw in Wood"  ,  -1,  3
- "Dinosaur"     ,  -1,  4
- "Typewriter"   ,  -2,  2
- "Reception"    ,  -2,  3
- "Cave"         ,  -3,  2
- "Blizzard"     ,  -3,  3
To get the real position in meters of each room*, multiply the first axis of the room-grid-position by 300, and the second axis by 600.

With a participant's log data, as well as the bounds and position of each room, we can infer new data, such as how many rooms a participant visited and for how long they visited in total.

Example: (Infering what room a participant is in at a given time)

Line from logdata: 27.53, 300.05, 1.65, 600.72, 0.0, 0.0, 0.0, 1.0
We can infer that the user was at position (300.05, 1.65, 600.72) 27.53 seconds into the experiment.

Room-Grid-Position: Clocks = 1, 1 (Museum 1)
Real-Position of room: Clocks = 1 * 300, 1 * 600 = Vector3(1 * 300, 0, 1 * 600) = Vector3(300, 0, 600)
Room size: 3m, 6m
Room bounds: ±3, ±6
User-position-x check: 300.05 is within ±3 of 300
User-position-z check: 600.65 is within ±6 of 600
We can infer that the user was in the Clocks room 27.53 seconds into the experiment.
