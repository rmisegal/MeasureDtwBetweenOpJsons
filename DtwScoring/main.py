# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os, json, sys
import dtw
import chart
import normalization
import numpy as np
import concurrent.futures
from zipfile import ZipFile
import os
from os.path import basename

def zip_json_files(zip_file_path, directory_to_zip):
  # create a ZipFile object
  with ZipFile(os.path.splitext(zip_file_path)[0]+".zip", 'w') as zipObj:
    # Iterate over all the files in directory
    for folderName, subfolders, filenames in os.walk(directory_to_zip):
        for filename in filenames:
            #create complete filepath of file in directory
            filePathCurr = os.path.join(folderName, filename)
            # Add file to zip
            zipObj.write(filePathCurr, basename(filePathCurr))
  return os.path.splitext(zip_file_path)[0]+".zip"

def json_path_array(path):
    json_files = [pos_json for pos_json in os.listdir(path) if pos_json.endswith('.json')]
    return json_files


def vector_arrays_from_json(path_to_json):
    json_files = json_path_array(path_to_json)
    vector_array = [[0 for i in range(len(json_files))] for i in range(50)]
    for index_frame, js in enumerate(json_files):
        with open(os.path.join(path_to_json, js)) as json_file:
            json_text = json.load(json_file)
            people = json_text['people']
            if len(people) > 0:
                vector = people[0]['pose_keypoints_2d']
                x, y = normalization.normal_vector(vector)
                xy = np.concatenate((x, y))
                for i in range(0, 50):
                    vector_array[i][index_frame] = xy[i]
    return vector_array

def compute_cost(aar1, arr2):
    C = dtw.compute_cost_matrix(aar1, arr2, metric='euclidean')
    D = dtw.compute_accumulated_cost_matrix(C)
    P = dtw.compute_optimal_warping_path(D)
    c_P = sum(D[n, m] for (n, m) in P)
    return c_P / len(P)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    path_to_json_expert = sys.argv[1] 
    path_to_json_patient = sys.argv[2]
    vector_arrays_expert = vector_arrays_from_json(path_to_json_expert) #convert JSON to 50 (25 vertexes, X,Y total 50) 1D arrays that are normalized
    vector_arrays_patient = vector_arrays_from_json(path_to_json_patient)
    
    distances = []
    os.mkdir(os.path.join(path_to_json_patient,"twoLineGraph"))
    for i in range(len(vector_arrays_expert)):
        twoline_file = os.path.join(path_to_json_patient,"twoLineGraph", "lineNum_" + str(i+1) +".png")
        chart.compare_tow_line(vector_arrays_expert[i], vector_arrays_patient[i], twoline_file)
    print(zip_json_files(os.path.join(path_to_json_patient + "_twoline.zip"), os.path.join(path_to_json_patient,"twoLineGraph")))

    os.mkdir(os.path.join(path_to_json_patient,"optimalWarpingPath"))
    for i in range(len(vector_arrays_expert)):
        optimal_file = os.path.join(path_to_json_patient,"optimalWarpingPath", "optimalWarping_" + str(i+1) +".png")
        C =  dtw.compute_cost_matrix(vector_arrays_expert[i], vector_arrays_patient[i], metric='euclidean')
        # print('Cost matrix C =', C, sep='\n')

        D =  dtw.compute_accumulated_cost_matrix(C)
        # print('Accumulated cost matrix D =', D, sep='\n')
        # print('DTW distance DTW(X, Y) =', D[-1, -1])

        P = dtw.compute_optimal_warping_path(D)
        # print('Optimal warping path P =', P.tolist())

        c_P = sum(D[n, m] for (n, m) in P)
        # print(c_P / len(P))
        # print('Total cost of optimal warping path:', c_P)
        # print('DTW distance DTW(X, Y) =', D[-1, -1])
        # optimal_file = os.path.join(path_to_json_patient + ".png")
        chart.optimal_path(P, D, optimal_file)
    print(zip_json_files(os.path.join(path_to_json_patient + "_optimalWarping.zip"), os.path.join(path_to_json_patient,"optimalWarpingPath")))

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        future_to_compere = {executor.submit(compute_cost, vector_arrays_expert[i], vector_arrays_patient[i]): i for i in range(0, 50)}
        for future in concurrent.futures.as_completed(future_to_compere):
            index = future_to_compere[future]
            try:
                data = future.result()
            except Exception as exc:
                print(exc)
            else:
                distances.append(data)

    score = np.average(distances)
    print(score)













