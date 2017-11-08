# *******************************************************************************************
# message service library test program - test the classes in messageServerLibrary.py
# ----------------------------------------------------------------------------------
#
# *. operating instructions
#    ----------------------
#
#    invoke as   
#       python messageServerTests.py  (port  (timeout))
#
#    preconditions for program execution:
#    *.  the presence of the Python 3 command interpreter, python, in a directory in the 
#        command line's PATH variable  (note: tested with Python 3.4.2)
#    *.  the presence of the program's supporting library, messageServerLibrary.py,
#        in Python's import path, sys.path.  (By default, sys.path includes the current directory).
#    *.  firewall access for localhost and a TCP port for communication with client
#        programs  (default: 8881)
#    *.  a platform that supports a DOSshell-like command interpreter:  i.e.,
#        -.  ability to execute platform commands using syntax like "cmd /c ...some command..."
#        -.  support for a 'del foo.txt'  command that (e.g.) deletes foo.txt
#    *.  ability to create, execute, and delete two files
#        -.  c:\temp\testserver.txt
#        -.  c:\temp\testclient.txt
#
# *. command line parameters
#    -----------------------
#
#     none
#
# *. effect
#    ------
#
#     use doctest to run unit tests against the programs messageServerLibrary.py.
#     if testing succeeds, you should see advisory messages - nothing more.
#
# *. details
#    -------
#
#     the message queues that this program establishes on behalf of its clients persist only as 
#     long as this program operates.
#
#     all responses to client requests have a two-part form:
#       status  (body)
#     where 
#      -.  status - leading field; either OK or error
#      -.  body - if present, a characterization of the request's particulars:  i.e.,
#          -.  a description of a request error
#          -.  for qs_for_reader and qs_for_writer, the queues to which the user has subscribed
#
# *.  other
#     -------
#
#     as of 4/27/15, this program has been successfully run to completion 
#
# -- Phil Pfeiffer
#    27 April 2015
# *******************************************************************************************

# supporting codes for the message server
#
from messageServerLibrary import *

# ###########################################################################################################
# test codes for messaging service
# ###########################################################################################################

# ============================================================================================================
# values for running unit tests
# ============================================================================================================

import doctest
def doctest_it(f, verbosity=False):
  doctest.run_docstring_examples(f, None, optionflags=doctest.ELLIPSIS|doctest.NORMALIZE_WHITESPACE, verbose=verbosity)

run_tests_on_load = True

# ************************************************************************************************************
# utility classes
# ************************************************************************************************************

# ==================================================================================================================
# test code for InvertibleMap class
#
# -- second set of tests also tests AddMapMethodAliases mixin
# ==================================================================================================================

# ---------------------------------------------------------------------------------------------
# first set of tests:  test operation up to but not including __getattr__-supported aliasing
# ---------------------------------------------------------------------------------------------
#
def invertible_map_test_no_aliasing(void):
  """
  >>> testMap = InvertibleMap()             # set up empty map - should return none
  >>> repr(testMap)
  "InvertibleMap(**{'forward_map': {}})"
  >>> eval(repr(testMap)) == testMap        # basic memoization test
  True
  >>> testMap.register('a','x')             # register first element
  >>> testMap
  InvertibleMap(**{'forward_map': {'a': {'x'}}})
  >>> eval(repr(testMap)) == testMap        # with-content memoization test
  True
  >>> testMap.codomain_elements_for_domain_element('a')    # check for correctness of ('a', {'x'}) binding
  {'x'}
  >>> testMap.domain_elements_for_codomain_element('a')
  set()
  >>> testMap.codomain_elements_for_domain_element('x')
  set()
  >>> testMap.domain_elements_for_codomain_element('x')
  {'a'}
  >>> testMap.register('a', 'y')                           # check for correctness of ('a', {'x', 'y'}) binding
  >>> testMap.codomain_elements_for_domain_element('a') == {'x', 'y'}
  True
  >>> testMap.register('b', 'w')
  >>> testMap.register('b', 'x')
  >>> testMap.register('b', 'z')
  >>> testMap.register('a', 'w')                           # should now have ('a', {'w', 'x', 'y'}) and ('b', {'w', 'x', 'z'})
  >>> testMap.domain_elements() == {'a', 'b'}                            # check that domain element retrieval works
  True
  >>> testMap.codomain_elements() == {'w', 'x', 'y', 'z'}                # check that codomain element retrival works
  True
  >>> testMap.codomain_elements_for_domain_element('a') == {'w', 'x', 'y'}    # check forward mappings for 'a', 'b'
  True
  >>> testMap.codomain_elements_for_domain_element('b') == {'w', 'x', 'z'}
  True
  >>> testMap.domain_elements_for_codomain_element('w') == {'a', 'b'}    # check inverse mappings for 'w', 'x', 'y', 'z'
  True
  >>> testMap.domain_elements_for_codomain_element('x') == {'a', 'b'}
  True
  >>> testMap.domain_elements_for_codomain_element('y') == {'a'}
  True
  >>> testMap.domain_elements_for_codomain_element('z') == {'b'}
  True
  >>> testMap.unregister('a', 'w')                                       # check single binding unregistration
  >>> testMap.codomain_elements_for_domain_element('a') == {'x', 'y'}
  True
  >>> testMap.codomain_elements_for_domain_element('b') == {'w', 'x', 'z'}
  True
  >>> testMap.unregister_codomain_element('x')                            # check codomain element unregistration
  >>> testMap.codomain_elements_for_domain_element('a') == {'y'}
  True
  >>> testMap.codomain_elements_for_domain_element('b') == {'w', 'z'}
  True
  >>> testMap.unregister_domain_element('a')                              # check domain element unregistration
  >>> testMap.codomain_elements_for_domain_element('a')
  set()
  >>> testMap.codomain_elements_for_domain_element('b') == {'w', 'z'}
  True
  """
  pass

if 'run_tests_on_load' in dir() and 'doctest_it' in dir():
  if run_tests_on_load:
    print('testing InvertibleMap - no alias test')
    doctest_it(invertible_map_test_no_aliasing)


# ---------------------------------------------------------------------------------------------
# second set of tests:  rerun first set with 'foo' alias for domain, 'bar' alias for codomain
# ---------------------------------------------------------------------------------------------
#
def invertible_map_test_with_aliasing(void):
   """
   >>> testMap = InvertibleMap(entity_aliases=[(('domain_element', 'foo'), ('codomain_element', 'bar'))])         # set up empty map - should return none
   >>> testMap.foos() == set()             # check for empty map
   True
   >>> testMap.bars() == set()
   True
   >>> eval(repr(testMap)) == testMap        # basic memoization test
   True
   >>> testMap.register('a','x')             # register first element
   >>> eval(repr(testMap)) == testMap        # string-check memoization test of map with content
   True
   >>> testMap.bars_for_foo('a')             # check for correctness of ('a', {'x'}) binding
   {'x'}
   >>> testMap.foos_for_bar('a')
   set()
   >>> testMap.bars_for_foo('x')
   set()
   >>> testMap.foos_for_bar('x')
   {'a'}
   >>> testMap.register('a', 'y')                           # check for correctness of ('a', {'x', 'y'}) binding
   >>> testMap.bars_for_foo('a') == {'x', 'y'}
   True
   >>> testMap.register('b', 'w')
   >>> testMap.register('b', 'x')
   >>> testMap.register('b', 'z')
   >>> testMap.register('a', 'w')                           # should now have ('a', {'w', 'x', 'y'}) and ('b', {'w', 'x', 'z'})
   >>> testMap.foos() == {'a', 'b'}                         # check that domain element retrieval works
   True
   >>> testMap.bars() == {'w', 'x', 'y', 'z'}               # check that codomain element retrival works
   True
   >>> testMap.bars_for_foo('a') == {'w', 'x', 'y'}    # check forward mappings for 'a', 'b'
   True
   >>> testMap.bars_for_foo('b') == {'w', 'x', 'z'}
   True
   >>> testMap.foos_for_bar('w') == {'a', 'b'}         # check inverse mappings for 'w', 'x', 'y', 'z'
   True
   >>> testMap.foos_for_bar('x') == {'a', 'b'}
   True
   >>> testMap.foos_for_bar('y') == {'a'}
   True
   >>> testMap.foos_for_bar('z') == {'b'}
   True
   >>> testMap.unregister('a', 'w')                    # check single binding unregistration
   >>> testMap.bars_for_foo('a') == {'x', 'y'}
   True
   >>> testMap.bars_for_foo('b') == {'w', 'x', 'z'}
   True
   >>> testMap.unregister_bar('x')                     # check codomain element unregistration
   >>> testMap.bars_for_foo('a') == {'y'}
   True
   >>> testMap.bars_for_foo('b') == {'w', 'z'}
   True
   >>> testMap.unregister_foo('a')                     # check domain element unregistration
   >>> testMap.bars_for_foo('a')
   set()
   >>> testMap.bars_for_foo('b') == {'w', 'z'}
   True
   """
   pass

