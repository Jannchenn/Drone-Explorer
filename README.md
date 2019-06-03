# Drone Explorer

UAV machine will explore a map and discover objects. 

## Getting Started

### Prerequisites
Install SITL
Preferably use on Linux 
Install QGroundControl (optional)

## Getting Started

1. Clone this project to your local machine.
2. Modify fix_paras.txt for fixed parameters.
   Example for fix_paras.txt
```
10 10
roomba
movement
100    
```
   line1: row col<br />
   line2: flying policy for the experiment: roomba will explore the map in sequence; random will explore the map randomly<br />
   line3: flying method for the experiment: movement will let the drone explore the map by the sectors to visit; time will let the drone explore in a certain period of time<br />
   line4: flying method duration: enter time duration or movement steps for the experiment

3. Modily indep_var.txt for variables.
   Example for indep_var.txt
 ```
  0.0 0.03 0.005 150 0.005
  0.1 0.03 0.005 150 0.005
  0.2 0.03 0.005 150 0.005
  0.3 0.03 0.005 150 0.005
  0.4 0.03 0.005 150 0.005
  0.5 0.03 0.005 150 0.005
  0.6 0.03 0.005 150 0.005
  0.7 0.03 0.005 150 0.005
  0.8 0.03 0.005 150 0.005
  0.9 0.03 0.005 150 0.005
  1 0.03 0.005 150 0.005
 ```
   meanings for columns from left to right:<br />
   probability for staying in the sector, events duration rate, events arrive rate, events arrive number, events die rate.

## Running the program
We have four script files for 4 different variables (though there are five variables, we set arrive rate and die rate same):<br />
   - DroneExplore_arrdie.sh
   - DroneExplore_arrnum.sh
   - DroneExplore_dur.sh
   - DroneExplore_prob.sh
For the variable to run experiments on, run the command
```
chmod 777 DroneExplore_(varname).sh
```
Then, run the script to start the experiment.
```
./DroneExplore_(varname).sh
```
Finally, after it finishes, a corresponding csv file will be generated.


## File Descriptions
More details are documented in each file
### Arena.py
This file contains Arena class, which contains the map that our agent(UAV) is going to explore
### Avgtime.py
This file will calculate the average time for 10 times roomba experiments. Later, random will do the experiment same time as roomba
### Board.py
This file contains Threading class, and this file will initiate the board to be explored
### Distribution.py
Contains distribution: exponential, random
### Drone.py
This file controls the drone action
### Edit.py
This file will change the fix_paras.txt, to let the drone take next experiment.
### Event.py
This file contains the Event object, which simulates and updates the event movements.
### Policy.py
Contains policies drone will fly including: random, roomba
### WriteReport.py
This file conmpute and analyze the result that drone collected; Generate the csv file from the collected data.
### Main.py
This file contains main function for the board running in the background and to start running the drone simulator. After the experiment finishes, it will generate the stats files.
### Graph.py / Graph2.py
This file generates corresponding graphs

