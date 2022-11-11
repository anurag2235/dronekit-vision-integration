dronekit-vision-integration
This repository is owned by aeroKLE SAE aerodesign team. It combines dronekit and computer vision project together.
To see files go to master branch.
No need to run vision and dronekit scripts separately.
Only dronekit script command run both of them.
No need to give argument to vision scripts as arguments are removed and model and other files are predefined in code.
In order to change them you have to do it in the code.
These commands are tested on dronekit-sitl on mission planner.
follow these commands.
open three linux terminals.
1st terminal: dronekit-sitl copter --home=28.3678576,77.3168729,0,270 (change home location and yaw angle as needed).
2nd terminal:mavproxy.py --master tcp:127.0.0.1:5760 --sitl 127.0.0.1:5501 --out 127.0.0.1:14550 --out 127.0.0.1:14551 --out 127.0.0.1:14552.
3rd terminal:sudo python3 aerothon.py --connect udp:127.0.0.1:14550 (change the parameters like speed,relative location as needed).
This will run a dronekit script, in the script you can use centroid coordinates whereever is needed by calling eye function eye().
eye() is defined in classify.py,classifyimage.py and classify-video.py.
eye() will only print centroid coordinates, to change use return in the vision scripts.
Import any one of the vision scripts as required.
HASTA LA VISTA BABY