if 'run_tests_on_load' in dir() and 'doctest_it' in dir():
  if run_tests_on_load:
    print('*** testing InvertibleMap - with aliasing')
    doctest_it(invertible_map_test_with_aliasing)
    print()


# ************************************************************************************************************
# test codes for classes for binding message collections to their defining properties: i.e.,
# -.  their associated  buffers
# -.  the names of the entities that use them
# ************************************************************************************************************

# ============================================================================================================
# test code for MessageBuffer class
# ============================================================================================================

def message_buffer_test(void):
   """
   >>> buf = MessageBuffer()        # start with empty buffer
   >>> buf
   MessageBuffer(**{'buffer': []})
   >>> eval(repr(buf)) == buf       # basic memoization test
   True
   >>> buf.append_message('foo')            # add a message
   >>> buf
   MessageBuffer(**{'buffer': ['foo']})
   >>> eval(repr(buf)) == buf               # memoization test with content
   True
   >>> buf.retrieve_message(0)              # check for message that's there
   'foo'
   >>> buf.retrieve_message(1)              # check for message that's not there
   >>> buf.append_message('bar')            # try appending a second message
   >>> buf
   MessageBuffer(**{'buffer': ['foo', 'bar']})
   """
   pass

if 'run_tests_on_load' in dir() and 'doctest_it' in dir():
  if run_tests_on_load:
    print('*** testing MessageBuffer')
    doctest_it(message_buffer_test)
    print()

# ============================================================================================================
# test code for MessageBufferCollection class
# ============================================================================================================

def message_buffer_collection_test(void):
   """
   >>> buf = MessageBufferCollection(**{'buffers': {}})      # start with empty collection  (note: clear to remove possible residue from earlier tests)
   >>> buf
   MessageBufferCollection(**{'buffers': {}})
   >>> eval(repr(buf)) == buf       # basic memoization test
   True
   >>> buf.is_registered('foo')     # confirm that 'foo' isn't registered
   False
   >>> buf.register('foo')          # add buffer 'foo'
   >>> buf.is_registered('foo')     # confirm that 'foo' is now registered
   True
   >>> buf
   MessageBufferCollection(**{'buffers': {'foo': MessageBuffer(**{'buffer': []})}})
   >>> buf.append_message('foo','m1')     # add 1st message to buffer
   >>> buf
   MessageBufferCollection(**{'buffers': {'foo': MessageBuffer(**{'buffer': ['m1']})}})
   >>> buf.append_message('foo','m2')     # add 2nd message to buffer
   >>> buf
   MessageBufferCollection(**{'buffers': {'foo': MessageBuffer(**{'buffer': ['m1', 'm2']})}})
   >>> eval(repr(buf)) == buf             # non-trivial memoization test
   True
   >>> buf.retrieve_message('foo',0)      # retrieve messages from buffer
   'm1'
   >>> buf.retrieve_message('foo',1)      # retrieve messages from buffer
   'm2'
   >>> buf.retrieve_message('foo',2)      # retrieve messages from buffer
   >>> buf.register('foo')                # attempt to reregister foo - check for message on stderr, which doctest won't catch
   >>> buf.register('bar')                # add a second buffer
   >>> buf.buffers() == { 'foo', 'bar' }  # confirm buffer name function correctness
   True
   >>> buf.retrieve_message('bar',0)      # retrieve message from empty buffer
   >>> buf.unregister('foo')              # unregister 'foo', check result
   >>> buf
   MessageBufferCollection(**{'buffers': {'bar': MessageBuffer(**{'buffer': []})}})
   """
   pass

if 'run_tests_on_load' in dir() and 'doctest_it' in dir():
  if run_tests_on_load:
    print('*** testing MessageBufferCollection')
    doctest_it(message_buffer_collection_test)
    print()

# ======================================================================================================================
# test code for MessageBufferToUsers -- class that associates buffers in a message buffer collection with a user
# ======================================================================================================================

# ......................................................................................................................
# test code for MessageBufferToUsers class
# -.  lacking:  tests for append_message()
# -.  aliasing feature tested by subclasses
#
def message_buffer_to_users_test(void):
   """
   >>> buf = MessageBufferToUsers(**{'buffers': {}, 'buffer_to_users': {}})      # start with empty collection  (note: clear to remove possible residue from earlier tests)
   >>> buf.buffers()
   set()
   >>> buf.users()
   set()
   >>> buf.buffers_for_user('w1')
   set()
   >>> buf.users_for_buffer('foo')
   set()
   >>> eval(repr(buf)) == buf        # basic memoization test
   True
   >>> buf.register('foo', 'w1')     # attempt to register a user for an unregistered buffer.  should fail, generating message to stderr
   False
   >>> buf.register_buffer('foo')    # add a buffer
   >>> buf.register('foo', 'w1')     # register two users for this buffer.  should succeed
   True
   >>> buf.register('foo', 'w2')
   True
   >>> buf.register_buffer('bar')     # register another buffer with two users.
   >>> buf.register_buffer('bar')     # reregistration should write to cerr, but otherwise have no effect
   >>> buf.register('bar', 'w2')      # should succeed
   True
   >>> buf.register('bar', 'w3')
   True
   >>> buf.buffers() == {'foo', 'bar'}
   True
   >>> buf.users_for_buffer('foo') == {'w1', 'w2'}
   True
   >>> buf.users_for_buffer('bar') == {'w2', 'w3'}
   True
   >>> buf.users() == {'w1', 'w2', 'w3'}
   True
   >>> buf.buffers_for_user('w1') == {'foo'}
   True
   >>> buf.buffers_for_user('w2') == {'foo', 'bar'}
   True
   >>> buf.buffers_for_user('w3') == {'bar'}
   True
   >>> eval(repr(buf)) == buf        # more complex memoization test
   True
   >>> buf.unregister_user('w3')     # check unregistering one user
   >>> buf.buffers() == {'foo', 'bar'}
   True
   >>> buf.users() == {'w1', 'w2'}
   True
   >>> buf.users_for_buffer('bar') == {'w2'}
   True
   >>> buf.buffers_for_user('w3') == set()
   True
   >>> buf.unregister_buffer('bar')     # check unregistering one buffer
   >>> buf.buffers() == {'foo'}
   True
   >>> buf.users() == {'w1', 'w2'}
   True
   >>> buf.users_for_buffer('bar') == set()
   True
   >>> buf.buffers_for_user('w2') == { 'foo' }
   True
   >>> buf.unregister('foo', 'w1')     # check unregistering one buffer/user combo
   >>> buf.buffers() == { 'foo' }
   True
   >>> buf.users() == {'w1', 'w2'}
   True
   >>> buf.users_for_buffer('foo') == { 'w2' }
   True
   >>> buf.buffers_for_user('w1') == set()
   True
   """
   pass

if 'run_tests_on_load' in dir() and 'doctest_it' in dir():
  if run_tests_on_load:
    print('*** testing MessageBufferToUsers')
    doctest_it(message_buffer_to_users_test)
    print()

# =================================================================================================================================
# test code for MessageQueueToWriters --
#     class that associates buffers (a.k.a. queues) in a message buffer collection with an append-only user (i.e., writer)
# ===============================================================================================================================

