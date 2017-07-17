import re

COMMANDS = ['/join', '/create', '/set_alias', '/block', '/unblock', '/delete']


def parse_command(msg):
  
  #Removes any initial white space
  x = re.compile('\s*')
  m = x.match(msg, 0)
  offest = m.end()
  
  #Check for command special character
  
  x = re.compile('[/][a-z]+[_]?[a-z]*')
  m = x.match(msg, offest)
  
  #String matches command patern
  if(m):
    offset = m.end()
    cmd = m.group(0)
    print(cmd)
    
    #String is a valid command
    if(cmd in COMMANDS):
      x = re.compile('[A-za-z0-9]+')
      m = x.search(msg, offset)
      parm = m.group(0)
      print(parm)
    
    #String isn't a valid command
    else:
      print('Unknown Command: "' + cmd + '"')
    
  #String isn't a Command
  else:
    print("No Match")
 
 
    
#***Main

s = 'hello'
t = '/hello'
zz = '/set_alias Joel'

parse_command(s)
parse_command(t)
parse_command(zz)


#http://www.bogotobogo.com/python/python_network_programming_tcp_server_client_chat_server_chat_client_select.php
