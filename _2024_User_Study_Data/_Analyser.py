import math
import numpy as np
import pandas as pd
from scipy.stats import ttest_ind, mannwhitneyu
from collections import Counter
from scipy.stats import chi2_contingency
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path

###########################################################################

#region Helper Functions

def get_museum_info():
    rooms = {}
    
    rooms['Museum1'] = {}
    rooms['Museum1']["Entrance"    ] =  ( 0,  0)
    rooms['Museum1']["Kitchen"     ] =  ( 0,  1)
    rooms['Museum1']["Clocks"      ] =  ( 1,  1)
    rooms['Museum1']["Radio"       ] =  ( 0,  2)
    rooms['Museum1']["Spring"      ] =  ( 1,  2)
    rooms['Museum1']["Dog"         ] =  ( 2,  2)
    rooms['Museum1']["Lion"        ] =  ( 1,  3)
    rooms['Museum1']["Basketball"  ] =  ( 0,  3)
    rooms['Museum1']["Construction"] =  (-1,  2)
    rooms['Museum1']["Office"      ] =  (-1,  3)
    rooms['Museum1']["Beach"       ] =  (-1,  4)
    rooms['Museum1']["Statues"     ] =  (-2,  2)
    rooms['Museum1']["Baby"        ] =  (-2,  3)
    rooms['Museum1']["Birds"       ] =  (-3,  2)
    rooms['Museum1']["Outside room"] =  (-3,  3)

    rooms['Museum2'] = {}
    rooms['Museum2']["Entrance"    ] =  ( 0,  0)
    rooms['Museum2']["Blackboard"  ] =  ( 0,  1)
    rooms['Museum2']["Aquarium"    ] =  ( 1,  1)
    rooms['Museum2']["Studio"      ] =  ( 0,  2)
    rooms['Museum2']["Arcade"      ] =  ( 1,  2)
    rooms['Museum2']["Race car"    ] =  ( 2,  2)
    rooms['Museum2']["Frog"        ] =  ( 1,  3)
    rooms['Museum2']["Cauldron"    ] =  ( 0,  3)
    rooms['Museum2']["Waiting room"] =  (-1,  2)
    rooms['Museum2']["Saw in Wood" ] =  (-1,  3)
    rooms['Museum2']["Dinosaur"    ] =  (-1,  4)
    rooms['Museum2']["Typewriter"  ] =  (-2,  2)
    rooms['Museum2']["Reception"   ] =  (-2,  3)
    rooms['Museum2']["Cave"        ] =  (-3,  2)
    rooms['Museum2']["Blizzard"    ] =  (-3,  3)

    tasks = {}
    tasks['Museum1'] = ["Entrance", "Office", "Outside room", "Lion"]
    tasks['Museum2'] = ["Entrance", "Cauldron", "Cave", "Dinosaur"]

    return rooms, tasks

def in_room(x, z, rooms_info):
    for room_name in rooms_info:
        room = rooms_info[room_name]
        room_x = room[0] * 300
        room_z = room[1] * 600

        if abs(x - room_x) < 6/2 and abs(z - room_z) < 12/2:
            return room_name
        
    print("ERROR: Player not in any room bounds at x=" + str(x) + ", z=" + str(z))
    return ""

def angle(q1, q2, degrees = True):

    # Inspired code from:
    # https://forum.unity.com/threads/quaternion-angle-implementation.572632/

    quaternion1 = np.array([q1[3], q1[0], q1[1], q1[2]])
    quaternion2 = np.array([q2[3], q2[0], q2[1], q2[2]])

    dot_product = min(np.dot(quaternion1, quaternion2), 1)

    angle_radians = np.arccos(dot_product) * 2
    angle_degrees = np.degrees(angle_radians)

    return angle_degrees if degrees else angle_radians

def round_sig(x, sig=3):
    return round(x, sig-int(math.floor(math.log10(abs(x))))-1) if x != 0 else 0

def get_scenario_experiments(scenario):
    _1st_museum, _2nd_museum = ('Museum1', 'Museum2') if scenario in [1, 2] else ('Museum2', 'Museum1')
    _1st_propagation, _2nd_propagation = ('Propagation', 'NoPropagation') if scenario in [2, 4] else ('NoPropagation', 'Propagation')
        
    return (f'{_1st_museum}-{_1st_propagation}', f'{_2nd_museum}-{_2nd_propagation}')

def get_experiment_stages():        
    return ['guided_tour', 'task_1', 'task_2', 'task_3', 'task_4']

#endregion

###########################################################################

#region Extracting Data

