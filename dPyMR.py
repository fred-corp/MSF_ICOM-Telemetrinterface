import time
import serial

class Transceiver :
  def __init__(self, dPyMRserial, ownID, timeout = 2):
    self.dPyMRserial = dPyMRserial
    self.ownID = ownID
    self.timeout = timeout
    self.ownID = ownID

    self.bol = b'\x02'
    self.eol = b'\x03'

  def discover(self, idRange = (0, 9999999)) :
    # TODO: Implement this function
    return ()

  def sendCommand(self, command):
    data = self.bol + command.encode("utf-8") + self.eol
    self.dPyMRserial.write(data)

  def sendMessage(self, message, otherID):
    command = '*SET,DPMR,TXMSG,IND,{},{},MSG,"{}",ACK'.format(str(otherID).zfill(7), str(self.ownID).zfill(7), message)
    
    self.sendCommand(command)
    
    response = b'' 
    byteread = b''
    beginTime = time.time()
    while not '*NTF,DPMR,TXMSG,IND,' in str(response.decode('utf-8')) :
      if(time.time() - beginTime > self.timeout):
        if(response == b''):
          return 'TIMEOUT_ERROR'
      byteread = self.dPyMRserial.read() #Read one byte, stuff it in a temp variable
      response += byteread #Add it to the read string
    while not (byteread==self.eol): #While we haven't received eol
      byteread = self.dPyMRserial.read() #Read one byte, stuff it in a temp variable
      response += byteread #Add it to the read string

    if '"' + message + '",ACK,OK' in str(response.decode('utf-8')) :
      return 'ACK_OK'
    elif '"' + message + '",ACK,NG' in str(response.decode('utf-8')) :
      return 'ACK_NG'
    else :
      return 'UNKNOWN_ERROR'