# ......................................................................................................................
# >>> lacking:  tests for append_message()
#
def message_queue_to_writers_test(void):
   """
   >>> buf = MessageQueueToWriters(**{'buffers': {}, 'buffers_to_users': {}})      # start with empty collection  (note: clear to remove possible residue from earlier tests)
   >>> buf.queues()
   set()
   >>> buf.writers()
   set()
   >>> buf.queues_for_writer('w1')
   set()
   >>> buf.writers_for_queue('foo')
   set()
   >>> eval(repr(buf)) == buf        # basic memoization test
   True
   >>> buf.register('foo', 'w1')     # attempt to register a writer for an unregistered queue.  should fail, generating message to stderr
   False
   >>> buf.register_queue('foo')     # add a queue
   >>> buf.register('foo', 'w1')     # register two writers for this queue.  should succeed
   True
   >>> buf.register('foo', 'w2')
   True
   >>> buf.register_queue('bar')     # register another queue with two writers.
   >>> buf.register_queue('bar')     # reregistration should write to cerr, but otherwise have no effect
   >>> buf.register('bar', 'w2')     # should succeed
   True
   >>> buf.register('bar', 'w3')
   True
   >>> buf.queues() == {'foo', 'bar'}
   True
   >>> buf.writers_for_queue('foo') == {'w1', 'w2'}
   True
   >>> buf.writers_for_queue('bar') == {'w2', 'w3'}
   True
   >>> buf.writers() == {'w1', 'w2', 'w3'}
   True
   >>> buf.queues_for_writer('w1') == {'foo'}
   True
   >>> buf.queues_for_writer('w2') == {'foo', 'bar'}
   True
   >>> buf.queues_for_writer('w3') == {'bar'}
   True
   >>> eval(repr(buf)) == buf        # more complex memoization test
   True
   >>> buf.unregister_writer('w3')     # check unregistering one writer
   >>> buf.queues() == {'foo', 'bar'}
   True
   >>> buf.writers() == {'w1', 'w2'}
   True
   >>> buf.writers_for_queue('bar') == {'w2'}
   True
   >>> buf.queues_for_writer('w3') == set()
   True
   >>> buf.unregister_queue('bar')     # check unregistering one queue
   >>> buf.queues() == {'foo'}
   True
   >>> buf.writers() == {'w1', 'w2'}
   True
   >>> buf.writers_for_queue('bar') == set()
   True
   >>> buf.queues_for_writer('w2') == { 'foo' }
   True
   >>> buf.unregister('foo', 'w1')     # check unregistering one queue/writer combo
   >>> buf.queues() == { 'foo' }
   True
   >>> buf.writers() == {'w1', 'w2'}
   True
   >>> buf.writers_for_queue('foo') == { 'w2' }
   True
   >>> buf.queues_for_writer('w1') == set()
   True
   """
   pass

run_tests_on_load = True

if 'run_tests_on_load' in dir() and 'doctest_it' in dir():
  if run_tests_on_load:
    print('*** testing MessageQueueToWriters')
    doctest_it(message_queue_to_writers_test)
    print()

# =================================================================================================================================
# test code for MessageQueueToReaders --
#     class that associates buffers (a.k.a. queues) in a message buffer collection with a serial access user (i.e., reader)
# note:  these are really streams, since they associate per-reader "current message" indices with each queue
# ===============================================================================================================================

# ......................................................................................................................
# >>> lacking:  tests for next_message()
#
def message_queue_to_readers_test(void):
   """
   >>> buf = MessageQueueToReaders(**{'buffers': {}, 'buffer_to_users': {}})      # start with empty collection  (note: clear to remove possible residue from earlier tests)
   >>> buf.queues()
   set()
   >>> buf.readers()
   set()
   >>> buf.queues_for_reader('w1')
   set()
   >>> buf.readers_for_queue('foo')
   set()
   >>> eval(repr(buf)) == buf        # basic memoization test
   True
   >>> buf.register('foo', 'w1')     # attempt to register a reader for an unregistered queue.  should fail, generating message to stderr
   False
   >>> buf.register_queue('foo')     # add a queue
   >>> buf.register('foo', 'w1')     # register two readers for this queue.  should succeed
   True
   >>> buf.register('foo', 'w2')
   True
   >>> buf.register_queue('bar')     # register another queue with two readers.
   >>> buf.register_queue('bar')     # reregistration should write to cerr, but otherwise have no effect
   >>> buf.register('bar', 'w2')     # should succeed
   True
   >>> buf.register('bar', 'w3')
   True
   >>> buf.queues() == {'foo', 'bar'}
   True
   >>> buf.readers_for_queue('foo') == {'w1', 'w2'}
   True
   >>> buf.readers_for_queue('bar') == {'w2', 'w3'}
   True
   >>> buf.readers() == {'w1', 'w2', 'w3'}
   True
   >>> buf.queues_for_reader('w1') == {'foo'}
   True
   >>> buf.queues_for_reader('w2') == {'foo', 'bar'}
   True
   >>> buf.queues_for_reader('w3') == {'bar'}
   True
   >>> buf.unregister_reader('w3')     # check unregistering one reader
   >>> buf.queues() == {'foo', 'bar'}
   True
   >>> buf.readers() == {'w1', 'w2'}
   True
   >>> buf.readers_for_queue('bar') == {'w2'}
   True
   >>> buf.queues_for_reader('w3') == set()
   True
   >>> eval(repr(buf)) == buf        # more complex memoization test
   True
   >>> buf.unregister_queue('bar')     # check unregistering one queue
   >>> buf.queues() == {'foo'}
   True
   >>> buf.readers() == {'w1', 'w2'}
   True
   >>> buf.readers_for_queue('bar') == set()
   True
   >>> buf.queues_for_reader('w2') == { 'foo' }
   True
   >>> buf.unregister('foo', 'w1')     # check unregistering one queue/reader combo
   >>> buf.queues() == { 'foo' }
   True
   >>> buf.readers() == {'w1', 'w2'}
   True
   >>> buf.readers_for_queue('foo') == { 'w2' }
   True
   >>> buf.queues_for_reader('w1') == set()
   True
   """
   pass

if 'run_tests_on_load' in dir() and 'doctest_it' in dir():
  if run_tests_on_load:
    print('*** testing MessageQueueToReaders')
    doctest_it(message_queue_to_readers_test)
    print()

# =================================================================================================================================
# test code for CommunicatorToSAP --
#     class that associates named users with (host, port) pairs
# ===============================================================================================================================

def communicator_to_SAP_test(void):
   """
   >>> buf = CommunicatorToSAP(**{'communicator_to_SAP': {}})      # start with empty collection  (note: clear to remove possible residue from earlier tests)
   >>> buf
   CommunicatorToSAP(**{'communicator_to_SAP': {}})
   >>> buf.communicators()
   set()
   >>> eval(repr(buf)) == buf     # basic repr test
   True
   >>> buf.register('foo', 'myhost', '1.1.1.1')
   >>> buf
   CommunicatorToSAP(**{'communicator_to_SAP': {'foo': ('myhost', '1.1.1.1')}})
   >>> buf.SAP('foo') == ('myhost', '1.1.1.1')
   True
   >>> buf.register('bar', 'yourhost', '1.2.3.4')
   >>> eval(repr(buf)) == buf    # more complex repr test
   True
   >>> buf.communicators() == {'foo', 'bar'}
   True
   >>> buf.unregister('foo')
   >>> buf.communicators() == {'bar'}
   True
   >>> buf.SAP('foo')
   >>> buf.SAP('bar') == ('yourhost', '1.2.3.4')
   True
   """
   pass

if 'run_tests_on_load' in dir() and 'doctest_it' in dir():
  if run_tests_on_load:
    print('*** testing CommunicatorToSAP')
    doctest_it(communicator_to_SAP_test)
    print()

# ************************************************************************************************************
# tests for classes for exchanging one-line messages with other processes
# ************************************************************************************************************

# =================================================================================================================================
# test code for MessageExchanger --
#     class that supports communication with other entities via two half-duplex files, one line at a time.
#
# preconditions for test execution:
# *.  a platform that supports a DOSshell-like command interpreter:  i.e.,
# -.  ability to execute platform commands using syntax like "cmd /c ...some command..."
# -.  support for a 'type foo.txt' command that (e.g.) outputs foo.txt to stdout
# -.  support for a 'del foo.txt'  command that (e.g.) deletes foo.txt
# *.  ability to create, delete two files - c:\temp\testin.txt, c:\temp\testout.txt
# ===============================================================================================================================

import subprocess
import functools

def message_exchanger_test(void):
  """
  >>> source_py_syntax = 'C:/temp/testin.txt'       # the Python files API (open(), close(), etc.) seems to require / separators
  >>> target_py_syntax = 'C:/temp/testout.txt'
  >>> testin = open(source_py_syntax, mode="w")     # set up test
  >>> testin_text  = []
  >>> testin_text += ['testing 1-2-3\\n' ]
  >>> testin_text += ['testing 4-5-6\\n' ]
  >>> testin_text += ['testing 7-8-9-10\\n' ]
  >>> testin.writelines( testin_text )
  >>> testin.close()
  >>> testin  = open(source_py_syntax, mode="r")
  >>> testout = open(target_py_syntax, mode="w")
  >>> buf = MessageExchanger(**{'infile': testin, 'outfile': testout})
  >>> ( status, line ) = buf.get_line()
  >>> ( status, line )
  (True, 'testing 1-2-3\\n')
  >>> buf.put_line( line )
  True
  >>> ( status, line ) = buf.get_line()
  >>> ( status, line )
  (True, 'testing 4-5-6\\n')
  >>> buf.put_line( line )
  True
  >>> ( status, line ) = buf.get_line()
  >>> ( status, line )
  (True, 'testing 7-8-9-10\\n')
  >>> buf.put_line( line )
  True
  >>> testin.close()
  >>> testout.close()
  >>> source_win_syntax = source_py_syntax.replace("/","\\\\")      # the windows API requires \ separators
  >>> target_win_syntax = target_py_syntax.replace("/","\\\\")
  >>> # type is a built-in and must be invoked via the shell
  >>> subprocess.check_output(["cmd", "/c", "type", source_win_syntax], universal_newlines=True)  == '{}'.format(functools.reduce(lambda s, n: s+n, testin_text, ""))
  True
  >>> subprocess.call(["cmd", "/c", "del", source_win_syntax])   # del is a built-in and must be invoked via the shell
  0

  >>> subprocess.call(["cmd", "/c", "del", target_win_syntax])
  0

  """
  pass


