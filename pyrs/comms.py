"""RsPy: Communication module
     SSHcomms       - connect to an RS Backend.
     commsLoopback  - loopback device for testing.
"""

import paramiko

class SSHcomms:

  def __init__(self, user, pwd, host, port):
    self.username = user
    self.password = pwd
    self.host = host;
    self.port = port;

  def connect(self)
    self.transport = paramiko.Transport((self.host, self.port))
    self.transport.connect(username = self.username, password = self.password)
    self.channel = self.transport.open_channel('session')
    self.channel.invoke_shell()

  def recv_ready(self):
    return self.channel.recv_ready();

  def recv(self, buflen):
    return self.channel.recv(buflen);

  def send(self, buffer):
    return self.channel.send(buffer);

  def close(self):
    self.channel.shutdown(2); # both directions.
    self.transport.close();


class commsLoopback:

  def __init__(self):
    self.stored = '';

  def connect(self):
    pass

  def recv_ready(self):
    return len(self.stored) > 0;

  def recv(self, buflen):
    if buflen > len(self.stored):
      raise Exception
    ans = self.stored[:buflen];
    self.stored = self.stored[buflen:];
    return ans;

  def send(self, buffer):
    self.stored += buffer;
    return;

