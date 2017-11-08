# *******************************************************************************************
# message client program - interactively generate requests to message server, displaying outputs
#
# parameters:
# -.  argv[1] - host to which to send requests (default: localhost)
# -.  argv[2] - port to which to send requests (default: 8881)
# -.  argv[3] - port on current host for accepting asynchronous responses (default: 8882)
# -.  argv[4] - timeout for current host to check for asynchronous responses (default: 15 seconds)
#
# effect: accepts requests from command line, issuing them and showing results
#
#  all requests and responses are one line long, newline terminated.
#  supported requests are as follows:
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
#  responses to requests have a two-part form:
#  -.  status - either OK or error
#  -.  body - if present, a characterization of the request's particulars:  i.e.,
#      -.  a description of a request error
#      -.  for qs_for_reader and qs_for_writer, the queues to which the user has subscribed
# *******************************************************************************************

import socket
import threading

# *************************************************************
# threads for managing concurrent activity
# *************************************************************

# =============================================================
# one client thread for generating and issuing requests
# =============================================================
#
def request_loop(server_host, server_well_known_port, client_timeout):
  reqlocal = threading.local()                                           # container for thread-local data
  while True:
    reqlocal.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # enable TCP connection
    reqlocal.sock.settimeout(20)                                           # put 20 second timeout on the socket to prevent indefinite execution
    reqlocal.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    # allow reuse of local addresses, for fast restart upon client termination
    reqlocal.request = input('enter next request ("exit" to end): ')
    if reqlocal.request == 'exit':  
      print('ending - program may take up to {} seconds to shut down'.format(client_timeout))
      break
    try:
      reqlocal.sock.connect((server_host, server_well_known_port))
      try:            # use file interface for message exchange
        reqlocal.infile, reqlocal.outfile = reqlocal.sock.makefile(mode='r'), reqlocal.sock.makefile(mode='w')
        try:          # do the request/response
          reqlocal.outfile.writelines([reqlocal.request+'\n'])
          reqlocal.outfile.flush()
          try:
            reqlocal.response = reqlocal.infile.readline()                 # get response from server
            print('read {}'.format(reqlocal.response),file=sys.stderr)     # show it for diagnostic purposes
          except Exception as e:
            print('?? client: couldn\'t read from server{} - exiting'.format('' if 'value' not in dir(e) else ' '+e.value), file=sys.stderr)
            break
        except Exception as e:
          print('?? client: couldn\'t write to server{} - exiting'.format('' if 'value' not in dir(e) else ' '+e.value), file=sys.stderr)
          break
        finally:
          reqlocal.infile.close()
          reqlocal.outfile.close()
      except Exception as e:
        print('?? client: couldn\'t access socket to server{} - exiting'.format('' if 'value' not in dir(e) else ' '+e.value), file=sys.stderr)
        break
    except Exception as e:
      print('?? client: couldn\'t connect to ({},{}):{}; exiting'.format(server_host, server_well_known_port, '' if 'value' not in dir(e) else ' '+e.value), file=sys.stderr)
    reqlocal.sock.close()


# ================================================================================
# one client thread for fielding and displaying messages from message server
# ================================================================================
#
stop_flag = False    # signal need to cease checking for async responses when request_loop ceases

def async_response_loop(well_known_port, timeout):
  asynclocal = threading.local()                                           # container for thread-local data
  try:
    asynclocal.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     # create a socket.
    asynclocal.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # allow reuse of local addresses, for fast restart upon server termination
    asynclocal.sock.settimeout(timeout)                                     # timeout at 15 second intervals so as to allow for checking of stop flag
    try:
      #
      # 
      asynclocal.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      #
      # associate socket with well-known port (8881) on current host ('')
      asynclocal.sock.bind(('', well_known_port))
      try:
        #
        # set the number of clients waiting for a connection that the server can bind at once
        asynclocal.sock.listen(5)
        try:
          print('accepting connections on port {}'.format(well_known_port))
          while True:
            try:
              asynclocal.newSocket, asynclocal.address = asynclocal.sock.accept()   # timeout at 15 second intervals so as to allow for checking of stop fla
              print('async loop: now connected to {}'.format(asynclocal.address))
              asynclocal.newSocket.settimeout(15)                                   # timeout at 15 second intervals so as to allow for checking of stop flag
              asynclocal.newSocketAsFile = asynclocal.newSocket.makefile(mode="r")
              try:
                while True:
                  print('Message from {}: {}'.format(asynclocal.address, asynclocal.newSocketAsFile.readline()))
              except:
                pass
              finally:
                print('no longer connected to {}'.format(asynclocal.address))
              asynclocal.newSocket.close()
              if stop_flag: break
            except socket.timeout:
              pass
            except:
              print('can\'t field asynchronous responses ({}) - exiting'.format(type(e)))
              break
            if stop_flag: break
        except Exception as e:
          print('can\'t field asynchronous responses ({}) - exiting'.format(type(e)))
        asynclocal.sock.close()
      except Exception as e:
        print('can\'t listen on socket for fielding responses ({}) - exiting'.format(type(e)))
    except Exception as e:
      print('can\'t bind socket for fielding async responses to {} ({}) - exiting'.format(well_known_port, type(e)))
  except Exception as e:
    print('can\'t create socket for fielding async responses ({}) - exiting'.format(type(e)))


# **************************************
# program main
# **************************************

# =======================================
# process command line arguments
# =======================================
#
import sys
try:
  server_host = sys.argv[1]
  server_well_known_port = int(sys.argv[2])
  client_well_known_port = int(sys.argv[3])
  client_timeout = int(sys.argv[4])
except:
  server_host = 'localhost'
  server_well_known_port = 8881
  client_well_known_port = 8882
  client_timeout = 15

# ************************************************************
# kick off threads
# ************************************************************
#
asyncsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

request_loop_thread = threading.Thread(name='request_loop', target=request_loop, args=(server_host, server_well_known_port, client_timeout))
async_thread = threading.Thread(name='async_response_loop', target=async_response_loop, args=(client_well_known_port, client_timeout))

async_thread.start()
request_loop_thread.start()
request_loop_thread.join()
stop_flag = True               # when the request loop closes, signal the async thread that it's time to shut down the program
async_thread.join()