if 'run_tests_on_load' in dir() and 'doctest_it' in dir():
  if run_tests_on_load:
    print('*** testing MessageExchanger')
    doctest_it(message_exchanger_test)
    print()

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# GenerateSubprocess:  supporting class for subprocess generation:
#
# class's
# *. __init__ method generates a process by
# -.  writing content to a specified file
# -.  executing that file, using Python
# *. terminate method
# -.  stops the proces
# -.  deletes the file
#
# preconditions for process execution:
# *.  a platform that supports a DOSshell-like command interpreter:  i.e.,
# -.  ability to execute platform commands using syntax like "cmd /c ...some command..."
# -.  support for a 'del foo.txt'  command that (e.g.) deletes foo.txt
# *.  presence of Python command interpreter, python, in directory in PATH variable
#
# Notes:
# -.  host_file argument must use Python syntax - e.g., c:/temp/foo.py
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class GenerateSubprocess(object):
  def __init__(self, host_file_name, host_file_code):
    self.host_file_name = host_file_name
    try:
      host_file = open(host_file_name, mode="w")     # create file for program
      host_file.writelines( host_file_code )
      host_file.close()                              # program code now written
      self.host_file_built = True
      try:
        self.proc = subprocess.Popen(["cmd", "/c", "python", self.windows_syntax(self.host_file_name)])   # start the program.  the windows API requires \ separators
        self.subprocess_started = True
      except Exception as e:
        print('?? {}: can\'t start process {}'.format(self.__class__.__name__, self.windows_syntax(self.host_file_name)))
        self.subprocess_started = False
    except:
      print('?? {}: can\'t open {} for writing'.format(self.__class__.__name__, self.windows_syntax(self.host_file_name)))
      self.host_file_built = False
  def terminate(self):
    if self.host_file_built:
      if self.subprocess_started:  self.proc.terminate()
      subprocess.call(["cmd", "/c", "del", self.windows_syntax(self.host_file_name)])   # del, a built-in, must be invoked via the shell.  also, the windows API requires \ separators
  #
  # auxiliary routines
  def windows_syntax(self,filename):  return filename.replace("/", "\\")


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# TestServer:  supporting class for testing client communications:
#
# class generate a process that
# -.  binds to a specified port on the current host
# -.  reads a "request" on that port
# -.  displays incoming connection and message
# -.  responds to request with initial "OK " + prefix
# -.  displays response
# -.  exits
# Notes:
# -.  host_file argument must use Python syntax - e.g., c:/temp/foo.py
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#
class TestServer(object):
  #
  def __init__(self, server_code_file, well_known_port=8881, response_prefix = "***"):
    self.proc_handle = GenerateSubprocess( server_code_file, self.build_server_code(well_known_port, response_prefix) )
  def terminate(self):
    self.proc_handle.terminate()
  #
  # auxiliary routines
  #
  # build the code, parameterized by well_known_port
  def build_server_code( self, well_known_port, response_prefix ):
    server_code  = [ ]
    server_code += [ "import sys\n" ]
    server_code += [ "import socket\n" ]
    server_code += [ "sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # enable TCP connection\n" ]
    server_code += [ "sock.settimeout(30)                                           # put 30 second timeout on the socket to prevent indefinite execution\n" ]
    server_code += [ "sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    # allow reuse of local addresses, for fast restart upon server termination\n" ]
    server_code += [ "well_known_port = {}\n".format(well_known_port) ]
    server_code += [ "try:\n" ]
    server_code += [ "  sock.bind(('', well_known_port))\n" ]
    server_code += [ "  sock.listen(1)    # set the number of clients waiting for a connection that the server can bind at once\n" ]
    server_code += [ "  try:              # get one connection, exchange messages, and quit\n" ]
    server_code += [ "    newSocket, address = sock.accept()\n" ]
    server_code += [ "    print('Connected from {}'.format(address))\n" ]
    server_code += [ "    newSocket.settimeout(10)                                  # put 10 second timeout on the socket to prevent indefinite execution\n" ]
    server_code += [ "    try:            # use file interface for message exchange\n" ]
    server_code += [ "      infile, outfile = newSocket.makefile(mode='r'), newSocket.makefile(mode='w')\n" ]
    server_code += [ "      try:          # do the exchange\n" ]
    server_code += [ "        input = infile.readline()                                # get input from client\n" ]
    server_code += [ "        print('server: read {}'.format(input),file=sys.stderr)   # show it for diagnostic purposes\n" ]
    server_code += [ "        try:          # do the exchange\n" ]
    server_code += [ "          response = 'OK ' + {} + input + '\\{}'               # echo input to client with initial OK, prefix\n".format('"'+response_prefix+'"', 'n') ]
    server_code += [ "          outfile.writelines(response)\n" ]
    server_code += [ "          outfile.flush()\n" ]
    server_code += [ "          print('server: wrote {}'.format(response),file=sys.stderr)    # show it for diagnostic purposes\n" ]
    server_code += [ "        except Exception as e:\n" ]
    server_code += [ "          print('?? server: couldn\\\'t write to client{} - exiting'.format('' if 'value' not in dir(e) else ' '+e.value), file=sys.stderr)\n" ]
    server_code += [ "      except Exception as e:\n" ]
    server_code += [ "        print('?? server: couldn\\\'t read from client{} - exiting'.format('' if 'value' not in dir(e) else ' '+e.value), file=sys.stderr)\n" ]
    server_code += [ "      finally:\n" ]
    server_code += [ "        infile.close()\n" ]
    server_code += [ "        outfile.close()\n" ]
    server_code += [ "    except Exception as e:\n" ]
    server_code += [ "      print('?? server: couldn\\\'t access socket to client{} - exiting'.format('' if 'value' not in dir(e) else ' '+e.value), file=sys.stderr)\n" ]
    server_code += [ "    finally:\n" ]
    server_code += [ "      newSocket.close()\n" ]
    server_code += [ "  except Exception as e:\n" ]
    server_code += [ "    print('?? server: couldn\\\'t process connection{} - exiting'.format('' if 'value' not in dir(e) else ' '+e.value), file=sys.stderr)\n" ]
    server_code += [ "  finally:\n" ]
    server_code += [ "    sock.close()\n" ]
    server_code += [ "except Exception as e:\n" ]
    server_code += [ "  print('?? server: couldn\\\'t bind to {}:{}; exiting'.format(well_known_port, '' if 'value' not in dir(e) else ' '+e.value), file=sys.stderr)\n" ]
    return server_code


# =================================================================================================================================
# test code for OpenSocketMessageExchanger --
#     class that supports communication with other entities via two half-duplex files, one line at a time.
#
# preconditions for test execution:
# *.  a platform that supports a DOSshell-like command interpreter:  i.e.,
# -.  ability to execute platform commands using syntax like "cmd /c ...some command..."
# -.  support for a 'del foo.txt'  command that (e.g.) deletes foo.txt
# *.  presence of Python 3 command interpreter, python, in directory in PATH variable
# *.  ability to create, delete one file - c:\temp\testserver.txt
# *.  firewall access for localhost, port 8881
# ===============================================================================================================================

import subprocess
import socket
import sys

# -----------------------------------------------------------------------------------------------------------------------------
# test code for the exchanger proper
# -----------------------------------------------------------------------------------------------------------------------------
#
def open_socket_message_exchanger_test(void):
  """
  Test the open socket message exchanger class by creating a server program on the fly, then trading messages with it
  >>> server_py_syntax = 'C:/temp/testserver.py'             # the Python files API (open(), close(), etc.) seems to require / separators
  >>> well_known_port = 8881                                 # server port for message exchange
  >>> response_prefix = "***"                                # prefix for distinguishing client request from server response
  >>> test_server = TestServer(server_py_syntax, well_known_port, response_prefix)
  >>> # ... ... now that server is started, communicate with it
  >>> sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  >>> sock.settimeout(10)                                    # timeout in seconds
  >>> sock.connect(('localhost', well_known_port))
  >>> exchanger = OpenSocketMessageExchanger(sock)
  >>> test_message = "etaoin shrdlu\\n"
  >>> request_status = exchanger.put_line(test_message)
  >>> request_status
  True
  >>> response = (False, None) if not request_status else exchanger.get_line()
  >>> parsed_response = (False, None) if not (request_status and response[0]) else (response[1].split(" ")[0] == "OK", None if " " not in response[1] else (response[1].split(" ", maxsplit=1))[1])
  >>> parsed_response[0] == request_status
  True
  >>> parsed_response[1] == response_prefix + test_message if parsed_response[0] else None
  True
  >>> exchanger.close()
  >>> # ... ... done; terminate the dialogue
  >>> test_server.terminate()
  """
  pass

