# dronekit-vision-integration
This repository is owned by aeroKLE SAE aerodesign team. It combines dronekit and computer vision project together.<br/>
To see files go to master branch.</br>
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
![1](https://user-images.githubusercontent.com/114636450/204099101-fe5e9075-0a7e-43df-a4e5-cc5daf401b8b.png)
![2](https://user-images.githubusercontent.com/114636450/204099108-594b1bb5-3e41-4a45-b29a-0ff4de6d3c11.jpg)
![3](https://user-images.githubusercontent.com/114636450/204099114-df7b0eaa-f2be-4abf-94fa-bab9f2fbd5e6.jpg)
![4](https://user-images.githubusercontent.com/114636450/204099120-9f7affec-7e11-4f73-bc63-3f5f2fc071a1.jpg)
![5](https://user-images.githubusercontent.com/114636450/204099125-74bf38f7-3a56-4f8e-806f-04216acb0436.jpg)
![IMG-20221121-WA0009](https://user-images.githubusercontent.com/114636450/204099135-99bfc970-dd72-415b-9760-ff73bd63dde3.jpg)

