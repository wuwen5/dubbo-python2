# -*- coding: utf-8 -*-
import os
import socket
import struct

ip = None
heartbeat_id = 0


def num_2_byte_list(num):
    """
    convert num to byte list
    :param num:
    :return:
    """
    byte = []
    while num > 0:
        b = num & 0xff  # 获取最低位的一个字节的值
        byte.append(b)
        num = num >> 8  # 移除最低位的一个字节
    return list(reversed(byte))


def byte_list_2_num(byte):
    """
    convert byte list to num
    :param byte:
    :return:
    """
    num = 0
    for b in byte:
        num += b
        num = num << 8
    num = num >> 8  # 将最后一次的移位恢复
    return num


def double_to_long_bits(value):
    """
    https://gist.github.com/carlozamagni/187e478f516cac926682
    :param value:
    :return:
    """
    if value != value:
        return 0x7ff8000000000000L
    else:
        return struct.unpack('Q', struct.pack('d', value))[0]


def get_ip():
    global ip
    if ip:
        return ip
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(('8.8.8.8', 80))
        ip = sock.getsockname()[0]
    finally:
        sock.close()
    return ip


def get_pid():
    return os.getpid()


def get_heartbeat_id():
    global heartbeat_id
    heartbeat_id += 1
    heartbeat_id_byte = num_2_byte_list(heartbeat_id)
    while len(heartbeat_id_byte) < 8:
        heartbeat_id_byte = [0] + heartbeat_id_byte
    return heartbeat_id_byte


if __name__ == '__main__':
    for i in range(10):
        print get_ip()