class UserInfo:
    def __init__(self, scenario):
        self.scenario = scenario
        self.data = {}

        self.data["pre_experiment"] = {}

        self.data["first_experiment"] = {}

        self.data["second_experiment"] = {}

        self.data["post_experiment"] = {}

    def infer_experiment_info(self, experiment, raw_data, rooms_info, tasks_info):
        raw_lines = raw_data.split("\n")

        last_time = 0
        last_position = ()
        last_rotation = ()
        last_room = ""

        total_room_visits = 0
        total_distance = 0
        total_turn = 0

        stages = get_experiment_stages()
        current_stage = 0
        for i in range(len(raw_lines) - 1):
            if stages[current_stage] not in self.data[experiment]:
                self.data[experiment][stages[current_stage]] = {}
                room_visits = 0
                stage_init_time = last_time
                stage_distance = 0
                stage_turn = 0
                
            line_info = raw_lines[i].split(",")

            time = float(line_info[0])
            position = (float(line_info[1]), float(line_info[2]), float(line_info[3]))
            rotation = (float(line_info[4]), float(line_info[5]), float(line_info[6]), float(line_info[7]))

            current_room = in_room(position[0], position[2], rooms_info)

            if current_room != "":
                if current_room not in self.data[experiment][stages[current_stage]]:
                    self.data[experiment][stages[current_stage]][current_room] = {}
                    self.data[experiment][stages[current_stage]][current_room]["order"] = len(self.data[experiment][stages[current_stage]]) - 1
                    self.data[experiment][stages[current_stage]][current_room]["sequence"] = []
                    self.data[experiment][stages[current_stage]][current_room]["total_time"] = 0
                    self.data[experiment][stages[current_stage]][current_room]["total_distance"] = 0
                    self.data[experiment][stages[current_stage]][current_room]["total_turn"] = 0

                if current_room != last_room:
                    self.data[experiment][stages[current_stage]][current_room]["sequence"].append(room_visits)
                    room_visits += 1
                    total_room_visits += 1
                elif i > 0:
                    distance = math.dist(position, last_position)
                    turn = angle(rotation, last_rotation)

                    self.data[experiment][stages[current_stage]][current_room]["total_time"] += time - last_time
                    self.data[experiment][stages[current_stage]][current_room]["total_distance"] += distance
                    self.data[experiment][stages[current_stage]][current_room]["total_turn"] += turn

                    total_distance += distance
                    stage_distance += distance
                    total_turn += turn
                    stage_turn += turn
                last_room = current_room

            last_time = time
            last_position = position
            last_rotation = rotation

            if(total_room_visits > 17 and current_stage < len(tasks_info) and current_room == tasks_info[current_stage]):
                self.data[experiment][stages[current_stage]]["total_room_visits"] = room_visits
                stage_time = last_time - stage_init_time
                self.data[experiment][stages[current_stage]]["total_time"] = stage_time
                self.data[experiment][stages[current_stage]]["distance_per_time"] = stage_distance / stage_time
                self.data[experiment][stages[current_stage]]["turn_per_time"] = stage_turn / stage_time
                current_stage += 1
                
        self.data[experiment][stages[current_stage]]["total_room_visits"] = room_visits
        stage_time = last_time - stage_init_time
        self.data[experiment][stages[current_stage]]["total_time"] = stage_time
        self.data[experiment][stages[current_stage]]["distance_per_time"] = stage_distance / stage_time
        self.data[experiment][stages[current_stage]]["turn_per_time"] = stage_turn / stage_time     

        self.data[experiment]["total_room_visits"] = total_room_visits
        self.data[experiment]["total_time"] = last_time
        self.data[experiment]["distance_per_time"] = total_distance / last_time
        self.data[experiment]["turn_per_time"] = total_turn / last_time

