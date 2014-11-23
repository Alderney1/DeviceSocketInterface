#--------------------------------------------------------------------
#Administration Details
#--------------------------------------------------------------------
__author__ = "Mats Larsen"
__copyright__ = "Mats Larsen 2014"
__credits__ = ["Mats Larsen"]
__license__ = "GPLv3"
__maintainer__ = "Mats Larsen"
__email__ = "larsen.mats.87@gmail.com"
__status__ = "Development"
__description__ = "This module is a device interface over socket to a sensor device."
__file__ = "device_interface.py"
__class__ = "DeviceSocketInterface"
__dependencies__ = [""]
#--------------------------------------------------------------------
#Version
#--------------------------------------------------------------------
__version_stage__ = "alpha"
__version_number__ = "0.1"
__version_date__ = "20140917"
__version_modification__ = ""
__version_next_update__ = ""
#--------------------------------------------------------------------
#Hardware
#--------------------------------------------------------------------
"""
The hardware for this uart project is device that have a ip-adresse, which means it can be connected over socket.
"""
#--------------------------------------------------------------------
#IMPORT
#--------------------------------------------------------------------
import traceback
import threading
import socket
import sys
import time
#--------------------------------------------------------------------
#CONSTANTS
#--------------------------------------------------------------------
LOG_LEVEL = 2 # Information level
ALWAYS_LOG_LEVEL = 1 # print always
#--------------------------------------------------------------------
#METHODS
#--------------------------------------------------------------------
def log(self,msg, log_level=LOG_LEVEL):
    """Print a message, and track, where the log is invoked
    Input:
    -msg: message to be printed, ''
    -log_level: informationlevel, i"""
    global LOG_LEVEL
    if log_level <= LOG_LEVEL:
        print(str(log_level) + ' : ' + FILEREC + ' ::' +
              traceback.extract_stack()[-2][2] + ' : ' + msg)

class DeviceSocketInterface(threading.Thread):
    """Class to receive data from the ati box"""
    class Error(Exception):
        """Exception class."""
        def __init__(self, message):
            self.message = message
            Exception.__init__(self, self.message)
        def __repr__(self):
            return self.message

    def __init__(self,host=None,port=None,**args):
        """
        The constructor if the interface class.
        Input:
        host-> string:IP adress to the host.
        port-> int: Port number to the host
        """
        #Assignment
        self.__host = host # host to connect to realtime
        self.__port = port # port to the sensor
        self.__timeout = args.get('socket_timeout',1.0) # socket timeout
        self.__name = args.get('name','Invalid')
        self.__timestamps = args.get('timestamps',False)
        self.__log_level = args.get('log_level',2)
        #Threading
        threading.Thread.__init__(self) # initialize the thread
        self.daemon = True
        #socket to the sensor connection
        self.__sockATI = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__sockATI.settimeout(self._socket_timeout)
        #Event
        self.__rec_event = threading.Event() # event for received data
        self.__thread_init = threading.Event() # status for the thread
        self.__thread_terminated = threading.Event() # when thread is terminated.
        #Reset variables
        self.__received = None
        self.__timelist = None
        self.__rec_event.clear()
        self.__thread_init.clear()
        self.__thread_terminated.clear()
        self.start()
        log(__class__ + ' : ' + self.__name + ' is created.', ALWAYS_LOG_LEVEL)


    def __del__(self):
        """Close the socket connection."""
        self.__sockATI.close()
        log(__class__ + ' : ' + self.__name + ' is destroyed', ALWAYS_LOG_LEVEL)

    def send_data(self, data):
        """
        Sending custom made data to the device.
        """
        self.__sockATI.sendto(data,(self.__host,self.__port))


    def get_data(self, sync=True, timeout=0.5):
        """Property will return recevied from the sensor.
        Input:
        - sync. If true it will wait until the event will be set, it
        means that new sensor data is received. If false, it is
        async and will just return the current value.
        - timeout, indicate how long it should wait for event.
        0 = forever.
        Output:
        - revieced, sensor data, None for timeout."""
        if self._rec_event.isSet(): # if event is  set from the run
            self._rec_event.clear() # clear the flag
            return self._received   # return sensor data
        elif sync == True: # if sync is enabled
            if self._rec_event.wait(timeout): # wait for event or timeout
                self._rec_event.clear() # clear flag
                return self._received
            else:
                return None # None for timeout happen
        else: # async
            return self._received
   

    def run(self):
        """Thread will get the new input from the sensor, and set the
        event to true. Continueouly update received
        """
        self.log(__class__ + ' : ' + self._name + ' is RUNNING', ALWAYS_LOG_LEVEL)
        self._thread_init.set() # set the thread to be alive

        while self._thread_init.isSet() == True:
            """Will only run if thread is set to alive, if it's false
            the run method will end, and this means the thread will
            be terminated."""
            try:
                self.__received = self.__sockATI.recv(2048) # get reciced
                self.__rec_event.set() # flag for recived data
                
                if self.__timestamps: # If write timestamps to file is true
                    self.__freq_info()
                              
                log('recived data',self._log_level)
            except socket.timeout: # socket timeout based on the arg
                pass

        log('ATI_Reciver ' + self._name + ' is stopped', ALWAYS_LOG_LEVEL)
        if self._timelist:
            self._timelist.close() # close the timestamps file
            log('Close timestamps receiver', self._log_level)

        self._thread_terminated.set()
        self.log(__class__ + ' : ' + self._name + ' is ENDING', ALWAYS_LOG_LEVEL)


    def __freq_info(self):
        """Measure the timestamps, write to a file."""
        if self.__timelist == None:
            self.__timelist = open('Timestamps_' + time.strftime("%H%M%S"), 'w')
            self.__prev = float((time.time() * 1))
        else:
            new = float((time.time()*1))
            self.__timelist.write(str((new - self.__prev)) + '\n' )
            self.__prev = new

    def stop(self):
        """Stop the thread."""
        log(__class__ + ' : ' + self._name + 'is trying to STOP', ALWAYS_LOG_LEVEL)
        self.__thread_init.clear()

    def wait_startup(self,timeout=None):
        """Wait to this thread is started up, expect
        if a timeout is given.
        Inputs:
        timeout:float-> timeout given in secs."""
        if self.__thread_init.wait(timeout):
            return True
        else:
            return False

    def wait_terminated(self,timeout=None):
        """Wait to this thread is terminated, expect
        if a timeout is given.
        Inputs:
        timeout:float-> timeout given in secs."""
        self.stop()
        if self.__thread_terminated.wait(timeout):
            return True
        else:
            return False


