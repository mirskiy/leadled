have python 3.2 by default, upgrading isn't super easy
needed py3.3 for something, don't remember what (for flask! even though we don't need it anymore...)

## todo:

- install flask, run through flask tutorial
- get flask to call a python function
- will flask keep the i2c connection open or does it restart every time?
- flask -> python -> i2c -> leds!
- later flask/django -> aws -> ssh -> zmq -> rpi -> python -> i2c -> leds
 - ssh https://zeromq.github.io/pyzmq/ssh.html
 - heartbeat http://zguide.zeromq.org/page:all#Heartbeating
 - dashboards:
  - https://www.raspberrypi.org/forums/viewtopic.php?f=36&t=69192
  - http://www.rpi-dashboard.com/
  - http://shopify.github.io/dashing/  <- most useful for future!
   - http://saltmines.us/blog/devlab/dashboard/

## problems:


## journal:

http://raspberrypi.stackexchange.com/questions/26118/python-in-the-latest-raspbian-wheezy

## future install: (solves py3.4, libzmq3)

http://procrastinative.ninja/2014/07/20/install-python34-on-raspberry-pi/
- sudo apt-get install libbz2-1.0 libbz2-dev libffi5 libffi-dev libncursesw5 libncursesw5-dev libreadline6 libreadline6-dev liblzma5 liblzma-dev libsqlite3-0 libsqlite3-dev libexpat1 libexpat1-dev libssl-dev openssl
- python3.4 from source
- pip3 install pyzmq (installs libzmq3 if not present)
- pip install "ipython[notebook]"
 - python3-zmq and libzmq1 were left over from previous installs when doing this last time. if you get errors with above, try installing them
- (dont think we need this) - apt-get install ipython3 ipython3-notebook (for some reason this install libzmq1, prolly cuz dependencies are handled by apt-get and it doesnt know any better)
- make sure ipython is using latest python version
- copy Adafruit stuff (rename - to \_, add __init__.py) to /usr/local/lib/python3.4/site-packages/
https://pypi.python.org/pypi/smbus-cffi/0.4.1
- sudo apt-get install build-essential libi2c-dev i2c-tools python-dev
- sudo pip3 install cffi
- sudo pip3 install smbus-cffi

