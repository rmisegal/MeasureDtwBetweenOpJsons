# MeasureDtwBetweenOpJsons
Measure the Dtw between two Jsons folders that was created with OpenPose

You need first to have two movies:
  Expert movie (e.g. exercise_arm_full_range.mp4) 
  and a Patient movie (e.g. 100100AFR.mp4).
  
You have to extract via the OpenPose the JSON files to two folders e.g.:
  C:\24D\CzechData\Data\00001AFR\Expert\Json 
  C:\24D\CzechData\Data\00001AFR\Patient\Json) 
  
with the following two commands:
  OpenPoseDemo.exe --video C:\24D\CzechData\Data\00001AFR\Expert\Video\exercise_arm_full_range.mp4 --write_json C:\24D\CzechData\Data\00001AFR\Expert\Json --display 0 --render_pose 0
  OpenPoseDemo.exe --video C:\24D\CzechData\Data\00001AFR\Patient\Video\100100AFR.mp4 --write_json C:\24D\CzechData\Data\00001AFR\Patient\Json --display 0 --render_pose 0

Now, those two folders will contain many JSON files (one per frame) that contain body skeleton vertexes.

from the terminal run: 
  python main.py C:\24D\CzechData\Data\00001AFR\Expert\Json C:\24D\CzechData\Data\00001AFR\Patient\Json

as an output you will get:

  C:\24D\CzechData\Data\00001AFR\Patient\Json_twoline.zip 
    The zip file contains 50 pictures (graphs) in total.
    Each picture present the flow of one vertex along the expert and the patient movies (location per frame along all movie) 
    The vertex location has 2 components X, Y -Therefore we have two graphs per-vertex (two pictures) - one for the X component movement along with the movie and one for the Y movement.
    Each picture contains two graph lines - a graph for the expert vertex movement and a graph for the same vertex for the patient.
    
  C:\24D\CzechData\Data\00001AFR\Patient\Json_optimalWarping.zip
    it contains the optimal warping path for each vertex per component.
    
  In the terminal, you will get a printout of the score where 0 is a perfect match (you can test it by inserting the same JSON files as an expert and as a patient)
