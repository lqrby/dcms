# -*- coding: utf-8 -*-
# TCP客户端的核心接口API是connect，由于TCP要求的是稳定传输，所以在后面数据传输前，需要借助三次握手的协议特点去实现连接。而connect函数则是三次握手协议的发起者。

from socket import *

# 创建socket

tcpClientSocket = socket(AF_INET, SOCK_STREAM)

# 链接服务器

serAddr = ('219.149.226.180', 7897)

tcpClientSocket.connect(serAddr)

# 提示用户输入数据

sendData = input("请输入要发送的数据：")

tcpClientSocket.send(sendData)

# 接收对方发送过来的数据，最大接收1024个字节

recvData = tcpClientSocket.recv(1024)

print('接收到的数据为:',recvData)

# 关闭套接字

tcpClientSocket.close()

# 5. TCP的连接状态

# 我们可以把刚刚的2个程序，放到2台虚拟机上，或者一台虚拟机，一台物理机上，然后使用wireshark抓包工具来对其通信过程进行数据包底层状态的分析。



# 可以看到图上，前3个包就是3次握手的结构。

# 中间2个包，是我们发送数据，服务器接收数据的包。

# 最后4个包，是连接断开后，进行的4次挥手的结构。

# 6. 三次握手的状态分析

# u 第一次握手：客户端首先将标志位SYN置为1，然后随机产生一个值seq=X的包，并将该数据包发送给server端，Client进入SYN_SENT状态，等待server确认。

# u 第二次握手：server收到数据包后由标志位SYN=1知道Client请求建立连接，Server将标志位SYN和ACK都置为1，ack numbern=X+1，随机产生一个值seq=K，并将该数据包发送给Client以确认连接请求，Server进入SYN_RCVD状态。

# u 第三次握手：Client收到确认后，检查ack number是否为X+1，ACK是否为1，如果正确则将标志位ACK置为1，ack=K+1，并将该数据包发送给Server，Server检查ack是否为K+1，ACK是否为1，如果正确则连接建立成功，Client和Server进入ESTABLISHED状态，完成三次握手，随后Client与Server之间可以开始传输数据了。