if 'run_tests_on_load' in dir() and 'doctest_it' in dir():
  if run_tests_on_load:
    print('*** testing OpenSocketMessageExchanger')
    doctest_it(open_socket_message_exchanger_test)
    print()

# =================================================================================================================================
# test code for (Service Access Point) SAPMessageExchanger --
#     class that uses a (host, port) pair to generate a socket message exchanger
#
# preconditions for test execution:
# *.  a platform that supports a DOSshell-like command interpreter:  i.e.,
# -.  ability to execute platform commands using syntax like "cmd /c ...some command..."
# -.  support for a 'del foo.txt'  command that (e.g.) deletes foo.txt
# *.  presence of Python 3 command interpreter, python, in directory in PATH variable
# *.  ability to create, delete one file - c:\temp\testserver.txt
# *.  firewall access for localhost, port 8881
# ===============================================================================================================================

import subprocess
import socket
import sys

def sap_message_exchanger_test(void):
  """
  Test the SAP message exchanger class by creating a server program on the fly, then trading messages with it
  >>> server_py_syntax = 'C:/temp/testserver.py'             # the Python files API (open(), close(), etc.) seems to require / separators
  >>> well_known_port = 8881                                 # server port for message exchange
  >>> response_prefix = "***"                                # prefix for distinguishing client request from server response
  >>> test_server = TestServer(server_py_syntax, well_known_port, response_prefix)
  >>> # ... ... now that server is started, communicate with it
  >>> exchanger = SAPMessageExchanger(**{ 'hostport' : ('localhost', well_known_port), 'timeout': 10 })
  >>> test_message = "etaoin shrdlu\\n"
  >>> request_status = exchanger.put_line(test_message)
  >>> request_status
  True
  >>> response = (False, None) if not request_status else exchanger.get_line()
  >>> parsed_response = (False, None) if not (request_status and response[0]) else (response[1].split(" ")[0] == "OK", None if " " not in response[1] else (response[1].split(" ", maxsplit=1))[1])
  >>> parsed_response[0] == request_status
  True
  >>> parsed_response[1] == response_prefix + test_message if parsed_response[0] else None
  True
  >>> exchanger.close()
  >>> # ... ... done; terminate the dialogue
  >>> test_server.terminate()
  """

if 'run_tests_on_load' in dir() and 'doctest_it' in dir():
  if run_tests_on_load:
    print('*** testing SAPMessageExchanger')
    doctest_it(sap_message_exchanger_test)
    print()

# ************************************************************************************************************
# test classes for parsing and responding to the bodies of requests of known types
# ************************************************************************************************************

# -----------------------------------------------------------------------------------------------------------------------------
# test for RegisterQueue -
#    class that replies to a request whose body is of the from   queue
# -----------------------------------------------------------------------------------------------------------------------------

def register_queue_test(void):
  """
  Test the register queue class by getting it to register a queue
  >>> #
  >>> # ... ... specify datasets for capturing results of request ... ...
  >>> # start with empty collection, to remove possible residue from earlier tests)
  >>> queue_to_readers = MessageQueueToReaders(**{'buffers': {}, 'buffer_to_users': {}})
  >>> queue_to_writers = MessageQueueToWriters(**{'buffers': {}, 'buffer_to_users': {}})
  >>> request_reactor = RegisterQueue(**{'queue_to_readers': queue_to_readers, 'queue_to_writers': queue_to_writers})
  >>> #
  >>> # ... ... initialize test datasets:  must register the queue in order to unregister ot
  >>> queue = 'q_bert'
  >>> queue_to_readers.queues() == set()    # ... ... confirm initialization ... ...
  True
  >>> queue_to_writers.queues() == set()
  True
  >>> #
  >>> # ... ... register the queue ... ...
  >>> request = queue + "  "
  >>> request_reactor(request)
  (True, None)
  >>> #
  >>> # ... ... confirm unregistration ... ...
  >>> queue_to_readers.queues() == { queue }
  True
  >>> queue_to_writers.queues() == { queue }
  True
  """

if 'run_tests_on_load' in dir() and 'doctest_it' in dir():
  if run_tests_on_load:
    print('*** testing RegisterQueue')
    doctest_it(register_queue_test)
    print()

# -----------------------------------------------------------------------------------------------------------------------------
# test for RegisterReaderForQueue -
#    class that replies to a request whose body is of the from   reader .. queue .. SAP
# -----------------------------------------------------------------------------------------------------------------------------

def register_reader_for_queue_test(void):
  """
  Test the register queue to reader class by getting it to register a message
  >>> #
  >>> # ... ... specify datasets for capturing results of request ... ...
  >>> # start with empty collection, to remove possible residue from earlier tests)
  >>> reader_to_SAP = CommunicatorToSAP(**{'communicator_to_SAP': {}})
  >>> queue_to_readers = MessageQueueToReaders(**{'buffers': {}, 'buffer_to_users': {}})
  >>> request_reactor = RegisterReaderForQueue(**{'communicator_to_SAP': reader_to_SAP, 'queue_to_readers': queue_to_readers})
  >>> #
  >>> # ... ... initialize test datasets:  must register the queue in order to register the reader
  >>> reader, queue, host, port = 'reader_foo', 'q_bert', 'host_baz', '1234'
  >>> queue_to_readers.register_queue(queue)
  >>> queue_to_readers.queues() == { queue }    # ... ... confirm initialization ... ...
  True
  >>> queue_to_readers.queues_for_reader( reader ) == set()
  True
  >>> queue_to_readers.readers() == set()
  True
  >>> queue_to_readers.readers_for_queue( queue ) == set()
  True
  >>> reader_to_SAP.SAP(reader) == None
  True
 >>> #
  >>> # ... ... register the reader ... ...
  >>> request = reader + "  " + queue + " " + host + " " + port
  >>> request_reactor(request)
  (True, None)
  >>> #
  >>> # ... ... confirm registration ... ...
  >>> queue_to_readers.queues() == { queue }    # ... ... confirm initialization ... ...
  True
  >>> queue_to_readers.queues_for_reader( reader ) == { queue }
  True
  >>> queue_to_readers.readers() == { reader }
  True
  >>> queue_to_readers.readers_for_queue( queue ) == { reader }
  True
  >>> reader_to_SAP.SAP(reader) == (host, port)
  True
  """

if 'run_tests_on_load' in dir() and 'doctest_it' in dir():
  if run_tests_on_load:
    print('*** testing RegisterReaderForQueue')
    doctest_it(register_reader_for_queue_test)
    print()

# -----------------------------------------------------------------------------------------------------------------------------
# test for RegisterWriterForQueue -
#    class that replies to a request whose body is of the from   writer .. queue
# -----------------------------------------------------------------------------------------------------------------------------

def register_writer_for_queue_test(void):
  """
  Test the register queue to writer class by getting it to register a message
  >>> #
  >>> # ... ... specify datasets for capturing results of request ... ...
  >>> # start with empty collection, to remove possible residue from earlier tests)
  >>> queue_to_writers = MessageQueueToWriters(**{'buffers': {}, 'buffer_to_users': {}})
  >>> request_reactor = RegisterWriterForQueue(**{'queue_to_writers': queue_to_writers})
  >>> #
  >>> # ... ... initialize test datasets:  must register the queue in order to register the writer
  >>> writer, queue = 'writer_foo', 'q_bert'
  >>> queue_to_writers.register_queue(queue)
  >>> queue_to_writers.queues() == { queue }    # ... ... confirm initialization ... ...
  True
  >>> queue_to_writers.queues_for_writer( writer ) == set()
  True
  >>> queue_to_writers.writers() == set()
  True
  >>> queue_to_writers.writers_for_queue( queue ) == set()
  True
  >>> #
  >>> # ... ... register the writer ... ...
  >>> request = writer + "  " + queue
  >>> request_reactor(request)
  (True, None)
  >>> #
  >>> # ... ... confirm registration ... ...
  >>> queue_to_writers.queues() == { queue }    # ... ... confirm initialization ... ...
  True
  >>> queue_to_writers.queues_for_writer( writer ) == { queue }
  True
  >>> queue_to_writers.writers() == { writer }
  True
  >>> queue_to_writers.writers_for_queue( queue ) == { writer }
  True
  """

