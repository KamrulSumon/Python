# *************************************************************************************************************************
# message service library module - support the processing of requests related to the organizing, capturing, 
# and distributing of client messages
# ------------------------------------------------------------------------------------------------------------------------
#
# organization
# ------------
#
# The module is organized as a series of classes.  No free functions have been harmed in the construction
# of this module.
#
# Inter-class dependencies are ordered bottom-up:  
# i.e., if a class B depends on a class A, then A will appear before B in file order.
#
# All external module dependencies have been placed at the head of the file.  All of these dependencies
# involve Python library modules.
#
# other
# -----
#
# The code below assumes Python 3 or better.  It has been tested with Python 3.4.2 on Windows
# (see messageServerTests.py)
#
# -- Phil Pfeiffer
#    27 April 2015
# *************************************************************************************************************************

# =========================================================================================================================
# dependencies on Python library modules
# =========================================================================================================================

import sys          # errors reported to sys.stderr
import copy         # copy.copy used to copy mutable keyed datasets in support of incremental dataset deletion
import socket       # message receipt and response supported using TCP connections
import re           # regular expressions used to parse incoming requests
import abc          # abc.ABCMeta used to declare a class as an abstract base class
import functools    # functoools.reduce used to concatenate lists of strings into individual strings for message output


# *************************************************************************************************************************
# utility classes
# *************************************************************************************************************************

# =========================================================================================================================
# metaclass for converting classes to singletons
# =========================================================================================================================

class Singleton(type):
  _instances = {}
  def __call__(cls, *args, **kwargs):
    if cls not in cls._instances:      # instantiate shared class instance on first object instantiation
      Singleton._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
    else:   # reinvoke __init__ for the lone instance on subsequent instantiations.  remove clause if re-init not desired
      Singleton._instances[cls].__init__(*args, **kwargs)
    return Singleton._instances[cls]

# ===========================================================================================================================
# mixin class for supporting aliaising of map methods in a class that
# -.  maps elements in a first 'from' domain to elements in a second 'to' domain
# -.  whose methods follow the following naming conventions:
#
#     -. register( fromelt, toelt )  -    add element ( fromelt, { toelt } )      to a map
#     -. register_from( fromelt ) -       add element ( fromelt, { } )            to a map
#     -. register_to( toelt ) -           add element ( toelt, { } }              to the map's inverse  (where supported)
#     -. froms( ) -                       return set of all elements in map's domain
#     -. tos_for_from( fromelt ) -        return set of all elements toelt such that map( from ) = toelt
#     -. tos( ) -                         return set of all elements in map's codomain
#     -. tos_for_from( fromelt ) -        return set of all elements toelt such that map( from ) = toelt
#     -. unregister( fromelt, toelt )  -  remove element  ( fromelt, { toelt } ) from a map   [not aliased]
#     -. unregister_from( fromelt ) -     remove all elements from the map whose domain element is fromelt
#     -. unregister_to( toelt ) -         remove all elements from the map whose codomain element is toelt
#
#  parameters:
# -. kwargs['entity_aliases'] -
#       a list of values of the form  (( from, ( from_alias | None )), ( to, ( to_alias | None )))
#       each of which specifies how __getattr__ supports aliasing of map name procedures, with
#    -.  instances of 'from' mapped to 'from_alias' (if present) or themselves (if None)
#    -.  instances of 'to'   ampped to 'to_alias;   (if present) or themselves (if None)
#
#  effect:  supports parallel set of methods, with
#    -.  from in method names replaced with from_alias
#    -.  to   in method names replaced with to_alias
#
#  example:
#    assume entity_aliases: [(( 'lodging', 'motel' ), ( 'locale', 'state' ))]
#    assumed names with aliases would then be as follows:
#
#     -. register()  -                    (no alias)
#     -. register_lodging( ) -            register_motel()
#     -. register_locale( ) -             register_state()
#     -. lodgings( ) -                    motels()
#     -. locales_for_lodging( ) -         states_for_motel()
#     -. locales( ) -                     states()
#     -. lodgings_for_locale( ) -         motels_for_state()
#     -. unregister( )  -                 (no alias)
#     -. unregister_lodging( ) -          unregister_motel()
#     -. unregister_locale( ) -           unregister_state()
#
#   With a map of [(( 'lodging', 'motel' ), ( 'locale', None ))], the following aliases would be supported:
#
#     -. register()  -                    (no alias)
#     -. register_lodging( ) -            register_motel()
#     -. register_locale( ) -             (no alias)
#     -. lodgings( ) -                    motels()
#     -. locales_for_lodging( ) -         locales_for_motel()
#     -. locales( ) -                     (no alias)
#     -. lodgings_for_locale( ) -         motels_for_locale()
#     -. unregister( )  -                 (no alias)
#     -. unregister_lodging( ) -          unregister_motel()
#     -. unregister_locale( ) -           (no alias)
# =========================================================================================================================

class AddMapMethodAliases(object):
  #
  # __init__:  initialize the alias dictionary
  def __init__(self):
    #
    # support easier-to-read method names for names for domain, codomain
    if 'entity_aliases' not in dir(self):  self.method_aliases = {}
  #
  # add_aliases:  initialize the aliases
  def add_aliases(self, **kwargs):
    if 'entity_aliases' in kwargs:
      self.aliases_keyvalue = kwargs['entity_aliases']
      for alias_map in self.aliases_keyvalue:
        try:
          ((frum, from_alias), (to, to_alias)) = alias_map
          if from_alias == frum:  from_alias = None     # avoid infinite recursion that could arise if attributes were aliased to themselves
          if to_alias == to:      to_alias = None
          if from_alias is None and to_alias is None:  return
          if from_alias is not None:
            if 'register_'+to in dir(self):      self.method_aliases.update( { 'register_' + to_alias   : eval('self.register_'+to) } )
            if to+'s' in dir(self):              self.method_aliases.update( { to_alias+'s'             : eval('self.' + to + 's') } )
            if 'unregister_'+to in dir(self):    self.method_aliases.update( { 'unregister_' + to_alias : eval('self.unregister_'+to) } )
          if to_alias is not None:
            if 'register_'+frum in dir(self):    self.method_aliases.update( { 'register_' + from_alias   : eval('self.register_'+frum) } )
            if frum+'s' in dir(self):            self.method_aliases.update( { from_alias+'s'             : eval('self.' + frum + 's') } )
            if 'unregister_'+frum in dir(self):  self.method_aliases.update( { 'unregister_' + from_alias : eval('self.unregister_'+frum) } )
          if from_alias is not None and to_alias is not None:
            if frum+'s_for_'+to in dir(self):    self.method_aliases.update( { from_alias+'s_for_'+to_alias : eval('self.' + frum + 's_for_' + to) } )
            if to+'s_for_'+frum in dir(self):    self.method_aliases.update( { to_alias+'s_for_'+from_alias : eval('self.' + to + 's_for_' + frum) } )
          if from_alias is None and to_alias is not None:
            if frum+'s_for_'+to in dir(self):    self.method_aliases.update( { frum+'s_for_'+to_alias   : eval('self.' + frum + 's_for_' + to) } )
            if to+'s_for_'+frum in dir(self):    self.method_aliases.update( { to_alias+'s_for_'+frum   : eval('self.' + to + 's_for_' + frum) } )
          if from_alias is not None and to_alias is None:
            if frum+'s_for_'+to in dir(self):    self.method_aliases.update( { from_alias+'s_for_'+to   : eval('self.' + frum + 's_for_' + to) } )
            if to+'s_for_'+frum in dir(self):    self.method_aliases.update( { to_alias+'s_for_'+frum   : eval('self.' + to + 's_for_' + frum) } )
        except:
          pass
  #
  # support method name aliases - return null set on failed lookups
  def __getattr__(self, attr):
    if attr not in self.method_aliases:
      print('{}.{}unknown attribute: {}', self.__class__.__name__, '__getattr__', attr, file=sys.stdout)
      return super().__getattribute__(attr)
    else:  return self.method_aliases[attr]
  #
  # auxiliary methods
  #
  def alias_keywords(self):
    return {} if 'aliases_keyvalue' not in dir(self) else { 'entity_aliases' : self.aliases_keyvalue }


