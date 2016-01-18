####SDN- OpenVswitch:Routing using RYU controller and Link information gathering 

##### About the project
1.Designed a custom network topology and developed python script for capturing network connectivity/reachability. 
2.Modified and developed function in a script for finding shortest path in topology upon link failure or breakage. 
3.Link status of all the links are captured and is used for finding the shortest path for the flow of packets.

##### For introduction of Openflow, OpenVswitch, use "http://archive.openflow.org/wk/index.php/OpenFlow_Tutorial" and "http://openvswitch.org/" respectively.


##### Steps to run the project
1. Install Mininet, use "http://mininet.org/" for further details
2. Install RYU controller, for more information on RYU controller "https://media.readthedocs.org/pdf/ryu/latest/ryu.pdf"
3. Place the custom_topology file within the custom folder of mininet.
4. Place all the files inside the ryu folder of my repo as it is.
5. Run the GUI.py
6. Click on Create Mininet topology. This will run the custom_topology.py which i have created to check the dynamic routing of the controller.
6.1. This will create a mininet topology according to my custom topology.py file.Use pingall command to test the reachability.
7. Click on Run controller. Reachability will be acheived only when the controller is switched on as it is a remote controller.
7.1. Run pingall command on the mininet window. Now you can see that there is a reachability to all the hosts and switches after the controller is turned on. Use "ctrl c" to exit the window.
8.Click on Log details.(If the command shows "Already in use" , this means that the controller window is still not closed. 
8.1. This will get information of all the links in the topology. This can be checked by using the command "link s1 s2 down". This change in the link status can be seen in the port modify file and the link add file.Check for reachability. There will be 'x' marks on links that cannot be reached
8.2 Close the log details window
9. Since the link is down we need to find the shortest path for the packets to flow. Click on Run shortest path file. 
10. Do not close the Shortest path window and click on the next tab in the GUI.
10.1 This will push the flow of packets in an alternate way. After all the windows that pop up have closed automatically, check for reachability again. You will notice that all the hosts can be reached without loss of packets with an alternate way. This makes this RYU controller dynamic.
11.Close the Shortest path window. 
12. Exit.