if 'run_tests_on_load' in dir() and 'doctest_it' in dir():
  if run_tests_on_load:
    print('*** testing RegisterWriterForQueue')
    doctest_it(register_writer_for_queue_test)
    print()

# -----------------------------------------------------------------------------------------------------------------------------
# test for QueuesForReader -
#    class that replies to a request whose body is of the from   reader
# -----------------------------------------------------------------------------------------------------------------------------

def queues_for_reader_test(void):
  """
  Test the queues for reader class by registering two readers, checking for registration
  >>> #
  >>> # ... ... specify datasets for capturing results of request ... ...
  >>> # start with empty collection, to remove possible residue from earlier tests)
  >>> queue_to_readers = MessageQueueToReaders(**{'buffers': {}, 'buffer_to_users': {}})
  >>> request_reactor = QueuesForReader(**{'queue_to_readers': queue_to_readers})
  >>> reader, queue1, queue2 = 'reader_foo', 'q_bert', 'q_qq'
  >>> #
  >>> # ... ... initialize test datasets:  must register the queue in order to register the readers
  >>> queue_to_readers.register_queue(queue1)
  >>> queue_to_readers.register_queue(queue2)
  >>> queue_to_readers.register(queue1, reader)
  True
  >>> queue_to_readers.register(queue2, reader)
  True
  >>> queue_to_readers.queues() == { queue1, queue2 }    # ... ... confirm initialization ... ...
  True
  >>> queue_to_readers.queues_for_reader( reader ) == { queue1, queue2 }
  True
  >>> queue_to_readers.readers() == { reader }
  True
  >>> queue_to_readers.readers_for_queue( queue1 ) == { reader }
  True
  >>> queue_to_readers.readers_for_queue( queue2 ) == { reader }
  True
  >>> #
  >>> # ... ... obtain the queues for reader data ... ...
  >>> request = reader + " "
  >>> (status, response) = request_reactor(request)
  >>> #
  >>> # ... ... confirm data ... ...
  >>> (status == True) and (response in ["{} {} ".format(queue1, queue2), "{} {} ".format(queue2, queue1)])
  True
  """

if 'run_tests_on_load' in dir() and 'doctest_it' in dir():
  if run_tests_on_load:
    print('*** testing QueuesForReader')
    doctest_it(queues_for_reader_test)
    print()

# -----------------------------------------------------------------------------------------------------------------------------
# test for  -
#    class that replies to a request whose body is of the from   writer
# -----------------------------------------------------------------------------------------------------------------------------

def queues_for_writer_test(void):
  """
  Test the queues for writer class by registering two writers, checking for registration
  >>> #
  >>> # ... ... specify datasets for capturing results of request ... ...
  >>> # start with empty collection, to remove possible residue from earlier tests)
  >>> queue_to_writers = MessageQueueToWriters(**{'buffers': {}, 'buffer_to_users': {}})
  >>> request_reactor = QueuesForWriter(**{'queue_to_writers': queue_to_writers})
  >>> writer, queue1, queue2 = 'writer_foo', 'q_bert', 'q_qq'
  >>> #
  >>> # ... ... initialize test datasets:  must register the queue in order to register the writers
  >>> queue_to_writers.register_queue(queue1)
  >>> queue_to_writers.register_queue(queue2)
  >>> queue_to_writers.register(queue1, writer)
  True
  >>> queue_to_writers.register(queue2, writer)
  True
  >>> queue_to_writers.queues() == { queue1, queue2 }    # ... ... confirm initialization ... ...
  True
  >>> queue_to_writers.queues_for_writer( writer ) == { queue1, queue2 }
  True
  >>> queue_to_writers.writers() == { writer }
  True
  >>> queue_to_writers.writers_for_queue( queue1 ) == { writer }
  True
  >>> queue_to_writers.writers_for_queue( queue2 ) == { writer }
  True
  >>> #
  >>> # ... ... obtain the queues for writer data ... ...
  >>> request = writer + " "
  >>> (status, response) = request_reactor(request)
  >>> #
  >>> # ... ... confirm data ... ...
  >>> (status == True) and (response in ["{} {} ".format(queue1, queue2), "{} {} ".format(queue2, queue1)])
  True
  """

if 'run_tests_on_load' in dir() and 'doctest_it' in dir():
  if run_tests_on_load:
    print('*** testing QueuesForWriter')
    doctest_it(queues_for_writer_test)
    print()

# -----------------------------------------------------------------------------------------------------------------------------
# test for AppendMessageToQueue -
#    class that replies to a request whose body is of the from   writer .. queue
# -----------------------------------------------------------------------------------------------------------------------------

def append_message_to_queue_test(void):
  """
  Test the append message to queue class by registering a queue and a writer for the queue, appending a message, and checking queue content
  Missing - tests of auto-push to readers functionality
  >>> #
  >>> # ... ... specify datasets for capturing results of request ... ...
  >>> # start with empty collection, to remove possible residue from earlier tests)
  >>> reader_to_SAP = CommunicatorToSAP(**{'communicator_to_SAP': {}})
  >>> queue_to_readers = MessageQueueToReaders(**{'buffers': {}, 'buffer_to_users': {}})
  >>> queue_to_writers = MessageQueueToWriters(**{'buffers': {}, 'buffer_to_users': {}})
  >>> request_reactor = AppendMessageToQueue(**{'queue_to_writers': queue_to_writers, 'communicator_to_SAP': reader_to_SAP, 'queue_to_readers': queue_to_readers})
  >>> #
  >>> # ... ... initialize test datasets:  must register the queue and the writer to the queue in order to add a message
  >>> writer, queue, message = 'writer_foo', 'q_bert', 'this is a message'
  >>> queue_to_writers.register_queue(queue)
  >>> queue_to_writers.register(queue, writer)
  True
  >>> queue_to_writers.queues() == { queue }    # ... ... confirm initialization ... ...
  True
  >>> queue_to_writers.queues_for_writer( writer ) == { queue }
  True
  >>> queue_to_writers.writers() == { writer }
  True
  >>> queue_to_writers.writers_for_queue( queue ) == { writer }
  True
  >>> #
  >>> # ... ... append the message ... ...
  >>> request = writer + "  " + queue + " " + message
  >>> request_reactor(request)
  (True, None)
  >>> #
  >>> # ... ... confirm append ... ...
  >>> queue_to_writers.queues() == { queue }
  True
  >>> queue_to_writers.queues_for_writer( writer ) == { queue }
  True
  >>> queue_to_writers.writers() == { writer }
  True
  >>> queue_to_writers.writers_for_queue( queue ) == { writer }
  True
  >>> queue_to_writers.retrieve_message(queue, 0) == 'this is a message'
  True
  """

if 'run_tests_on_load' in dir() and 'doctest_it' in dir():
  if run_tests_on_load:
    print('*** testing AppendMessageToQueue')
    doctest_it(append_message_to_queue_test)
    print()

# -----------------------------------------------------------------------------------------------------------------------------
# test for UnregisterReaderFromQueue -
#    class that replies to a request whose body is of the from   reader .. queue
# -----------------------------------------------------------------------------------------------------------------------------

def unregister_reader_from_queue_test(void):
  """
  Test the unregister reader from queue class by getting it to unregister a reader
  >>> #
  >>> # ... ... specify datasets for capturing results of request ... ...
  >>> # start with empty collection, to remove possible residue from earlier tests)
  >>> queue_to_readers = MessageQueueToReaders(**{'buffers': {}, 'buffer_to_users': {}})
  >>> request_reactor = UnregisterReaderFromQueue(**{'queue_to_readers': queue_to_readers})
  >>> #
  >>> # ... ... initialize test datasets:  must register the queue and the reader to the queue in order to unregister the reader
  >>> reader, queue = 'reader_foo', 'q_bert'
  >>> queue_to_readers.register_queue(queue)
  >>> queue_to_readers.register(queue, reader)
  True
  >>> queue_to_readers.queues() == { queue }    # ... ... confirm initialization ... ...
  True
  >>> queue_to_readers.queues_for_reader( reader ) == { queue }
  True
  >>> queue_to_readers.readers() == { reader }
  True
  >>> queue_to_readers.readers_for_queue( queue ) == { reader }
  True
  >>> #
  >>> # ... ... unregister the reader ... ...
  >>> request = reader + "  " + queue + " "
  >>> request_reactor(request)
  (True, None)
  >>> #
  >>> # ... ... confirm unregistration ... ...
  >>> queue_to_readers.queues() == { queue }
  True
  >>> queue_to_readers.queues_for_reader( reader ) == set()
  True
  >>> queue_to_readers.readers() == { reader }
  True
  >>> queue_to_readers.readers_for_queue( queue ) == set()
  True
  """