# ============================================================================================================
# collection class for supporting
# -.  1<->N associations between domain, codmain objects
# *.  allows for
# -.  registering and updating (domain, codomain) bindings
# -.  removing a particular (domain, codomain) binding from the collection
# -.  removing a domain element from collection and all associated (domain element, codomain element)
# -.  removing a codomain element from collection  and all associated (domain element, codomain element)
# -.  aliasing the names of the methods, using Alias
# ============================================================================================================
#
class InvertibleMap(AddMapMethodAliases):
  #
  # __init__:  initialize the two-way mapping.
  #
  def __init__(self, **kwargs):
    #
    # pre-populate maps if explicitly requested to do so
    self.forward_map, self.reverse_map = {}, {}
    if 'forward_map' in kwargs:
      for (domain_element, codomain_element_set) in kwargs['forward_map'].items():
        for codomain_element in codomain_element_set:
          self.register(domain_element, codomain_element)
    #
    # support easier-to-read method names for names containing 'domain', 'codomain'
    super().__init__()
    self.add_aliases(**kwargs)
  #
  # register domain_element <-> codomain_element element binding
  def register(self, domain_element, codomain_element):
    if domain_element not in self.forward_map: self.forward_map[domain_element] = set([])
    self.forward_map[domain_element] |= {codomain_element}
    if codomain_element not in self.reverse_map: self.reverse_map[codomain_element] = set([])
    self.reverse_map[codomain_element] |= {domain_element}
  #
  # break all bindings for domain_element
  def unregister_domain_element(self, domain_element):
    if domain_element not in self.forward_map: return
    for codomain_element in self.forward_map[domain_element]:
      self.reverse_map[codomain_element] -= { domain_element }
      if self.reverse_map[codomain_element] == set(): del self.reverse_map[codomain_element]
    del self.forward_map[domain_element]
  #
  # break all bindings for codomain_element
  def unregister_codomain_element(self, codomain_element):
    if codomain_element not in self.reverse_map: return
    for domain_element in self.reverse_map[codomain_element]:
      self.forward_map[domain_element] -= { codomain_element }
      if self.forward_map[domain_element] == set(): del self.forward_map[domain_element]
    del self.reverse_map[codomain_element]
  #
  # break a specific domain_element <-> codomain_element element binding
  def unregister(self, domain_element, codomain_element):
    if domain_element in self.forward_map:
      self.forward_map[domain_element] -= { codomain_element }
    if codomain_element in self.reverse_map:
      self.reverse_map[codomain_element] -= { domain_element }
  #
  # retrieve all domain elements
  def domain_elements(self): return set(self.forward_map.keys())
  #
  # retrieve all codomain elements bound to domain_element
  def codomain_elements_for_domain_element(self, domain_element):
    return self.forward_map.get(domain_element, set([]))
  #
  # retrieve all codomain elements
  def codomain_elements(self): return set(self.reverse_map.keys())
  #
  # retrieve all domain elements bound to codomain_element
  def domain_elements_for_codomain_element(self, codomain_element):
    return self.reverse_map.get(codomain_element, set([]))
  #
  # auxiliary methods
  # the forward map suffices here, because the backward map inverts the forward
  #
  def me(self, methodname):    return "{}.{}".format(self.__class__.__name__, methodname)
  def __repr__(self):
    return "{}(**{!r})".format( self.__class__.__name__, self.state_by_keyword())
  def __eq__(self, other):   return isinstance( other, self.__class__ ) and self.state_by_keyword() == other.state_by_keyword()
  def state_by_keyword(self):
    keywords = { } if 'forward_map' not in dir(self) else { 'forward_map': self.forward_map }
    keywords.update( self.alias_keywords() )
    return keywords


# ************************************************************************************************************
# classes for binding message collections to their defining properties: i.e.,
# -.  their associated  buffers
# -.  the names of the entities that use them
# ************************************************************************************************************

# ============================================================================================================
# classes for buffering groups of messages by name
# ============================================================================================================

# --------------------------------------------------------------------------------------
# class that corresponds to a message buffer - i.e., a list of messages
# --------------------------------------------------------------------------------------
#
class MessageBuffer(object):
  #
  # __init__:  initialize the buffer.
  #
  # kwargs parameters (all optional):
  # *.  'buffer' - if present, the message list will be prepopulated with the values in this list
  #
  def __init__(self, **kwargs):
    # pre-populate buffer if explicitly requested to do so
    if 'buffer' in kwargs:  self.message_list = kwargs['buffer']
    else:
      # instantiate buffer collection if nothing defined as of yet
      if 'buffer' not in dir(self):  self.message_list = []
  #
  # add next message to stream
  def append_message(self, message):  self.message_list += [message]
  #
  # return specified message from stream
  def retrieve_message(self, k):   return None if k not in range(len(self.message_list)) else self.message_list[k]
  #
  # auxiliary methods
  def __repr__(self):          return "{}(**{!r})".format(self.__class__.__name__, self.state_by_keyword())
  def __eq__(self, other):     return isinstance( other, self.__class__ ) and self.state_by_keyword() == other.state_by_keyword()
  def state_by_keyword(self):
    return {} if 'message_list' not in dir(self) else { 'buffer': self.message_list }


