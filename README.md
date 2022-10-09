# dronekit-vision-integration
This repository is owned by aeroKLE SAE aerodesign team. It combines dronekit and computer vision project together.<br/>
No need to run vision and dronekit scripts separately.<br/>
Only dronekit script command run both of them.<br/>
No need to give argument to vision scripts as arguments are removed and model and other files are predefined in code.<br/>
In order to change them you have to do it in the code.<br/>
These commands are tested on dronekit-sitl on mission planner.<br/>
follow these commands.<br/>
open three linux terminals.<br/>
1st terminal: dronekit-sitl copter --home=28.3678576,77.3168729,0,270   (change home location and yaw angle as needed).<br/>
2nd terminal:mavproxy.py --master tcp:127.0.0.1:5760 --sitl 127.0.0.1:5501 --out 127.0.0.1:14550 --out 127.0.0.1:14551 --out 127.0.0.1:14552.<br/>
3rd terminal:sudo python3 aerothon.py --connect udp:127.0.0.1:14550      (change the parameters like speed,relative location as needed).<br/>
This will run a dronekit script, in the script you can use centroid coordinates whereever is needed by calling eye function eye().<br/>
eye() is defined in classify.py,classifyimage.py and classify-video.py.<br/>
eye() will only print centroid coordinates, to change use return in the vision scripts.<br/>
Import any one of the vision scripts as required.<br/>