if 'run_tests_on_load' in dir() and 'doctest_it' in dir():
  if run_tests_on_load:
    print('*** testing UnregisterReaderFromQueue')
    doctest_it(unregister_reader_from_queue_test)
    print()

# -----------------------------------------------------------------------------------------------------------------------------
# test for UnregisterQueueFromWriter -
#    class that replies to a request whose body is of the from   writer .. queue
# -----------------------------------------------------------------------------------------------------------------------------

def unregister_writer_from_queue_test(void):
  """
  Test the unregister writer from queue class by getting it to unregister a writer
  >>> #
  >>> # ... ... specify datasets for capturing results of request ... ...
  >>> # start with empty collection, to remove possible residue from earlier tests)
  >>> queue_to_writers = MessageQueueToWriters(**{'buffers': {}, 'buffer_to_users': {}})
  >>> request_reactor = UnregisterWriterFromQueue(**{'queue_to_writers': queue_to_writers})
  >>> #
  >>> # ... ... initialize test datasets:  must register the queue and the writer to the queue in order to unregister the writer
  >>> writer, queue = 'writer_foo', 'q_bert'
  >>> queue_to_writers.register_queue(queue)
  >>> queue_to_writers.register(queue, writer)
  True
  >>> queue_to_writers.queues() == { queue }    # ... ... confirm initialization ... ...
  True
  >>> queue_to_writers.queues_for_writer( writer ) == { queue }
  True
  >>> queue_to_writers.writers() == { writer }
  True
  >>> queue_to_writers.writers_for_queue( queue ) == { writer }
  True
  >>> #
  >>> # ... ... unregister the writer ... ...
  >>> request = writer + "  " + queue + " "
  >>> request_reactor(request)
  (True, None)
  >>> #
  >>> # ... ... confirm unregistration ... ...
  >>> queue_to_writers.queues() == { queue }
  True
  >>> queue_to_writers.queues_for_writer( writer ) == set()
  True
  >>> queue_to_writers.writers() == { writer }
  True
  >>> queue_to_writers.writers_for_queue( queue ) == set()
  True
  """

if 'run_tests_on_load' in dir() and 'doctest_it' in dir():
  if run_tests_on_load:
    print('*** testing UnregisterWriterFromQueue')
    doctest_it(unregister_writer_from_queue_test)
    print()

# -----------------------------------------------------------------------------------------------------------------------------
# test for UnregisterEntity -
#    class that replies to a request whose body is of the form   communicator
# -----------------------------------------------------------------------------------------------------------------------------

def unregister_entity_test(void):
  """
  Test the unregister entity class by getting it to unregister an entity from the reader and writer datasets
  >>> #
  >>> # ... ... specify datasets for capturing results of request ... ...
  >>> # start with empty collection, to remove possible residue from earlier tests)
  >>> reader_to_SAP = CommunicatorToSAP(**{'communicator_to_SAP': {}})
  >>> queue_to_readers = MessageQueueToReaders(**{'buffers': {}, 'buffer_to_users': {}})
  >>> queue_to_writers = MessageQueueToWriters(**{'buffers': {}, 'buffer_to_users': {}})
  >>> request_reactor = UnregisterEntity(**{'queue_to_readers': queue_to_readers, 'communicator_to_SAP': reader_to_SAP, 'queue_to_writers': queue_to_writers})
  >>> #
  >>> # ... ... initialize test datasets:  must register the queue and register the entity for queue in order to unregister the entity
  >>> entity, queue, host, port = 'mr_foo', 'q_bert', 'host_bar', 'port_baz'
  >>> # queue_to_readers.register_queue(queue) - don't need to register queue twice, since read and write queues are the same
  >>> queue_to_writers.register_queue(queue)
  >>> queue_to_readers.register(queue, entity)
  True
  >>> queue_to_writers.register(queue, entity)
  True
  >>> reader_to_SAP.register(entity, host, port)
  >>> queue_to_writers.queues() == { queue }    # ... ... confirm initialization ... ...
  True
  >>> queue_to_readers.queues_for_reader( entity ) == { queue }
  True
  >>> queue_to_writers.queues_for_writer( entity ) == { queue }
  True
  >>> queue_to_readers.readers() == { entity }
  True
  >>> queue_to_readers.readers_for_queue( queue ) == { entity }
  True
  >>> queue_to_writers.writers_for_queue( queue ) == { entity }
  True
  >>> reader_to_SAP.SAP( entity ) == ( host, port )
  True
  >>> #
  >>> # ... ... unregister the entity ... ...
  >>> request = entity + " "
  >>> request_reactor(request)
  (True, None)
  >>> #
  >>> # ... ... confirm unregistration ... ...
  >>> queue_to_writers.queues() == { queue }
  True
  >>> queue_to_readers.queues_for_reader( entity ) == set()
  True
  >>> queue_to_writers.queues_for_writer( entity ) == set()
  True
  >>> queue_to_writers.writers() == set()
  True
  >>> queue_to_readers.readers_for_queue( queue ) == set()
  True
  >>> queue_to_writers.writers_for_queue( queue ) == set()
  True
  >>> reader_to_SAP.SAP( entity ) == None
  True
  """

if 'run_tests_on_load' in dir() and 'doctest_it' in dir():
  if run_tests_on_load:
    print('*** testing UnregisterEntity')
    doctest_it(unregister_entity_test)
    print()

# -----------------------------------------------------------------------------------------------------------------------------
# test for UnregisterQueue -
#    class that replies to a request whose body is of the from   queue
# -----------------------------------------------------------------------------------------------------------------------------

def unregister_queue_test(void):
  """
  Test the unregister queue class by getting it to unregister a queue from the read and write queue datasets
  >>> #
  >>> # ... ... specify datasets for capturing results of request ... ...
  >>> # start with empty collection, to remove possible residue from earlier tests)
  >>> queue_to_readers = MessageQueueToReaders(**{'buffers': {}, 'buffer_to_users': {}})
  >>> queue_to_writers = MessageQueueToWriters(**{'buffers': {}, 'buffer_to_users': {}})
  >>> request_reactor = UnregisterQueue(**{'queue_to_readers': queue_to_readers, 'queue_to_writers': queue_to_writers})
  >>> #
  >>> # ... ... initialize test datasets:  must register the queue in order to unregister ot
  >>> queue = 'q_bert'
  >>> #queue_to_readers.register_queue(queue) - only need register once, since the queues are in a shared structure
  >>> queue_to_writers.register_queue(queue)
  >>> queue_to_readers.queues() == { queue }    # ... ... confirm initialization ... ...
  True
  >>> queue_to_writers.queues() == { queue }
  True
  >>> #
  >>> # ... ... unregister the queue ... ...
  >>> request = queue + "  "
  >>> request_reactor(request)
  (True, None)
  >>> #
  >>> # ... ... confirm unregistration ... ...
  >>> queue_to_readers.queues() == set()
  True
  >>> queue_to_writers.queues() == set()
  True
  """

if 'run_tests_on_load' in dir() and 'doctest_it' in dir():
  if run_tests_on_load:
    print('*** testing UnregisterQueue')
    doctest_it(unregister_queue_test)
    print()

# ************************************************************************************************************
# test classes for managing interactions with other processes via message exchange
# preconditions for test execution:
# *.  a platform that supports a DOSshell-like command interpreter:  i.e.,
# -.  ability to execute platform commands using syntax like "cmd /c ...some command..."
# -.  support for a 'del foo.txt'  command that (e.g.) deletes foo.txt
# *.  presence of Python 3 command interpreter, python, in directory in PATH variable
# *.  ability to create, delete one file - c:\temp\testserver.txt
# *.  firewall access for localhost, port 8881
# ************************************************************************************************************

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# TestClient:  supporting class for testing communications with external client:
#
# class generate a process that
# -.  writes a request to a specified (host, port)
# -.  displays incoming connection and message
# -.  responds to message with initial "OK " + prefix
# -.  displays response
# -.  exits