# --------------------------------------------------------------------------------------
# collection class for MessageBuffer objects
# *.  allows for registering, looking up, unregistering message buffers by name
# *.  assures
# -.  uniqueness of names in collection
# -.  consistency of state on attempted re-registration
# --------------------------------------------------------------------------------------
#
class MessageBufferCollection(metaclass=Singleton):
  #
  # __init__:  initialize the collection
  #
  # kwargs parameters (all optional):
  # *.  'buffers' - if present, the collection of buffers will be pre-populated with the buffer objects in this list:
  #       e.g.,  MessageBufferCollection(**{'buffers': {'foo': MessageBuffer(**{'buffer': []})}})
  #              pre-populates the collection with one, empty buffer called 'foo'
  #
  def __init__(self, **kwargs):
    # pre-populate map if explicitly requested to do so
    if 'buffers' in kwargs:  self.buffer_collection = kwargs['buffers']
    else:
      # instantiate buffer collection if nothing defined as of yet
      if 'buffer_collection' not in dir(self):  self.buffer_collection = {}
  #
  # check if (named) buffer registered
  def is_registered(self, buffer_name):  return buffer_name in self.buffer_collection
  #
  # instantiate and register (named) buffer
  def register(self, buffer_name):
    if buffer_name not in self.buffer_collection:  self.buffer_collection[buffer_name] = MessageBuffer()
    else:  print("{}: advisory - buffer {} already registered".format(self.me('register'), buffer_name), file=sys.stderr)
  #
  # return buffer names
  def buffers(self):  return set(self.buffer_collection.keys())
  #
  # unregister specified buffer
  def unregister(self, buffer_name):
    if buffer_name in self.buffer_collection:  del self.buffer_collection[buffer_name]
    else: print("{}: advisory - buffer {} not currently registered".format(self.me('unregister'), buffer_name), file=sys.stderr)
  #
  # add message to specified buffer
  def append_message(self, buffer_name, message):
    if buffer_name in self.buffer_collection:  self.buffer_collection[buffer_name].append_message(message)
    else:  print("{}: advisory - buffer {} not currently registered".format(self.me('append_message'), buffer_name), file=sys.stderr)
  #
  # return specified message from specified buffer
  def retrieve_message(self, buffer_name, k):
    if buffer_name in self.buffer_collection:  return self.buffer_collection[buffer_name].retrieve_message(k)
    else:  print("{}: advisory - buffer {} not currently registered".format(self.me('retrieve_messages'), buffer_name), file=sys.stderr)
  #
  # auxiliary methods
  def me(self, methodname):    return "{}.{}".format(self.__class__.__name__, methodname)
  def __repr__(self):          return "{}(**{!r})".format(self.__class__.__name__, self.state_by_keyword())
  def __eq__(self, other):     return isinstance( other, self.__class__ )     # keywords check not needed due to singleton status
  def state_by_keyword(self):
    return {} if 'buffer_collection' not in dir(self) else { 'buffers': self.buffer_collection }


# ============================================================================================================
#  classes for associating named message buffers with named users - i.e., readers and writers -
#  along with positional information for the readers
# ============================================================================================================

# -----------------------------------------------------------------------------------------
# class for associating named buffers from a message buffer collection with named users
# ----------------------------------------------------------------------------------------

class MessageBufferToUsers(AddMapMethodAliases):
  #
  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #  supporting class for managing the mapping of buffer names to user names
  #
  class MessageBufferNameToUsers(InvertibleMap):
    #
    # initialize the map itself
    #
    # kwargs parameter (optional):
    # *.  'buffer_to_users' - if present, the map will be pre-populated with the key => value set pairings in this list:  e.g.,
    #                         if 'buffer_to_users' = {'stuff': {'joan', 'joe'}}}, 
    #                         then the initial map will have 'stuff' -> {'joan', 'joe'} as its one (key, value set) pair
    #
    def __init__(self, **kwargs):
      if 'buffer_to_users' in kwargs:
        buffer_to_users = kwargs['buffer_to_users']
        forward_map = buffer_to_users.get('forward_map',{})
        del kwargs['buffer_to_users']
        kwargs.update({'forward_map': forward_map})
      kwargs.update({'entity_aliases': [(('domain_element', 'buffer'), ('codomain_element', 'user'))]})
      super().__init__(**kwargs)
  #
  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #
  # initialize content for MessageBufferToUsers instances  -
  #    i.e., a named message buffer collection, along with a map from named message buffers to named buffer users
  #
  # kwargs parameters (all optional):
  #
  # *.  'buffers'          - if present, the collection of buffers will be pre-populated with the buffer objects in this list:
  #                          e.g.,  MessageBufferToUsers(**{'buffers': {'foo': MessageBuffer(**{'buffer': []})}}) 
  #                                 pre-populates the collection with one, empty buffer called 'foo'
  # *.  'buffer_to_users'  - if present, use this value to pre-populate the map from buffers to users, as described above, under MessageBufferNameToUsers
  # *.  'entity_aliases'   - if present, a pair of values that are to alias the terms for the domain elements and codomain elements, respectively,
  #                          in the MessageBufferCollection and MessageBufferNameToUsers method names
  #
  def __init__(self, **kwargs):
    #
    # initialize the buffers argument, if requested to do so
    self.buffer_collection = MessageBufferCollection(**kwargs)
    #
    # craft aliases for this class's methods - again, if requested to do so
    super().__init__()
    self.buffer_alias, self.user_alias = None, None
    if 'entity_aliases' in kwargs:
      self.entity_aliases = kwargs['entity_aliases']
      try:
        (self.buffer_alias, self.user_alias) = self.entity_aliases
        self.add_aliases(**{'entity_aliases': [(('buffer', self.buffer_alias), ('user', self.user_alias))]})
      except:
        pass
    #
    # finally, initialize the map.  'buffer_to_users' will be checked in the constructor for MessageBufferNameToUsers
    self.buffer_to_users = MessageBufferToUsers.MessageBufferNameToUsers(**kwargs)
  #
  # register (i.e., create) a named buffer
  def register_buffer(self, buffer_name):
    if not self.buffer_collection.is_registered(buffer_name):  self.buffer_collection.register(buffer_name)
    else:  print("{}: advisory - {} {} already registered".format(self.me('register'), 'buffer' if self.buffer_alias is None else self.buffer_alias, buffer_name), file=sys.stderr)
  #
  # return names of all buffers
  def buffers(self):  return self.buffer_collection.buffers()
  #
  # register a user for a buffer.  require prior buffer registration.
  def register(self, buffer_name, user_name):
    if self.buffer_collection.is_registered(buffer_name):
      self.buffer_to_users.register(buffer_name, user_name)
      return True
    else:
      print("{}: advisory - {} {} not yet registered".format(self.me('register'), 'buffer' if self.buffer_alias is None else self.buffer_alias, buffer_name), file=sys.stderr)
      return False
  #
  # return names of all buffers for a given user
  def buffers_for_user(self, user_name):  return self.buffer_to_users.buffers_for_user(user_name)
  #
  # return names of all users for all buffers
  def users(self):  return self.buffer_to_users.users()
  #
  # return names of all users for a given buffer
  def users_for_buffer(self, buffer_name):  return self.buffer_to_users.users_for_buffer(buffer_name)
  #
  # unregister a user for a buffer
  def unregister(self, buffer_name, user_name):
    self.buffer_to_users.unregister(buffer_name, user_name)
  #
  # unregister a buffer and all (buffer, user) bindings for that buffer
  def unregister_buffer(self, buffer_name):
    if self.buffer_collection.is_registered(buffer_name):
      users_for_buffer = copy.copy(self.users_for_buffer(buffer_name))
      for user in users_for_buffer:  self.unregister(buffer_name, user)
      self.buffer_collection.unregister(buffer_name)
    else:  print("{}: advisory - {} {} already unregistered".format(self.me('unregister_buffer'), 'buffer' if self.buffer_alias is None else self.buffer_alias, buffer_name), file=sys.stderr)
  #
  # unregister user from all message buffers
  def unregister_user(self, user_name):
    self.buffer_to_users.unregister_user(user_name)
  #
  # auxiliary methods
  def me(self, methodname):  return "{}.{}".format(self.__class__.__name__, methodname)
  def __repr__(self):        return "{}(**{!r})".format(self.__class__.__name__, self.state_by_keyword())
  def __eq__(self, other):   return isinstance( other, self.__class__ )     # keywords check not needed due to singleton status
  def state_by_keyword(self):
    keywords = self.buffer_collection.state_by_keyword()
    keywords.update( { 'buffer_to_users': self.buffer_to_users.state_by_keyword() } )
    if 'entity_aliases' in dir(self): keywords.update( { 'entity_aliases':  self.entity_aliases } )
    return keywords


