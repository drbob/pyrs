""" Simplify Auth for git commits of pyrs """

# This module allows the use of a file with auth parameters.
# so that I don't have to continually remove auth stuff from the examples.
#
# Its a simple system - doesn't allow spaces in passwords!


class Auth:
  def __init__(self):
    self.haveParams = False;

    # expected auth parameters.
    self.user = 'user'
    self.port = 7022
    self.host = '127.0.0.1'
    self.pwd = None # This is only required parameter, really.

    self.tryFileLoad('auth.txt');

  def setUser(self, user):
    self.user = user;

  def setHost(self, host):
    self.host = host;

  def setPort(self, port):
    self.port = port;

  def setIpPort(self, ip, port):
    self.host = ip;
    self.port = port;

  def setPwd(self, pwd):
    self.pwd = pwd;
    self.haveParams = True; # as last required.

  def tryFileLoad(self, filename):
    with open( filename, "r" ) as fd:
      for line in fd:
        data = line.split();
        if len(data) != 2:
          print "pyrs.auth.Auth.tryFileLoad() Error Parsing Line: %s" % (line)
          continue;
        if data[0] == 'port':
          self.setPort(int(data[1]));
        elif data[0] == 'host':
          self.setHost(data[1]);
        elif data[0] == 'pwd':
          self.setPwd(data[1]);
        elif data[0] == 'user':
          self.setUser(data[1]);
        else:
          print "pyrs.auth.Auth.tryFileLoad() Error Parsing Line: %s" % (line)
  
      if not self.haveParams:
        print "pyrs.auth.Auth.tryFileLoad() Warning: Not enough to Auth User"
      else:
        print "pyrs.auth.Auth.tryFileLoad() Loaded Auth Parameters!"
      return;
    print "pyrs.auth.Auth.tryFileLoad() Couldn't open Auth file %s" % (filename);


