import socket
import sys
import time
import os
import glob


# Helper Functions

# The purpose of this function is to set up a socket connection.
def create_socket(host, port):
    # 1. Create a socket.
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2. Try connecting the socket to the host and port.
    try:
        soc.connect((host, port))
    except:
        print("Connection Error to", port)
        sys.exit()
    # 3. Return the connected socket.
    return soc


# The purpose of this function is to read in a CSV file.
def read_csv(path):
    # 1. Open the file for reading.
    table_file = open(path, "r")
    # 2. Store each line.
    table = table_file.readlines()
    # 3. Create an empty list to store each processed row.
    table_list = []
    # 4. For each line in the file:
    for line in table:
        # 5. split it by the delimiter,
        row = line.strip().split(',')
        # 6. remove any leading or trailing spaces in each element, and
        row = [r.strip() for r in row]
        # 7. append the resulting list to table_list.
        table_list.append(row)
    # 8. Close the file and return table_list.
    table_file.close()
    return table_list


# The purpose of this function is to find the default port
# when no match is found in the forwarding table for a packet's destination IP.
def find_default_gateway(table):
    # 1. Traverse the table, row by row,
    for row in table:
        # 2. and if the network destination of that row matches 0.0.0.0,
        if row[0] == '0.0.0.0':
            # 3. then return the interface of that row.
            return row[3]


# The purpose of this function is to generate a forwarding table that includes the IP range for a given interface.
# In other words, this table will help the router answer the question:
# Given this packet's destination IP, which interface (i.e., port) should I send it out on?
def generate_forwarding_table_with_range(table):
    # 1. Create an empty list to store the new forwarding table.
    new_table = []
    # 2. Traverse the old forwarding table, row by row,
    for row in table:
        # 3. and process each network destination other than 0.0.0.0
        # (0.0.0.0 is only useful for finding the default port).
        if row[0] != '0.0.0.0':
            # 4. Store the network destination and netmask.
            network_dst_string = row[0]
            netmask_string = row[1]
            # 5. Convert both strings into their binary representations.
            network_dst_bin = ip_to_bin(network_dst_string)
            netmask_bin = ip_to_bin(netmask_string)
            # 6. Find the IP range.
            ip_range = find_ip_range(network_dst_bin, netmask_bin)
            # 7. Build the new row.
            new_row = [network_dst_string, netmask_string,
                       ip_range[0], ip_range[1], row[3]]
            # 8. Append the new row to new_table.
            new_table.append(new_row)
    # 9. Return new_table.
    return new_table


def ip_to_bin(ip):
    # Split the IP into octets and convert each octet to an integer
    ip_octets = [int(octet) for octet in ip.split('.')]

    # Perform bitwise shifting to create the 32-bit representation of the IP
    ip_int = (ip_octets[0] << 24) + (ip_octets[1] << 16) + \
        (ip_octets[2] << 8) + ip_octets[3]

    return ip_int


# The purpose of this function is to find the range of IPs inside a given a destination IP address/subnet mask pair.
def find_ip_range(network_dst, netmask):
    # Perform a bitwise AND on the network destination and netmask
    # to get the minimum IP address in the range.
    min_ip = network_dst & netmask

    # Calculate the maximum IP address in the range.
    # To obtain the maximum IP in the range, apply a bitwise OR
    # between the network destination and the bitwise NOT of the netmask.
    max_ip = network_dst | ~netmask

    # Return a list containing the minimum and maximum IP in the range.
    return [min_ip, max_ip]


# The purpose of this function is to perform a bitwise NOT on an unsigned integer.
def bit_not(n, numbits=32):
    return (1 << numbits) - 1 - n


# The purpose of this function is to write packets/payload to file.
def write_to_file(path, packet_to_write, send_to_router=None):
    # 1. Open the output file for appending.
    out_file = open(path, "a")
    # 2. If this router is not sending, then just append the packet to the output file.
    if send_to_router is None:
        out_file.write(packet_to_write + "\n")
    # 3. Else if this router is sending, then append the intended recipient, along with the packet, to the output file.
    else:
        out_file.write(packet_to_write + " " +
                       "to Router " + send_to_router + "\n")
    # 4. Close the output file.
    out_file.close()