# -----------------------------------------------------------------------------------------------------------------
# class for associating queues -- 
#    -- i.e., **append-only** message buffers from a message buffer collection 
# -- with users who may update those queues.
#
# terms of association:  
# -.  a writer may be associated with any number of queues
# -.  a queue may be associated with any number of writers
# -.  a given writer may be associated with at most one instance of a given queue
#
# design notes:
# -.  MessageQueueToReaders and MessageQueueToWriters use a common set of queue names:  i.e., if a given queue is 
#     registered under the name 'foo' in the former, it will be registered as 'foo' under the latter.
# -.  as is typical for python, method hiding is a convention.  in particular, note the comments that
#     MessageQueueToReaders.retrieve_position() and MessageQueueToReaders.retrieve_message() are meant to support testing 
#     rather than "production" usage
# -----------------------------------------------------------------------------------------------------------------

class MessageQueueToWriters(MessageBufferToUsers):
  #
  # initialize the class's (queues, map from queues to writers) pair
  #
  # kwargs parameters (all optional):
  # *.  'buffers' - if present, the collection of queues will be pre-populated with the buffer objects in this list:
  #       e.g.,  MessageQueueToWriters(**{'buffers': {'foo': MessageBuffer(**{'buffer': []})}})
  #              pre-populates the collection with one, empty buffer called 'foo'
  # *.  'buffers_to_users' - if present, use this value to pre-populate the map from queues to writers
  #
  def __init__(self, **kwargs):
    #
    # initialize the buffers argument, if requested to do so
    kwargs.update( { 'entity_aliases': ('queue', 'writer') } )
    super().__init__(**kwargs)
  #
  # retrieve message k from queue -- strictly for testing purposes
  def retrieve_message(self, queue_name, k):
    return self.buffer_collection.retrieve_message(queue_name, k)
  #
  # add message from writer to queue, requiring registration as precondition for writing
  def append_message(self, queue_name, writer_name, message):
    if queue_name in self.buffer_collection.buffers():
      if writer_name in self.writers_for_queue(queue_name):
        self.buffer_collection.append_message(queue_name, message)
        return True
      else:
        print("{}: queue {} not currently registered to {}".format(self.me('append_message'), queue_name, writer_name), file=sys.stderr)
        return False
    else:
      print("{}: queue {} not currently registered".format(self.me('retrieve_messages'), queue_name), file=sys.stderr)
      return False


# ------------------------------------------------------------------------------------------------------------------------------
# class for associating queues -- 
#    -- i.e., read-from-the-end buffers from a message buffer collection 
# -- with users who may access those queues. 
#
# terms of association:  
# -.  a reader may be associated with any number of queues
# -.  a queue may be associated with any number of reader
# -.  a given reader may be associated with at most one instance of a given queue
#
# design notes:
# -.  for this class, the name "queue" was chosen for simplicity.  what is referred to here as "queues" are actually streams, 
#     in that each reader-queue association is further associated with an implicit "current message" parameter, 
#     -.  initially set to 0, then
#     -.  bumped up as messages are retrieved from the underlying buffer
# -.  MessageQueueToReaders and MessageQueueToWriters use a common set of queue names:  i.e., if a given queue is 
#     registered under the name 'foo' in the former, it will be registered as 'foo' under the latter.
# -.  as is typical for python, method hiding is a convention.  in particular, note the comments that
#     MessageQueueToReaders.retrieve_position() and MessageQueueToReaders.retrieve_message() are meant to support testing 
#     rather than "production" usage
# ------------------------------------------------------------------------------------------------------------------------------

class MessageQueueToReaders(MessageBufferToUsers):
  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #
  # initialize the class's (queues, map from queues to readers) pair
  #
  # kwargs parameters (all optional):
  # *.  'queues' - if present, the collection of queues will be pre-populated with the buffer objects in this list:
  #       e.g.,  MessageQueueToReaders(**{'queues': {'foo': MessageBuffer(**{'buffer': []})}})
  #              pre-populates the collection with one, empty buffer called 'foo'
  # *.  'queue_to_readers' - if present, use this value to pre-populate the map from queues to readers, as described above, under MessageQueueNameToWriters
  # *.  'queue_to_readers_to_positinos' -
  #        if present, use this value to pre-populate the map from queues to readers to their positions
  #        otherwise, initialize all reader positions to 0
  #
  def __init__(self, **kwargs):
    #
    # initialize the buffers argument, if requested to do so
    kwargs.update( { 'entity_aliases': ('queue', 'reader') } )
    super().__init__(**kwargs)
    #
    # pre-populate map of queue positions by reader
    if 'queue_to_readers_to_positions' in kwargs:  self.queue_to_readers_to_positions = kwargs['queue_to_readers_to_positions']
    else:
      # instantiate buffer collection if nothing defined as of yet
      if 'queue_to_readers_to_positions' not in dir(self):
        self.queue_to_readers_to_positions = {}
        for queue in self.queues():
          self.queue_to_readers_to_positions[queue] = {}
          for reader in self.readers_for_queue(queue):
            self.queue_to_readers_to_positions[queue][reader] = 0
  #
  # register a reader for a queue.  require prior queue registration.
  def register(self, queue_name, reader_name):
    if super().register(queue_name, reader_name):
      if queue_name not in self.queue_to_readers_to_positions:  self.queue_to_readers_to_positions[queue_name] = {}
      if reader_name not in self.queue_to_readers_to_positions[queue_name]:  self.queue_to_readers_to_positions[queue_name][reader_name] = 0
      return True
    else:
      return False
  #
  # return next message from queue to reader, requiring registration as precondition for reading
  def next_message(self, queue_name, reader_name):
    if queue_name in self.queues():
      if reader_name in self.readers_for_queue(queue):
        next = self.queue_to_readers_to_positions[queue_name][reader_name]
        message = self.buffer_collection[queue_name].retrieve_message(next)
        if message is not None: self.queue_to_readers_to_positions[queue_name][reader_name] = next+1
        return message
      else:  print("{}: queue {} not currently registered to {}".format(self.me('next_message'), queue_name, reader_name), file=sys.stderr)
    else:  print("{}: queue {} not currently registered".format(self.me('next_message'), queue_name), file=sys.stderr)
  #
  # retrieve current stream position for queue reader  -- strictly for testing purposes
  def retrieve_position(self, queue_name, reader_name):
    if queue_name in self.queues():
      if reader_name in self.readers_for_queue(queue):
        return self.queue_to_readers_to_positions[queue_name][reader_name]
      else:  print("{}: queue {} not currently registered to {}".format(self.me('next_message'), queue_name, reader_name), file=sys.stderr)
    else:  print("{}: queue {} not currently registered".format(self.me('next_message'), queue_name), file=sys.stderr)
  #
  # retrieve message k from queue -- strictly for testing purposes
  def retrieve_message(self, queue_name, k):
    return self.buffer_collection.retrieve_message(queue_name, k)
  #
  # unregister a reader for a queue
  def unregister(self, queue_name, reader_name):
    super().unregister(queue_name, reader_name)
    if reader_name in self.queue_to_readers_to_positions[queue_name]:  del self.queue_to_readers_to_positions[queue_name][reader_name]
  #
  # unregister a queue and all (queue, reader) bindings for that queue
  def unregister_queue(self, queue_name):
    self.unregister_buffer(queue_name)
    del self.queue_to_readers_to_positions[queue_name]
  #
  # unregister reader from all message queues
  def unregister_reader(self, reader_name):
    self.unregister_user(reader_name)
    for queue_name in self.queues():
      if reader_name in self.queue_to_readers_to_positions[queue_name]:  del self.queue_to_readers_to_positions[queue_name][reader_name]
  #
  # auxiliary methods
  def me(self, methodname):  return "{}.{}".format(self.__class__.__name__, methodname)
  def __repr__(self):        return "{}(**{!r})".format(self.__class__.__name__, self.state_by_keyword())
  def __eq__(self, other):   return isinstance( other, self.__class__ )     # keywords check not needed due to singleton status
  def state_by_keyword(self):
    keywords = super().state_by_keyword()
    if 'queue_to_readers_to_positions' in dir(self):  keywords.update( { 'queue_to_readers_to_positions': self.queue_to_readers_to_positions } )
    return keywords