def get_user_infos(rooms_info, tasks_info):

    user_infos = {}

    # Extract pre experiment info from google forms (.csv)
        
    pre_experiment_file = 'pre_experiment.csv'
    pre_experiment_df = pd.read_csv(pre_experiment_file)

    pre_experiment_ids = pre_experiment_df.iloc[:, 0]
    gender_values = pre_experiment_df.iloc[:, 1]
    age_values = pre_experiment_df.iloc[:, 2]
    hours_playing_games_values = pre_experiment_df.iloc[:, 3]
    spatial_ability_values = pre_experiment_df.iloc[:, 4]
    energetic_values = pre_experiment_df.iloc[:, 5]
    spatial_test_values = pre_experiment_df.iloc[:, 6]
    hmd_values = pre_experiment_df.iloc[:, 7]
    scenario_values = pre_experiment_df.iloc[:, 9]
    complete_values = pre_experiment_df.iloc[:, 10]

    for index, value in pre_experiment_ids.items():
        if complete_values[index] == 'No':
            continue
        id = int(value)
        user_infos[id] = UserInfo(int(scenario_values[index]))
        user_infos[id].data["pre_experiment"]["gender"] = gender_values[index]
        user_infos[id].data["pre_experiment"]["age"] = int(age_values[index])
        user_infos[id].data["pre_experiment"]["hours_playing"] = str(hours_playing_games_values[index])
        user_infos[id].data["pre_experiment"]["spatial_ability"] = int(spatial_ability_values[index])
        user_infos[id].data["pre_experiment"]["energetic"] = int(energetic_values[index])
        user_infos[id].data["pre_experiment"]["spatial_test"] = spatial_test_values[index]
        user_infos[id].data["pre_experiment"]["hdm"] = hmd_values[index]

    for id in user_infos:
        first_experiment, second_experiment = get_scenario_experiments(user_infos[id].scenario)
        
        # Infer path info from raw game data (.txt) with rooms info for the first experiment
        first_data_path = Path(f'ParticipantData/{first_experiment}/{id}.txt')
        try:
            with open(first_data_path, 'r') as file:
                raw_game_data = file.read()
                museum = first_experiment.split('-')[0]
                user_infos[id].infer_experiment_info('first_experiment', raw_game_data, rooms_info[museum], tasks_info[museum])
        except FileNotFoundError:
            print(f"File '{first_path_data_filename}' not found.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

        # Infer path info from raw game data (.txt) with rooms info for the second experiment
        second_data_path = Path(f'ParticipantData/{second_experiment}/{id}.txt')
        try:
            with open(second_data_path, 'r') as file:
                raw_game_data = file.read()
                museum = second_experiment.split('-')[0]
                user_infos[id].infer_experiment_info('second_experiment', raw_game_data, rooms_info[museum], tasks_info[museum])
        except FileNotFoundError:
            print(f"File '{second_path_data_filename}' not found.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    # Extract post experiment info from google forms (.csv)
    
    post_experiment_file = 'post_experiment.csv'
    post_experiment_df = pd.read_csv(post_experiment_file)

    post_experiment_id_values = post_experiment_df.iloc[:, 0]
    immersion_first_experiment_values = post_experiment_df.iloc[:, 2]
    realistic_first_experiment_values = post_experiment_df.iloc[:, 3]
    immersion_second_experiment_values = post_experiment_df.iloc[:, 5]
    realistic_second_experiment_values = post_experiment_df.iloc[:, 6]
    motion_sickness_values = post_experiment_df.iloc[:, 8]

    for index, value in post_experiment_id_values.items():
        id = int(value)
        if id not in user_infos:
            continue
        
        user_infos[id].data["first_experiment"]["immersion"] = int(immersion_first_experiment_values[index])
        user_infos[id].data["first_experiment"]["realistic"] = int(realistic_first_experiment_values[index])
        user_infos[id].data["second_experiment"]["immersion"] = int(immersion_second_experiment_values[index])
        user_infos[id].data["second_experiment"]["realistic"] = int(realistic_second_experiment_values[index])
        user_infos[id].data["post_experiment"]["motion_sickness"] = motion_sickness_values[index]

    return user_infos
    
#endregion

###########################################################################

def main():
    rooms_info, tasks_info = get_museum_info()
    user_infos = get_user_infos(rooms_info, tasks_info)

    conditions_by_scenario = {}
    conditions_by_scenario['Scenario 1 VS Scenario 3 (No Propagation First)'] = ([1], [3])
    conditions_by_scenario['Scenario 2 VS Scenario 4 (Propagation First)'] = ([2], [4])
    conditions_by_scenario['Scenario 1,2 VS Scenario 3,4 (Museum 1 First VS Museum 2 First)'] = ([1, 2], [3, 4])
    conditions_by_scenario['Scenario 1,3 VS Scenario 2,4 (No Propagation First VS Propagation First)'] = ([1, 3], [2, 4])
    conditions_by_scenario['Scenario 1,4 VS Scenario 2,3 (Same combination of museum and propagation)'] = ([1, 4], [2, 3])

    for condition in conditions_by_scenario:
        print('######')
        print(condition)
        group0, group1 = conditions_by_scenario[condition]

        compare_conditions_by_scenario(["pre_experiment","gender"], group0, group1, user_infos)
        compare_conditions_by_scenario(["pre_experiment","age"], group0, group1, user_infos)
        compare_conditions_by_scenario(["pre_experiment","hours_playing"], group0, group1, user_infos)
        compare_conditions_by_scenario(["pre_experiment","spatial_ability"], group0, group1, user_infos)
        compare_conditions_by_scenario(["pre_experiment","energetic"], group0, group1, user_infos)
        compare_conditions_by_scenario(["pre_experiment","spatial_test"], group0, group1, user_infos)
        compare_conditions_by_scenario(["pre_experiment","hdm"], group0, group1, user_infos)
        
        compare_conditions_by_scenario(["post_experiment","motion_sickness"], group0, group1, user_infos)

    conditions_by_experiment = {}
    conditions_by_experiment['Scenario 1'] = ([(1, 'first_experiment')], [(1, 'second_experiment')])
    conditions_by_experiment['Scenario 2'] = ([(2, 'first_experiment')], [(2, 'second_experiment')])
    conditions_by_experiment['Scenario 3'] = ([(3, 'first_experiment')], [(3, 'second_experiment')])
    conditions_by_experiment['Scenario 4'] = ([(4, 'first_experiment')], [(4, 'second_experiment')])
    conditions_by_experiment['Musem 1 - No Propagation - First VS Musem 1 - No Propagation - Second'] = ([(1, 'first_experiment')], [(4, 'second_experiment')])
    conditions_by_experiment['Musem 2 - No Propagation - First VS Musem 2 - No Propagation - Second'] = ([(3, 'first_experiment')], [(2, 'second_experiment')])
    conditions_by_experiment['Musem 1 - Propagation - First VS Musem 1 - Propagation - Second'] = ([(2, 'first_experiment')], [(3, 'second_experiment')])
    conditions_by_experiment['Musem 2 - Propagation - First VS Musem 2 - Propagation - Second'] = ([(4, 'first_experiment')], [(1, 'second_experiment')])
    conditions_by_experiment['Musem 1 - First VS Musem 2 - Second'] = ([(1, 'first_experiment'),(2, 'first_experiment')], [(1, 'second_experiment'),(2, 'second_experiment')])
    conditions_by_experiment['Musem 2 - First VS Musem 1 - Second'] = ([(3, 'first_experiment'),(4, 'first_experiment')], [(3, 'second_experiment'),(4, 'second_experiment')])
    conditions_by_experiment['No Propagation - First VS Propagation - Second'] = ([(1, 'first_experiment'),(3, 'first_experiment')], [(1, 'second_experiment'),(3, 'second_experiment')])
    conditions_by_experiment['No Propagation - First VS No Propagation - Second'] = ([(1, 'first_experiment'),(3, 'first_experiment')], [(2, 'second_experiment'),(4, 'second_experiment')])
    conditions_by_experiment['Propagation - First VS No Propagation - Second'] = ([(2, 'first_experiment'),(4, 'first_experiment')], [(2, 'second_experiment'),(4, 'second_experiment')])
    conditions_by_experiment['Propagation - First VS Propagation - Second'] = ([(2, 'first_experiment'),(4, 'first_experiment')], [(1, 'second_experiment'),(3, 'second_experiment')])
    conditions_by_experiment['No Propagation VS Propagation'] = ([(1, 'first_experiment'),(2, 'second_experiment'),(3, 'first_experiment'),(4, 'second_experiment')], [(1, 'second_experiment'),(2, 'first_experiment'),(3, 'second_experiment'),(4, 'first_experiment')])
    conditions_by_experiment['Museum 1 VS Museum 2'] = ([(1, 'first_experiment'),(2, 'first_experiment'),(3, 'second_experiment'),(4, 'second_experiment')], [(1, 'second_experiment'),(2, 'second_experiment'),(3, 'first_experiment'),(4, 'first_experiment')])

    conditions_by_experiment['Propagation vs No Propagation in Museum 1'] = ([(1, 'first_experiment'),(4, 'second_experiment')], [(2, 'first_experiment'),(3, 'second_experiment')])
    conditions_by_experiment['Propagation vs No Propagation in Museum 2'] = ([(1, 'second_experiment'),(4, 'first_experiment')], [(2, 'second_experiment'),(3, 'first_experiment')])

    conditions_by_experiment['Propagation vs No Propagation in Museum 1 First'] = ([(1, 'first_experiment')], [(2, 'first_experiment')])
    conditions_by_experiment['Propagation vs No Propagation in Museum 1 Second'] = ([(4, 'second_experiment')], [(3, 'second_experiment')])

    conditions_by_experiment['Propagation vs No Propagation in Museum 2 First'] = ([(4, 'first_experiment')], [(3, 'first_experiment')])
    conditions_by_experiment['Propagation vs No Propagation in Museum 2 Second'] = ([(1, 'second_experiment')], [(2, 'second_experiment')])


    for condition in conditions_by_experiment:
        print('######')
        print(condition)
        group0, group1 = conditions_by_experiment[condition]
        print('First Group:', group0)
        print('Second Group:', group1)

        compare_conditions_by_experiment(["?_experiment","immersion"], group0, group1, user_infos)
        compare_conditions_by_experiment(["?_experiment","realistic"], group0, group1, user_infos)
        
        compare_conditions_by_experiment(["?_experiment","total_room_visits"], group0, group1, user_infos)
            
        for stage in get_experiment_stages():
            compare_conditions_by_experiment(["?_experiment", stage, "total_room_visits"], group0, group1, user_infos)

    print()
    print("Done")

###########################################################################

#region Analysing Data

def compare_conditions_by_scenario(variable, group0, group1, user_infos):

    list0 = []
    list1 = []

    ordered = True

    for id in sorted(list(user_infos.keys())):
        data = user_infos[id].data
        scenario = user_infos[id].scenario
        if scenario in group0:
            target_list = list0
        elif scenario in group1:
            target_list = list1
        else:
            continue

        target_value = data
        for value_type in variable:
            target_value = target_value[value_type]

        if ordered and isinstance(target_value, str):
            ordered = False

        if isinstance(target_value, list) or isinstance(target_value, dict):
            target_value = len(target_value)

        target_list.append(target_value)

    run_test(variable, list0, list1, ordered)

def compare_conditions_by_experiment(variable, group0, group1, user_infos):

    list0 = []
    list1 = []

    ordered = True

    for id in sorted(list(user_infos.keys())):
        data = user_infos[id].data
        user_scenario = user_infos[id].scenario
        scenario0, scenario1 = None, None
        for experiment in group0:
            if user_scenario == experiment[0]:
                scenario0, experiment0 = experiment
                break
        for experiment in group1:
            if user_scenario == experiment[0]:
                scenario1, experiment1 = experiment
                break

        if scenario0 != None:
            target_value = data
            for value_type in variable:
                value_type = experiment0 if value_type == '?_experiment' else value_type
                target_value = target_value[value_type]

            if isinstance(target_value, list) or isinstance(target_value, dict):
                target_value = len(target_value)

            if ordered and isinstance(target_value, str):
                ordered = False

            list0.append(target_value)

        if scenario1 != None:
            target_value = data
            for value_type in variable:
                value_type = experiment1 if value_type == '?_experiment' else value_type
                target_value = target_value[value_type]

            if ordered and isinstance(target_value, str):
                ordered = False

            if isinstance(target_value, list) or isinstance(target_value, dict):
                target_value = len(target_value)

            if ordered and isinstance(target_value, str):
                ordered = False

            list1.append(target_value)

    run_test(variable, list0, list1, ordered)


def run_test(variable, list0, list1, ordered):

    print("#")

    if ordered:
        print(variable, "(Ordered):")
        
        mean0 = np.mean(list0)
        mean1 = np.mean(list1)

        statistic, t_test_p_value = ttest_ind(list0, list1)
        statistic, wilcoxon_p_value = mannwhitneyu(list0, list1)

        print("First Group Mean =", round_sig(mean0))
        print("Second Group Mean =", round_sig(mean1))
        print("T-test P-value =", round(t_test_p_value, 3))
        print("Wilcoxon P-value =", round(wilcoxon_p_value, 3))
        if wilcoxon_p_value < 0.05:
            if t_test_p_value < 0.05:
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ^ Double Significant ^ !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            else:
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ^ Wilcoxon Significant ^ !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        elif t_test_p_value < 0.05:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ^ T-test Significant ^ !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    else:
        print(variable, "(Unordered):")
        
        count_list0 = dict(Counter(list0))
        count_list1 = dict(Counter(list1))
        sorted_count_list0 = dict(sorted(count_list0.items()))
        sorted_count_list1 = dict(sorted(count_list1.items()))

        observed = []
        for category in set(list0 + list1):
            observed.append([list0.count(category), list1.count(category)])

        chi2, chi_p_value, _, _ = chi2_contingency(observed)

        print("First Group =", sorted_count_list0)
        print("Second Group =", sorted_count_list1)
        print("Chi P-value =", chi_p_value)

        if chi_p_value < 0.05:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ^ Chi Significant ^ !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

#endregion

###########################################################################

main()
