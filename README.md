# Rapsi-Car-Robot
A car robot based on the raspberry pi zero, 4tronix's icon zero motor hat, and couple of other sensors

### Components
The compenents listt is continously updated as I add new sensors to the project. The list can be found [here](./components.md)

### Scripts and Modules Usage
1. Ensure to set up raspberry pi in headless mode. This is covered in the book mentioned above or [here](https://www.tomshardware.com/reviews/raspberry-pi-headless-setup-how-to,6028.html) is a good online tutorial.
2. Also ensure to have SFTP (For file transfer) and SSH access to the Pi
3. Copy the project folder to the pi using sftp
4. SSH into the pi and navigate to the folder location
    > if this is your first time, install the dependencies by running the following in your terminal: 
    - `sudo apt-get install -y python3-pip python3-smbus ic2-tools`
    - `pip3 install -r requirements.txt`
    - enable the i2c interface. [Here](https://nl.mathworks.com/help/supportpkg/raspberrypiio/ref/enablei2c.html) is a simple online tutorial for that.
5. All the modules provide in the *lib* folder can be tested by simply running: `python3 <Module-Name>.py`
6. All files in the root folder with prefix *run_* combine different functionality and can be run similarly with the command from the previous point

### Diagrams
In progress **

### Books and Credit
-*Learn Robotics Programming by Danny Staple*.