# ===========================================================================================================================
# class that track associations between communicators and their service access points (SAPs) - i.e., (host/ port) pairs
#
# terms of association:  
# -.  a communicator may be associated with at most one SAP
#
# design notes:
# -.  no restrictions have been placed on associations between SAPs and communicators.  
#     while each SAP may, in practice, be associated with at most one communicator, the use of SAPs to demultiplex
#     messages to multiple communicators is feasible and should therefore be allowed.
# -.  while the class uses the term "communicators", at present only readers need register:
#     asynchronous updates of message queue status are only being sent to readers
# ===========================================================================================================================
#
class CommunicatorToSAP(metaclass=Singleton):
  #
  # initialize binding mappings, limiting sources to one per stream
  def __init__(self, **kwargs):
    if 'communicator_to_SAP' in kwargs:  self.communicator_to_SAP = kwargs['communicator_to_SAP']
    else:
      if 'communicator_to_SAP' not in dir(self): self.communicator_to_SAP = {}
  #
  def register(self, communicator, host, port):  self.communicator_to_SAP[communicator] = (host, port)
  #
  def unregister(self, communicator):
    if communicator in self.communicator_to_SAP:  del self.communicator_to_SAP[communicator]
  #
  def SAP(self, communicator):    return self.communicator_to_SAP.get(communicator, None)
  #
  # retrieve all communicators
  def communicators(self): return set(self.communicator_to_SAP.keys())
  #
  # auxiliary methods
  def __repr__(self):          return "{}(**{!r})".format(self.__class__.__name__, self.state_by_keyword())
  def __eq__(self, other):     return isinstance( other, self.__class__ ) and self.state_by_keyword() == other.state_by_keyword()
  def state_by_keyword(self):
    return {} if 'communicator_to_SAP' not in dir(self) else { 'communicator_to_SAP': self.communicator_to_SAP }


# ************************************************************************************************************
# classes for exchanging one-line messages with other processes
# design:
# -.  messages will be exchanged via file system readline/writeline APIs
#     (this can be supported since sockets can be configured to work like files)
# ************************************************************************************************************
#
# ============================================================================================================
# class that supports line-by-line-based communication with other entities via two half-duplex files:
# -.  one for receiving messages  (infile)
# -.  one for sending messages    (outfile)
# ============================================================================================================
#
class MessageExchanger(object):
  #
  # specify infile for sending, outfile for receiving messages, 
  # allowing for optional one-time initialization of the two file parameters
  def __init__(self, **kwargs):
    self.infile, self.outfile = kwargs.get('infile', None), kwargs.get('outfile', None)
  #
  # read line from a co-communicator, returning (status, line) pair.
  # allow for overriding of __init__-time file specification with kwargs' 'infile' keyword
  def get_line(self, **kwargs):
    infile = self.resolve_infile( 'get_line', **kwargs )
    try:
      next_line = infile.readline()
      return ( True, next_line )
    except Exception:
      print("{}: read failure".format(self.me('get_line')), file=sys.stderr)
      return ( False, None )
  #
  # send line to a co-communicator, returning status of write.
  # allow for overriding of __init__-time file specification with kwargs' 'outfile' keyword
  def put_line(self, line, **kwargs):
    outfile = self.resolve_outfile( 'put_line', **kwargs )
    try:
      outfile.write( line )
      outfile.flush( )            # essential for assuring immediate receipt of message
      return True
    except Exception:
      print("{}: write failure (output: {})".format(self.me('put_line'), line), file=sys.stderr)
      return False
  #
  # auxiliary methods
  def resolve_infile(self, methodname, **kwargs):
    assert 'infile' in kwargs or 'infile' in dir(self), "{}: infile not defined".format(self.me(methodname))
    return kwargs.get('infile', self.infile)
  def resolve_outfile(self, methodname, **kwargs):
    assert 'outfile' in kwargs or 'outfile' in dir(self), "{}: outfile not defined".format(self.me(methodname))
    return kwargs.get('outfile', self.outfile)
  #
  def me(self, methodname):    return "{}.{}".format(self.__class__.__name__, methodname)
  def __repr__(self):          return "{}(**{!r})".format(self.__class__.__name__, self.state_by_keyword())
  def __eq__(self, other):     return isinstance( other, self.__class__ ) and self.state_by_keyword() == other.state_by_keyword()
  def state_by_keyword(self):
    keywords = {}
    if 'infile'  in dir(self): keywords.update( { 'infile': self.infile } )
    if 'outfile' in dir(self): keywords.update( { 'outfile': self.outfile } )
    return keywords


