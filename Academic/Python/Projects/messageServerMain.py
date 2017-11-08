# *******************************************************************************************
# message service program - field and respond to requests from message clients
# ----------------------------------------------------------------------------
#
# *. operating instructions
#    ----------------------
#
#    invoke as   
#       python messageServerMain.py  (port  (timeout))
#
#    preconditions for program execution:
#    *.  the presence of the Python 3 command interpreter, python, in a directory in the 
#        command line's PATH variable  (note: tested with Python 3.4.2)
#    *.  the presence of the program's supporting library, messageServerLibrary.py,
#        in Python's import path, sys.path.  (By default, sys.path includes the current directory).
#    *.  firewall access for localhost and a TCP port for communication with client
#        programs  (default: 8881)
#
# *. command line parameters
#    -----------------------
#
#    -.  argv[1] - port on current host for accepting requests (default: 8881)
#    -.  argv[2] - idle timeout, in seconds (default: 30)
#        the program will shut itself down after this many seconds if it receives no requests
#
# *. effect
#    ------
#
#    respond to requests relating to organizing, capturing, and distributing
#    messages from client programs.
#
#    all requests that this program services and responses that it generates are one-line-long,
#    newline-terminated texts.  the supported requests and their formats are as follows:
#
#     register_q  q_name  -
#        register q_name as an active message queue
#     set_reader_for_q  q_reader q_name  host port -
#        register q_reader as a reader of q_name: i.e.,
#        -.  send any messages accumulated in q_name to q_reader at TCP connection (host, port) immediately
#        -.  send messages to (host, port) as they're added to q_name
#        q_name must have been previously registered
#     set_writer_for_q  q_writer  q_name  -
#        register q_writer as a writer of q_name
#        q_name must have been previously registered
#     qs_for_reader q_reader -
#        return a list of queues for which q_reader has registered as a reader
#     qs_for_writer q_writer -
#        return a list of queues for which q_writer has registered as a writer
#     append_message_to_q q_name q_writer message -
#        append message to q_name.  q_writer must be registered as a writer for q_name
#     unset_reader_for_q  q_reader q_name  -
#        unregister q_reader as a reader of q_name
#     unset_writer_for_q  q_writer q_name   -
#        unregister q_writer as a reader of q_name
#     unset_communicator  q_entity  -
#        unregister q_entity as a user of all queues, removing q_entity's SAP
#     unregister_q  q_name  -
#        unregister q_name as an active message queue, removing all readers and writers
#
# *.  details
#     -------
#
#    the message queues that this program establishes on behalf of its clients persist only as 
#    long as this program operates.
#
#    all responses to client requests have a two-part form:
#      status  (body)
#    where 
#      -.  status - leading field; either OK or error
#      -.  body - if present, a characterization of the request's particulars:  i.e.,
#          -.  a description of a request error
#          -.  for qs_for_reader and qs_for_writer, the queues to which the user has subscribed
#
# *.  other
#     -----
#
#     as of 4/27/15, this program has been tested ... somewhat.  testing has included
#     -.  the testing of the supporting library against a test program, messageServerTests.py,
#         that 
#         -.  applies a series of unit tests to the library's classes, under the assumption that
#         -.  the program is running on a Windows platform
#         see the header for messageServerTests.py for details
#     -.  the interactive testing of the main program with a companion client program,
#         messageClientMain.py, up to but not including the testing of the logic for
#         asynchronous message delivery and capture.
#
#     for an implementation of a companion client program, see messageClientMain.py
#
# -- Phil Pfeiffer
#    27 April 2015
# *******************************************************************************************

# supporting codes for the message server
#
from messageServerLibrary import *

# **************************************
# process command line arguments
# **************************************
#
import sys
try:
  well_known_port = int(sys.argv[1])
  timeout = float(sys.argv[2])
except:
  well_known_port = 8881    # for accepting requests
  timeout = 2500             # length that server sits idle, in seconds

# ************************************************************
# set up datasets, handler for serving client requests
# ************************************************************
#
queue_to_readers, queue_to_writers, reader_to_SAP  = MessageQueueToReaders(), MessageQueueToWriters(), CommunicatorToSAP()
handler = RequestHandler(RequestDispatcher(queue_to_readers, queue_to_writers, reader_to_SAP))

# ************************************************************
# set up network machinery for serving client requests
# ************************************************************
#
# create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
# allow reuse of local addresses, for fast restart upon server termination
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#
# set timeout to prevent indefinite python interpreter keyboard lockup
sock.settimeout(timeout)
#
# associate socket with well-known port (8881) on current host ('')
sock.bind(('', well_known_port))
#
# set the number of clients waiting for a connection that the server can bind at once
sock.listen(5)
print('accepting connections on port {} with a {}-second timeout'.format(well_known_port, timeout))

# ************************************************************
# loop for servicing requests
# ************************************************************
try:
  while 1:
    newSocket, address = sock.accept()
    print("Connected from {}".format(address))
    request_as_seen, request_type, status, response = handler.respond( newSocket )
    print("Request <{}> handled: type = {}, status = {}, response = {}".format(request_as_seen.rstrip(), request_type, status, response))
    newSocket.close()
except Exception as e:
  print('?? exception detected of type {}{}: exiting'.format(type(e), '' if 'value' not in dir(e) else ": "+e.value))
finally:
  sock.close()

