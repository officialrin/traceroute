def get_route(hostname):
    timeLeft = TIMEOUT
    tracelist1 = []  # This is your list to use when iterating through each trace
    tracelist2 = []  # This is your list to contain all traces

    for ttl in range(1, MAX_HOPS):
        for tries in range(TRIES):
            destAddr = gethostbyname(str(hostname))

            # Fill in start
            icmp = getprotobyname("icmp")
            mySocket = socket(AF_INET, SOCK_RAW, icmp) # Make a raw socket named mySocket
            # Make a raw socket named mySocket
            # Fill in end

            mySocket.setsockopt(IPPROTO_IP, IP_TTL, struct.pack('I', ttl))
            mySocket.settimeout(TIMEOUT)
            try:
                d = build_packet()
                mySocket.sendto(d, (hostname, 0))
                t = time.time()
                startedSelect = time.time()
                whatReady = select.select([mySocket], [], [], timeLeft)
                howLongInSelect = (time.time() - startedSelect)
                if whatReady[0] == []:  # Timeout
                    tracelist1.append("* * * Request timed out.")
                    # Fill in start
                    # You should add the list above to your all traces list
                    tracelist2.append(tracelist1)
                    # Fill in end
                recvPacket, addr = mySocket.recvfrom(1024)
                timeReceived = time.time()
                timeLeft = timeLeft - howLongInSelect
                if timeLeft <= 0:
                    tracelist1.append("* * * Request timed out.")
                    # Fill in start
                    tracelist2.append(tracelist1)
                    # You should add the list above to your all traces list
                    # Fill in end
            except timeout:
                continue

            else:
                # Fill in start
                header = recvPacket[20:28]
                type, code, checksum, packID, seqNo = struct.unpack("bbHHh", header)
                # Fetch the icmp type from the IP packet
                # Fill in end
                try:  # try to fetch the hostname
                # Fill in start
                    hostname = gethostbyaddr(str(addr[0]))
                    print(hostname)
                # Fill in end
                except herror:  # if the host does not provide a hostname
                # Fill in start
                    hostname = ("Hostname not found.")
                # Fill in end

                if type == 11:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    # Fill in start
                    tracelist1.append((str(ttl), str(round((timeReceived - t) * 1000))+"ms", addr[0]))
                    tracelist2.append(tracelist1)
                    # You should add your responses to your lists here
                    # Fill in end
                elif type == 3:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    # Fill in start
                    tracelist1.append((str(ttl), str(round((timeReceived - t) * 1000))+"ms", addr[0]))
                    tracelist2.append(tracelist1)
                    # You should add your responses to your lists here
                    # Fill in end
                elif type == 0:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    # Fill in start
                    tracelist1.append((str(ttl), str(round((timeReceived - t) * 1000))+"ms", addr[0],ip_to_host(addr[0])))
                    tracelist2.append(tracelist1)
                    # You should add your responses to your lists here and return your list if your destination IP is met
                    # Fill in end
                    print(tracelist2)
                    print(tracelist1)
                    return tracelist2
                else:
                # Fill in start
                    tracelist1.append("Error.")
                    print("Error.")
                # If there is an exception/error to your if statements, you should append that to your list here
                # Fill in end
                break
            finally:
                mySocket.close()