# ============================================================================================================
# class that uses an open socket as a message exchanger.
# key addition to message exchanger functionality:  
#    use of the socket API to derive an object that allows for file-like treatment of sockets:
#    in particular, the use of readline and writelines with open sockets.
# ============================================================================================================
#
class OpenSocketMessageExchanger(MessageExchanger):
  def __init__(self, sock, **kwargs):
    self.sock = sock
    #
    # pre-populate state if explicitly requested to do so
    self.infile  = kwargs.get('infile', sock.makefile(mode='r'))
    if not 'infile' in kwargs: kwargs['infile'] = self.infile
    self.outfile  = kwargs.get('outfile', sock.makefile(mode='w'))
    if not 'outfile' in kwargs: kwargs['outfile'] = self.outfile
    super().__init__( **kwargs )
  def close(self):
    self.infile.close()
    self.outfile.close()
  #
  # auxiliary methods
  def __repr__(self):          return "{}({}, **{!r})".format(self.__class__.__name__, self.sock, self.state_by_keyword())
  def __eq__(self, other):     return isinstance( other, self.__class__ ) and self.state_by_keyword() == other.state_by_keyword()
  def state_by_keyword(self):
    keywords = super().state_by_keyword()
    keywords.update( self.local_state_by_keyword() )
    return keywords
  def local_state_by_keyword(self):
    keywords = {}
    if 'infile'  in dir(self): keywords.update( { 'infile': self.infile } )
    if 'outfile' in dir(self): keywords.update( { 'outfile': self.outfile } )
    return keywords


# ===========================================================================================================================
# class that uses a service access point (SAP) - i.e.., a (host, port) pair - to generate a socket message exchanger
# ===========================================================================================================================
#
class SAPMessageExchanger(OpenSocketMessageExchanger):
  def __init__(self, **kwargs):
    try:
      self.sock = kwargs.get('sock', socket.socket(socket.AF_INET, socket.SOCK_STREAM))
      if 'timeout' in kwargs:  self.sock.settimeout(kwargs['timeout'])
      self.hostport = kwargs.get('hostport', ('', 80))
      self.sock.connect(self.hostport)
      super().__init__(self.sock, **kwargs)
    except Exception:
      print("{}: can't connect to {}{}port {}".format(self.me('__init__'), self.hostport[0], '' if self.hostport[0] == '' else ', ', self.hostport[1]), file=sys.stderr)
  #
  def close(self):  self.sock.close()
  #
  # auxiliary methods
  def __repr__(self):          return "{}({}, **{!r})".format(self.__class__.__name__, self.hostport, self.state_by_keyword())
  def __eq__(self, other):     return isinstance( other, self.__class__ ) and (self.hostport, self.state_by_keyword()) == (other.hostport, other.state_by_keyword())
  def state_by_keyword(self):
    keywords = super().state_by_keyword()
    if 'sock' in dir(self): keywords.update( { 'sock': self.sock } )
    return keywords


# ***************************************************************************************************************************
# define classes for parsing bodies of client requests and generating bodies for responses to these requests
# all requests as welll as all generated responses are limited to one text line
#
# Response generator classes can be partioned into three groups
# -.  side-effect free generators:
#       QueuesForReader, QueuesForWriter
# -.  generators whose only effects are on local data structures
#       RegisterQueue, RegisterWriterForQueue,
#       UnregisterReaderForQueue, UnregisterWriterForQueue, UnregisterEntity, UnregisterQueue
# -.  generators that also issue messages to clients
#       RegisterReaderForQueue, which also sends all backlogged messages to the new reader
#       AppendMessageToQueue, which also sends the message to all registered queue readers
# ***************************************************************************************************************************

# ============================================================================================================
# abstract class for common functionality for individual response generators
# ============================================================================================================

class AbstractResponseGenerator(metaclass=abc.ABCMeta):
  #
  # patterns for request tokens
  #
  def _p_queue():        return "(?P<queue>[A-Za-z_]\w*)"
  def _p_reader():       return "(?P<reader>[A-Za-z_]\w*)"
  def _p_writer():       return "(?P<writer>[A-Za-z_]\w*)"
  def _p_message():      return "(?P<message>.*)"
  def _p_communicator(): return "(?P<communicator>[A-Za-z_]\w*)"
  def _p_SAP():          return "(?P<host>[A-Za-z_\.]*)\s+(?P<port>\d{1,5})"
  #
  # initialize the pattern that the current instance of a response generator uses a pattern to parse requests.
  # also, check that the parameters that the current response generator requires are present in the keywords dict. 
  def __init__(self, pattern, required_keywords, kwargs):
    self.require_keywords(required_keywords, kwargs, '__init__')
    self.pattern, self.required_keywords, self.kwargs = re.compile("^" + pattern + "$"), required_keywords, kwargs
  #
  # respond to a request by
  # -.  checking to see if it matches the expected request pattern
  # -.  calling the derived class's generate_response method if so, with the results of the parse
  def __call__(self, request_body):
    match = self.pattern.match(request_body)
    if match is None:  return (False, 'error (syntax error)')
    return self.generate_response(match.groupdict())
  #
  # auxiliary methods
  #
  # check that the keyword parameters that the concrete class requires are in actual_keywords
  def require_keywords(self, required_keywords, actual_keywords, methodname):
    missing_keys = set(required_keywords) - set(actual_keywords.keys())
    if len(missing_keys) == 0:  return
    missing_keycount  = "{} keyword{}".format(len(missing_keys), '' if len(missing_keys) == 1 else 's')
    missing_keynames  = functools.reduce(lambda s, n: s + ", " + n, missing_keys, "")[2:]
    raise Exception("?? {}: kwargs missing {}: {}".format(self.me(methodname), missing_keycount, missing_keynames))
  #
  def me(self, methodname):  return "{}.{}".format(self.__class__.__name__, methodname)
  def __repr__(self):        return "{}({!r}, {!r}, {!r})".format(self.__class__.__name__,  self.pattern, self.required_keywords, self.kwargs)
  def __eq__(self, other):   return isinstance( other, self.__class__ ) and ( self.pattern, self.required_keywords, self.kwargs ) ==  ( other.pattern, other.required_keywords, other.kwargs )


# ===================================================================================================================================
# request-specific response generators
# 
# each class below is responsible for recognizing and responding to one particular type of request.
#
# design notes:
# -.  each response generator has two methods:
#     -.  one __init__ that establishes the context for parsing requests
#     -.  a response_generator method that 
#         -.  generates a response
#         -.  realizes any additional effects associated with the request
# -.  the format for each class's associated request is specified by the pattern parameter passed to its base class's __init__ method,
#     AbstractResponseGenerator.__init__.
# -.  the implementation assumes that the queue readers (kwargs['queue_to_readers']) and queue writers (kwargs['queue_to_writers'])
#     classes associate entities with queues in a common, underlying message buffer
# ===================================================================================================================================

