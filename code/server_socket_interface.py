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
__file__ = "server_socket_interface.py"
__class__ = "ServerSocketInterface"
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
The hardware for this uart project is device that have a ip-address, which means it can be connected over socket.
"""
#--------------------------------------------------------------------
#IMPORT
#--------------------------------------------------------------------
import traceback
import threading
import socket
import sys
import time
import numpy as np
#--------------------------------------------------------------------
#CONSTANTS
#--------------------------------------------------------------------
LOG_LEVEL = 2 # Information level
ALWAYS_LOG_LEVEL = 1 # print always
#--------------------------------------------------------------------
#METHODS
#--------------------------------------------------------------------
def log(msg, log_level=LOG_LEVEL):
    """Print a message, and track, where the log is invoked
    Input:
    -msg: message to be printed, ''
    -log_level: information level, i"""
    global LOG_LEVEL
    if log_level <= LOG_LEVEL:
        print(str(log_level) + ' : ' + __file__ + '.py ::' +
              traceback.extract_stack()[-2][2] + ' : ' + msg)
    
class ServerSocketInterface(threading.Thread):
    """Class to receive data from the ati box"""
    class Error(Exception):
        """Exception class."""
        def __init__(self, message):
            self.message = message
            Exception.__init__(self, self.message)
        def __repr__(self):
            return self.message
        
    class ClientHandler(threading.Thread):
        def __init__(self,conn,addr, **kwargs):
            """
            """
            #Assignment
            self.__conn = conn
            self.__addr = addr
            self.__name = kwargs.get('name','Invalid')
            self.__log_level = kwargs.get('log_level',2)
             #Threading
            threading.Thread.__init__(self) # initialize the thread
            self.daemon = True
            self.start()
        log(self.__class__ + ' : ' + self.__sc + ' : ' + self.__name + ' is created.', ALWAYS_LOG_LEVEL)

        def run(self):
             self.__thread_init.set() # set the thread to be alive
             log(__class__ + ' : ' + self.__name + ' is RUNNING', ALWAYS_LOG_LEVEL)

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
        self.__timeout = args.get('timeout',10.0) # socket timeout
        self.__name = args.get('name','Invalid')
        self.__max_clients = kwargs.get('max_clients',1)
        self.__timestamps = args.get('timestamps',False)
        self.__log_level = args.get('log_level',2)
        #local assignment
        self.__clients = []
        #Threading
        threading.Thread.__init__(self) # initialize the thread
        self.daemon = True
        #socket to the sensor connection
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__sock.settimeout(self.__timeout)
        self.__sock.bind((self.__host,self.__port))
        self.__sock.listen(self.__max_clients)
        
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
        log(__class__ + ' : ' + self.__sc + ' : ' + self.__name + ' is created.', ALWAYS_LOG_LEVEL)

    def run(self):
        """Thread will get the new input from the sensor, and set the
        event to true. Continuously update received
        """
        connection = None
        self.__thread_init.set() # set the thread to be alive
        log(__class__ + ' : ' + self.__name + ' is RUNNING', ALWAYS_LOG_LEVEL)
        if self.__thread_init:
            print('Sand')
        while self.__thread_init.isSet() == True:
            """Will only run if thread is set to alive, if it's false
            the run method will end, and this means the thread will
            be terminated."""
            con, addr = self.__sock.accept()
            self.__client.append(self.ClientHandler(conn=conn,addr=addr,name='Client'))

            try:
                self.__received = self.__sock.recv(1024) # get received
                self.__rec_event.set() # flag for recived data
                if self.__timestamps: # If write timestamps to file is true
                    self.__freq_info()    
            except socket.timeout: # socket timeout based on the arg
                log('Timeout data',self.__log_level)
                pass
           

                if connection == None:
                    connection, client_address = self.__sock.accept()
                    data = connection.recv(16)
   
        log('ATI_Reciver ' + self.__name + ' is stopped', ALWAYS_LOG_LEVEL)
        if self._timelist:
            self._timelist.close() # close the timestamps file
            log('Close timestamps receiver', self._log_level)

        self._thread_terminated.set()
        self.log(__class__ + ' : ' + self._name + ' is ENDING', ALWAYS_LOG_LEVEL)