def write_to_file(path, packet_to_write, send_to_router=None):
    # 1. Open the output file for appending.
    out_file = open(path, "a")
    # 2. If this router is not sending, then just append the packet to the output file.
    if send_to_router is None:
        out_file.write(packet_to_write + "\n")
    # 3. Else if this router is sending, then append the intended recipient, along with the packet, to the output file.
    else:
        out_file.write(packet_to_write + " " +
                       "to Router " + send_to_router + "\n")
    # 4. Close the output file.
    out_file.close()

    # The purpose of this function is to receive and process incoming packets.


def send_packets():
    # 0. Remove any output files in the output directory
    # (this just prevents you from having to manually delete the output files before each run).
    files = glob.glob('output/*')
    for f in files:
        os.remove(f)

    # 1. Connect to the appropriate sending ports (based on the network topology diagram).
    soc_2 = create_socket('127.0.0.1', 8002)
    soc_4 = create_socket('127.0.0.1', 8004)

    # 2. Read in and store the forwarding table.
    forwarding_table = read_csv('input/router_1_table.csv')
    # 3. Store the default gateway port.
    default_gateway_port = find_default_gateway(forwarding_table)
    # 4. Generate a new forwarding table that includes the IP ranges for matching against destination IPS.
    forwarding_table_with_range = generate_forwarding_table_with_range(
        forwarding_table)

    # 5. Read in and store the packets.
    packets_table = read_csv('input/packets.csv')

    # 6. For each packet,
    for packet in packets_table:
        # packet structure: 163.120.179.133,10.0.0.81,It,7
        # 7. Store the source IP, destination IP, payload, and TTL.
        # packet = packet[0].split(',')
        # 5. Store the source IP, destination IP, payload, and TTL.
        sourceIP = packet[0]
        destinationIP = packet[1]
        payload = packet[2]
        ttl = packet[3]

        # 6. Decrement the TTL by 1 and construct a new packet with the new TTL.
        new_ttl = str(int(ttl) - 1)

        new_packet = f"{sourceIP},{destinationIP},{payload},{new_ttl}"
        # Check if TTL has reached zero, and discard the packet if so.
        if int(new_ttl) <= 0:
            print("Packet TTL expired. Discarding packet.")
            write_to_file('output/discarded_by_router_2.txt', new_packet)
            continue  # Skip forwarding for this packet

        # 7. Convert the destination IP into an integer for comparison purposes.
        destinationIP_int = ip_to_bin(destinationIP)
        destinationIP_int = destinationIP_int

        # 8. Find the appropriate sending port to forward this new packet to.
        sending_port = None
        for row in forwarding_table_with_range:
            network_dst_string = row[0]
            netmask_string = row[1]
            network_dst_bin = ip_to_bin(network_dst_string)
            netmask_bin = ip_to_bin(netmask_string)
            destinationIP_int = ip_to_bin(destinationIP)

            # Find the IP range using bitwise operations
            min_ip = network_dst_bin & netmask_bin
            max_ip = network_dst_bin | bit_not(netmask_bin)

            if min_ip <= destinationIP_int <= max_ip:
                sending_port = row[4]
                break

        # 10. If no port is found, then set the sending port to the default port.
        if sending_port is None:
            sending_port = default_gateway_port

        # 11. Either
        # (a) send the new packet to the appropriate port (and append it to sent_by_router_1.txt),
        # (b) append the payload to out_router_1.txt without forwarding because this router is the last hop, or
        # (c) append the new packet to discarded_by_router_1.txt and do not forward the new packet
        if sending_port == '8002':
            print("sending packet", new_packet, "to Router 2")
            write_to_file('output/sent_by_router_1.txt',
                          new_packet, send_to_router=sending_port)
            soc_2.send(new_packet.encode())
        elif sending_port == '8004':
            print("sending packet", new_packet, "to Router 4")
            write_to_file('output/sent_by_router_1.txt',
                          new_packet, send_to_router=sending_port)
            soc_4.send(new_packet.encode())
        elif sending_port == '127.0.0.1':
            print("OUT:", payload)
            write_to_file('output/out_router_1.txt', payload)

        else:
            print("DISCARD:", new_packet)
            write_to_file('output/discarded_by_router_1.txt', new_packet)

        # Sleep for some time before sending the next packet (for debugging purposes)
        time.sleep(1)


if __name__ == "__main__":
    send_packets()