# ----------------------------------------------------------------------
# register a queue under the specified name
# ----------------------------------------------------------------------
#
class RegisterQueue(AbstractResponseGenerator):
  #
  def __init__(self, **kwargs):
    parent = self.__class__.__bases__[0]
    pattern = parent._p_queue() + "\s*"
    required_keywords = ['queue_to_writers', 'queue_to_readers']
    super().__init__(pattern, required_keywords, kwargs)
    self.queue_to_readers = kwargs['queue_to_readers']
    self.queue_to_writers = kwargs['queue_to_writers']
  #
  def generate_response(self, parsed_request_body):
    if parsed_request_body is None:  return (False, None)
    self.queue_to_writers.register_queue(parsed_request_body['queue'])
    # self.queue_to_readers.register_queue(parsed_request_body['queue'])  - not needed, since the queues share a common singleton
    return (True, None)

# ----------------------------------------------------------------------------------------------
# register a reader for a specified queue, 
#   sending any messages in that queue to the reader's specified SAP.
# 
# design notes: 
# -.  in practice, for the request to actually succeed, the queue must already be registered
# ----------------------------------------------------------------------------------------------
#
class RegisterReaderForQueue(AbstractResponseGenerator):
  #
  def __init__(self, **kwargs):
    parent = self.__class__.__bases__[0]
    pattern = parent._p_reader() + "\s+" + parent._p_queue() + "\s+" + parent._p_SAP() + "\s*"
    required_keywords = ['queue_to_readers', 'communicator_to_SAP']
    super().__init__(pattern, required_keywords, kwargs)
    self.queue_to_readers = kwargs['queue_to_readers']
    self.reader_to_SAP = kwargs['communicator_to_SAP']
  #
  def generate_response(self, parsed_request_body):
    if parsed_request_body is None:  return (False, None)
    self.queue_to_readers.register(parsed_request_body['queue'], parsed_request_body['reader'])
    self.reader_to_SAP.register(parsed_request_body['reader'], parsed_request_body['host'], parsed_request_body['port'])
    #
    # push any messages curerntly in this queue to the queue's readers
    try:
      exchanger = SAPMessageExchanger(**{'hostport': (parsed_request_body['host'], parsed_request_body['port'])})
      while True:
        message = self.queue_to_readers('queue').next_message()
        if message is None: break
        exchanger.put_line(message)
        ack = exchanger.get_line()
        if ack != 'OK': break
      exchanger.close()
    except:
      pass
    return (True, None)

# ----------------------------------------------------------------------------------------------
# register a writer for a specified queue
# 
# design notes: 
# -.  in practice, for the request to actually succeed, the queue must already be registered
# ----------------------------------------------------------------------------------------------
#
class RegisterWriterForQueue(AbstractResponseGenerator):
  #
  def __init__(self, **kwargs):
    parent = self.__class__.__bases__[0]
    pattern = parent._p_writer() + "\s+" + parent._p_queue() + "\s*"
    required_keywords = ['queue_to_writers']
    super().__init__(pattern, required_keywords, kwargs)
    #
    self.queue_to_writers = kwargs['queue_to_writers']
  #
  def generate_response(self, parsed_request_body):
    if parsed_request_body is None:  return (False, None)
    self.queue_to_writers.register(parsed_request_body['queue'], parsed_request_body['writer'])
    return (True, None)

# ----------------------------------------------------------------------
# return the queues for which a given entity as registered as a reader
# ----------------------------------------------------------------------
#
class QueuesForReader(AbstractResponseGenerator):
  #
  def __init__(self, **kwargs):
    parent = self.__class__.__bases__[0]
    pattern = parent._p_reader() + "\s*"
    required_keywords = ['queue_to_readers']
    super().__init__(pattern, required_keywords, kwargs)
    #
    self.queue_to_readers = kwargs['queue_to_readers']
    #
  def generate_response(self, parsed_request_body):
    if parsed_request_body is None:  return (False, None)
    queues = self.queue_to_readers.queues_for_reader(parsed_request_body['reader'])
    return (True, functools.reduce(lambda s, n: s+n+" ", queues, ""))

# ----------------------------------------------------------------------
# return the queues for which a given entity as registered as a writer
# ----------------------------------------------------------------------
#
class QueuesForWriter(AbstractResponseGenerator):
  #
  def __init__(self, **kwargs):
    parent = self.__class__.__bases__[0]
    pattern = parent._p_writer() + "\s*"
    required_keywords = ['queue_to_writers']
    super().__init__(pattern, required_keywords, kwargs)
    #
    self.queue_to_writers = kwargs['queue_to_writers']
  #
  def generate_response(self, parsed_request_body):
    if parsed_request_body is None:  return (False, None)
    queues = self.queue_to_writers.queues_for_writer(parsed_request_body['writer'])
    return (True, functools.reduce(lambda s, n: s+n+" ", queues, ""))

# ----------------------------------------------------------------------------------------------
# append a message to a spedified queue,
#   sending that message to the SAPs for all currently registered readers
#
# design notes: 
# -.  in practice, for the request to actually succeed, the queue must already be registered,
#     and the associated entity must be registered as a writer for the queue
# ----------------------------------------------------------------------------------------------
#
class AppendMessageToQueue(AbstractResponseGenerator):
  #
  def __init__(self, **kwargs):
    parent = self.__class__.__bases__[0]
    pattern = parent._p_writer() + "\s+" + parent._p_queue() + "\s+" + parent._p_message()
    required_keywords = ['queue_to_writers', 'queue_to_readers', 'communicator_to_SAP']
    super().__init__(pattern, required_keywords, kwargs)
    #
    self.queue_to_readers = kwargs['queue_to_readers']
    self.reader_to_SAP = kwargs['communicator_to_SAP']
    self.queue_to_writers = kwargs['queue_to_writers']
  #
  def generate_response(self, parsed_request_body):
    if parsed_request_body is None:  return (False, None)
    queue, writer, message = parsed_request_body['queue'], parsed_request_body['writer'], parsed_request_body['message']
    if not self.queue_to_writers.append_message(queue, writer, message):  return False
    #
    # push all unsent messages from this queue to the queue's readers
    for reader in self.queue_to_readers.readers():
      try:
        exchanger = SAPMessageExchanger(**{'hostport': self.reader_to_SAP.SAP(reader)} )
        while True:
          message = self.queue_to_readers.next_message(queue, reader)
          if message is None: break
          exchanger.put_line(message)
          ack = exchanger.get_line()
          if ack != 'OK': break
        exchanger.close()
      except:
        pass
    return (True, None)

# ----------------------------------------------------------------------
# drop an entity's current as-reader registration for a given queue
# ----------------------------------------------------------------------
#
class UnregisterReaderFromQueue(AbstractResponseGenerator):
  #
  def __init__(self, **kwargs):
    parent = self.__class__.__bases__[0]
    pattern = parent._p_reader() + "\s+" + parent._p_queue() + "\s*"
    required_keywords = ['queue_to_readers']
    super().__init__(pattern, required_keywords, kwargs)
    #
    self.queue_to_readers = kwargs['queue_to_readers']
  #
  def generate_response(self, parsed_request_body):
    if parsed_request_body is None:  return (False, None)
    self.queue_to_readers.unregister(parsed_request_body['queue'], parsed_request_body['reader'])
    return (True, None)