# -.  connects to a server on specified port
# -.  sends specified message
# -.  checks for specified response
# -.  exits
# Notes:
# -.  host_file argument must use Python syntax - e.g., c:/temp/foo.py
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class TestClient(object):
  #
  def __init__(self, client_code_file, host='localhost', well_known_port=8881, request=""):
    self.proc_handle = GenerateSubprocess( client_code_file, self.build_client_code(host, well_known_port, request) )
  def terminate(self):
    self.proc_handle.terminate()
  #
  # auxiliary routines
  #
  # build the code, parameterized by well_known_port
  def build_client_code( self, host, well_known_port, request ):
    client_code  = [ ]
    client_code += [ "import sys\n" ]
    client_code += [ "import socket\n" ]
    client_code += [ "sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # enable TCP connection\n" ]
    client_code += [ "sock.settimeout(20)                                           # put 20 second timeout on the socket to prevent indefinite execution\n" ]
    client_code += [ "sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    # allow reuse of local addresses, for fast restart upon client termination\n" ]
    client_code += [ "host, well_known_port, request = {!r}, {!r}, {!r}\n".format(host, well_known_port, request) ]
    client_code += [ "try:\n" ]
    client_code += [ "  sock.connect((host, well_known_port))\n" ]
    client_code += [ "  try:            # use file interface for message exchange\n" ]
    client_code += [ "    infile, outfile = sock.makefile(mode='r'), sock.makefile(mode='w')\n" ]
    client_code += [ "    try:          # do the request/response\n" ]
    client_code += [ "      outfile.writelines(request)\n" ]
    client_code += [ "      outfile.flush()\n" ]
    client_code += [ "      print('client: wrote {}'.format(request),file=sys.stderr)    # show it for diagnostic purposes\n" ]
    client_code += [ "      try:\n" ]
    client_code += [ "        response = infile.readline()                                # get response from server\n" ]
    client_code += [ "        print('client: read {}'.format(response),file=sys.stderr)   # show it for diagnostic purposes\n" ]
    client_code += [ "      except Exception as e:\n" ]
    client_code += [ "        print('?? client: couldn\\\'t read from server{} - exiting'.format('' if 'value' not in dir(e) else ' '+e.value), file=sys.stderr)\n" ]
    client_code += [ "    except Exception as e:\n" ]
    client_code += [ "      print('?? client: couldn\\\'t write to server{} - exiting'.format('' if 'value' not in dir(e) else ' '+e.value), file=sys.stderr)\n" ]
    client_code += [ "    finally:\n" ]
    client_code += [ "      infile.close()\n" ]
    client_code += [ "      outfile.close()\n" ]
    client_code += [ "  except Exception as e:\n" ]
    client_code += [ "    print('?? client: couldn\\\'t access socket to server{} - exiting'.format('' if 'value' not in dir(e) else ' '+e.value), file=sys.stderr)\n" ]
    client_code += [ "  finally:\n" ]
    client_code += [ "    sock.close()\n" ]
    client_code += [ "except Exception as e:\n" ]
    client_code += [ "  print('?? client: couldn\\\'t connect to ({},{}):{}; exiting'.format(host, well_known_port, '' if 'value' not in dir(e) else ' '+e.value), file=sys.stderr)\n" ]
    return client_code

# ============================================================================================================
# tests for RequestHandler -
#    class that represents an entity that uses a message exchanger to reply to a request
# ============================================================================================================

import subprocess
import socket
import sys

# -------------------------------------------------------------------------------------------------------------
# first tests: use dummy dispatcher to check basic responses
# -------------------------------------------------------------------------------------------------------------

def respond_to_request_dummy_dispatcher_test(void):
  """
  Test RequestHandler by creating a client program on the fly, then trading messages with it
  >>> #
  >>> # ... ... dispatcher checks for 'request' before space, leaves what follows after ... ...
  >>> dispatcher = lambda request, **kwargs: (request.split(' ')[0], request.split(' ')[0] == 'request', '' if ' ' not in request else request.split(' ',maxsplit=1)[1])
  >>> responder = RequestHandler( dispatcher )
  >>> #
  >>> # ... ... set up for simple server communications ... ...
  >>> sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # enable TCP connection
  >>> sock.settimeout(30)                                           # put 30 second timeout on the socket to prevent indefinite execution
  >>> sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    # allow reuse of local addresses, for fast restart upon server termination
  >>> well_known_port = 8881
  >>> #
  >>> # ... ... initiate the lightweight test server ... ...
  >>> sock.bind(('', well_known_port))
  >>> sock.listen(1)    # set the number of clients waiting for a connection that the server can bind at once
  >>> #
  >>> # ... ... set up a lightweight test client ... ...
  >>> client_py_syntax = 'C:/temp/testclient.py'             # the Python files API (open(), close(), etc.) seems to require / separators
  >>> request = "request response parameters\\n"             # request with parameters
  >>> test_client = TestClient(client_py_syntax, 'localhost', well_known_port, request)
  >>> #
  >>> # ... ... respond to message from client ... ...
  >>> newSocket, address = sock.accept()
  >>> print('Connected from {}'.format(address), file=sys.stderr)
  >>> newSocket.settimeout(30)
  >>> request_as_seen, request_type, status, response = responder.respond( sock=newSocket )
  >>> request_as_seen == request
  True
  >>> request_type == request.split(' ')[0]
  True
  >>> status == True
  True
  >>> response == ("OK" if status else "error") + ('' if ' ' not in request else ' ' + dispatcher(request)[2])
  True
  >>> #
  >>> # ... ... done; terminate the test ... ...
  >>> newSocket.close()
  >>> sock.close()
  >>> test_client.terminate()
  """

if 'run_tests_on_load' in dir() and 'doctest_it' in dir():
  if run_tests_on_load:
    print('*** testing RequestHandler - dummy request dispatcher')
    doctest_it(respond_to_request_dummy_dispatcher_test)
    print()

# -------------------------------------------------------------------------------------------------------------
# remaining tests: use RequestDispatcher as dispatcher
# -------------------------------------------------------------------------------------------------------------

def respond_to_request_register_q_test(void):
  """
  Test RequestHandler by creating a client program on the fly, then trading messages with it
  >>> #
  >>> # ... ... dispatcher checks for 'request' before space, leaves what follows after ... ...
  >>> reader_to_SAP = CommunicatorToSAP(**{'communicator_to_SAP': {}})
  >>> queue_to_readers = MessageQueueToReaders(**{'buffers': {}, 'buffer_to_users': {}})
  >>> queue_to_writers = MessageQueueToWriters(**{'buffers': {}, 'buffer_to_users': {}})
  >>> responder = RequestHandler( RequestDispatcher(queue_to_readers, queue_to_writers, reader_to_SAP) )
  >>> #
  >>> # ... ... confirm initial conditions ... ...
  >>> request_type, new_q = 'register_q', 'q_bert'
  >>> queue_to_readers.queues() == set()
  True
  >>> queue_to_writers.queues() == set()
  True
  >>> #
  >>> # ... ... set up for simple server communications ... ...
  >>> sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # enable TCP connection
  >>> sock.settimeout(30)                                           # put 30 second timeout on the socket to prevent indefinite execution
  >>> sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    # allow reuse of local addresses, for fast restart upon server termination
  >>> well_known_port = 8881
  >>> #
  >>> # ... ... initiate the lightweight test server ... ...
  >>> sock.bind(('', well_known_port))
  >>> sock.listen(1)    # set the number of clients waiting for a connection that the server can bind at once
  >>> #
  >>> # ... ... set up a lightweight test client ... ...
  >>> client_py_syntax = 'C:/temp/testclient.py'             # the Python files API (open(), close(), etc.) seems to require / separators
  >>> request = "{} {}\\n".format(request_type, new_q)
  >>> test_client = TestClient(client_py_syntax, 'localhost', well_known_port, request)
  >>> #
  >>> # ... ... respond to message from client ... ...
  >>> newSocket, address = sock.accept()
  >>> print('Connected from {}'.format(address), file=sys.stderr)
  >>> newSocket.settimeout(30)
  >>> request_as_seen, parsed_request_type, status, response = responder.respond( sock=newSocket )
  >>> request_as_seen == request
  True
  >>> parsed_request_type == request_type
  True
  >>> status
  True
  >>> response
  'OK'
  >>> #
  >>> # ... ... check for registration ... ...
  >>> queue_to_readers.queues() == { new_q }
  True
  >>> queue_to_writers.queues() == { new_q }
  True
  >>> #
  >>> # ... ... done; terminate the test ... ...
  >>> newSocket.close()
  >>> sock.close()
  >>> test_client.terminate()
  """

if 'run_tests_on_load' in dir() and 'doctest_it' in dir():
  if run_tests_on_load:
    print('*** testing RequestHandler - RequestDispatcher as dispatcher')
    doctest_it(respond_to_request_register_q_test)
    print()


# ***********************************************
#  Tests Complete 
# ***********************************************

if 'run_tests_on_load' in dir() and 'doctest_it' in dir():
  if run_tests_on_load:
    print('*** tests concluded')
    print()
