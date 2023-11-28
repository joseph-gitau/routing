packet = ['163.120.179.133 10.0.0.81 It 6']
packet = packet[0].split(' ')

sourceIP = packet[0]
destinationIP = packet[1]
payload = packet[2]
ttl = packet[3]

print(sourceIP)
print(destinationIP)
print(payload)
print(ttl)