# ----------------------------------------------------------------------
# drop an entity's current as-writer registration for a given queue
# ----------------------------------------------------------------------
#
class UnregisterWriterFromQueue(AbstractResponseGenerator):
  #
  def __init__(self, **kwargs):
    parent = self.__class__.__bases__[0]
    pattern = parent._p_writer() + "\s+" + parent._p_queue() + "\s*"
    required_keywords = ['queue_to_writers']
    super().__init__(pattern, required_keywords, kwargs)
    #
    self.queue_to_writers = kwargs['queue_to_writers']
  #
  def generate_response(self, parsed_request_body):
    if parsed_request_body is None:  return (False, None)
    self.queue_to_writers.unregister(parsed_request_body['queue'], parsed_request_body['writer'])
    return (True, None)

# ------------------------------------------------------------------------------------------
# drop an entity's current registration from all queues, deleting the entity's SAP
#   (if one has been specified)
# ------------------------------------------------------------------------------------------
#
class UnregisterEntity(AbstractResponseGenerator):
  #
  def __init__(self, **kwargs):
    parent = self.__class__.__bases__[0]
    pattern = parent._p_communicator() + "\s*"
    required_keywords = ['queue_to_readers', 'communicator_to_SAP', 'queue_to_writers']
    super().__init__(pattern, required_keywords, kwargs)
    #
    self.queue_to_readers = kwargs['queue_to_readers']
    self.reader_to_SAP    = kwargs['communicator_to_SAP']
    self.queue_to_writers = kwargs['queue_to_writers']
  #
  def generate_response(self, parsed_request_body):
    if parsed_request_body is None:  return (False, None)
    self.queue_to_readers.unregister_reader(parsed_request_body['communicator'])
    self.queue_to_writers.unregister_writer(parsed_request_body['communicator'])
    self.reader_to_SAP.unregister(parsed_request_body['communicator'])
    return (True, None)

# ----------------------------------------------------------------------
# unregister the specified queue
# ----------------------------------------------------------------------
#
class UnregisterQueue(AbstractResponseGenerator):
  #
  def __init__(self, **kwargs):
    parent = self.__class__.__bases__[0]
    pattern = parent._p_queue() + "\s*"
    required_keywords = ['queue_to_writers']
    super().__init__(pattern, required_keywords, kwargs)
    self.queue_to_writers = kwargs['queue_to_writers']
  #
  def generate_response(self, parsed_request_body):
    if parsed_request_body is None:  return (False, None)
    self.queue_to_writers.unregister_queue(parsed_request_body['queue'])
    return (True, None)


# ************************************************************************************************************
# define classes for exchanging messages with clients
# ************************************************************************************************************

# ----------------------------------------------------------------------
# request dispatcher class -
# -. accepts a request
# -. parses the request
# -. dispatches it to its respective handler
# ----------------------------------------------------------------------
#
class RequestDispatcher(object):
  #
  # pattern for overall request
  def p_request():  return "(?P<request_name>[A-Za-z]\w*)(\s+(?P<request_body>.*))?"
  #
  # ##### main methods ####
  #
  def __init__(self, queue_to_readers, queue_to_writers, reader_to_SAP):
    #
    # store required datasets in a dict for use by responders
    self.required_datasets = dict( { 'queue_to_readers': queue_to_readers, 'queue_to_writers': queue_to_writers, 'communicator_to_SAP': reader_to_SAP } )
    #
    # initialize the table of responders by request type
    self.request_to_responder = {
        'register_q':           RegisterQueue(**self.required_datasets),
        'set_reader_for_q':     RegisterReaderForQueue(**self.required_datasets),
        'set_writer_for_q':     RegisterWriterForQueue(**self.required_datasets),
        'qs_for_reader':        QueuesForReader(**self.required_datasets),
        'qs_for_writer':        QueuesForWriter(**self.required_datasets),
        'append_message_to_q':  AppendMessageToQueue(**self.required_datasets),
        'unset_reader_from_q':  UnregisterReaderFromQueue(**self.required_datasets),
        'unset_writer_from_q':  UnregisterWriterFromQueue(**self.required_datasets),
        'unset_communicator':   UnregisterEntity(**self.required_datasets),
        'unregister_q':         UnregisterQueue(**self.required_datasets)
    }
    # compile the pattern for separating requests into head and body portions
    self.request_pattern = re.compile(self.__class__.p_request())
  #
  # field a client's request by 
  # -. first checking for conformance to the basic  "request_type ...parameters..."  format, then
  # -. dispatching the request to the appropriate handler, as determined from the above table
  #  
  def __call__(self, request):
    #
    # first, attempt to separate the request's type -- i.e., its head field -- from the specifics -- i.e., its body
    match = self.request_pattern.match(request)
    if match is None:  return ('unknown', False, 'syntax error (bad format)')
    #
    # then, try to locate the particular request in the table of known requests
    match_dict = match.groupdict()
    request_type = match_dict['request_name']
    if request_type not in self.request_to_responder:  return (request_type, False, 'unknown request type')
    #
    # pass the body to whatever responder is indicated
    return ( request_type, ) + self.request_to_responder[request_type]( match_dict['request_body'] )
  #
  # auxiliary methods
  def me(self, methodname):  return "{}.{}".format(self.__class__.__name__, methodname)


# ================================================================================================================
# class that uses a message exchanger and a request dispatcher to respond to a request
# assumptions:
# -.  one request is required for one response
# -.  the dispatcher is a function that
#     -.  accepts two arguments:
#         -.  a request:  a one-line-long string
#         -.  a keywords object
#     -,  carries out any side effects implied by the request
#     -.  returns two values:
#         -.  a status
#         -.  a one-line response to the request:  a value of type (one-line string, None) - initially None
# ================================================================================================================
#
class RequestHandler(object):
  #
  def __init__(self, dispatcher):  self.dispatcher = dispatcher
  #
  # read the one-line request from the socket, generate the one-line response, respond via the socket, return the response and status
  #
  def respond(self, sock):
    request_type, status, response = 'unknown', False, None
    try:
      exchanger = OpenSocketMessageExchanger(sock)
      try:
        interim_status, request = exchanger.get_line( )
        if interim_status:
          request_type, interim_status, response_body = self.dispatcher( request )
          response = ("OK" if interim_status else "error") + ('' if response_body is None else " "+response_body)
          try:
            status = exchanger.put_line( response+'\n' ) and interim_status
          except Exception:
            print("{}: write failure".format(self.me('respond')), file=sys.stderr)
            status = False
      except Exception:
        print("{}: read failure".format(self.me('respond')), file=sys.stderr)
      finally:
        exchanger.close()
    except Exception:
      print("{}: connect failure".format(self.me('respond')), file=sys.stderr)
    return ( request, request_type, status, response )
  #
  def me(self, methodname):    return "{}.{}".format(self.__class__.__name__, methodname)
  def __repr__(self):          return "{}({!r})".format(self.__class__.__name__, self.dispatcher)
  def __eq__(self, other):     return isinstance( other, self.__class__ ) and self.dispatcher == other.dispatcher
