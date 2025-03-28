from machine import UART, Pin

class R4D3B16():
    FUNCTION_CONTROL_INSTRUCTION = 0x06
    FUNCTION_READ_STATUS = 0x03
    CMD_TURN_ON = 0x01
    CMD_SHUT_DOWN = 0x02
    STARTING_REGISTER_ADDRESS = 0x0001

    CONTROL_INSTRUCTION_RESPONSE_LEN = 8
    READ_STATUS_RESPONSE_LEN = 7

    DELAY = 0
    OPEN = 1
    CLOSED = 2
    NUM_OF_CHANNELS = 8

    def __init__(self):
        self.uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5), timeout=300)
        self.direction_pin = Pin(13, Pin.OUT)

    def get_check_sum(self, data):
        data = bytearray(data)
        crc = 0xFFFF
        for pos in data:
            crc ^= pos
            for i in range(8):
                if ((crc & 1) != 0):
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1
        return [crc >> 0 & 0xff, crc >> 8 & 0xff]

    def get_address_channel_from_index(self, index):
        index = index - 1
        address = int(index / self.NUM_OF_CHANNELS) + 1
        channel = index % self.NUM_OF_CHANNELS + 1
        return address, channel

    def generate_control_instruction(self, cmd, index):
        packet = []
        address, channel = self.get_address_channel_from_index(index)
        packet.append(address)
        packet.append(self.FUNCTION_CONTROL_INSTRUCTION)
        packet.append((channel & 0xff00) >> 8)
        packet.append(channel & 0x00ff)
        packet.append(cmd)
        packet.append(self.DELAY)
        check_sum = self.get_check_sum(packet)
        packet.append(check_sum[0])
        packet.append(check_sum[1])
        return packet

    def generate_read_status(self, index):
        packet = []
        address, channel = self.get_address_channel_from_index(index)
        packet.append(address)
        packet.append(self.FUNCTION_READ_STATUS)
        packet.append((channel & 0xff00) >> 8)
        packet.append(channel & 0x00ff)
        packet.append((self.STARTING_REGISTER_ADDRESS & 0xff00) >> 8)
        packet.append(self.STARTING_REGISTER_ADDRESS & 0x00ff)
        check_sum = self.get_check_sum(packet)
        packet.append(check_sum[0])
        packet.append(check_sum[1])
        return packet

    def write(self, packet):
        self.direction_pin.value(1)
        self.uart.write(bytes(packet))
        self.uart.flush()

    def read(self, len):
        self.direction_pin.value(0)
        ret = self.uart.read(len)
        if ret is not None:
            return list(ret)
        return []

    def set_relay_on(self, index):
        packet = self.generate_control_instruction(self.CMD_TURN_ON, index)
        self.write(packet)
        read_packet = self.read(self.CONTROL_INSTRUCTION_RESPONSE_LEN)
        if read_packet is not None and len(read_packet) == self.CONTROL_INSTRUCTION_RESPONSE_LEN:
            crc = read_packet[-2:]
            expected_crc = self.get_check_sum(read_packet[:-2])
            if expected_crc == crc:
                address = read_packet[0]
                function = read_packet[1]
                channel = (read_packet[2] << 8) + read_packet[3]
                state = read_packet[4]
                expected_address, expected_channel = self.get_address_channel_from_index(index)
                if address == expected_address and function == self.FUNCTION_CONTROL_INSTRUCTION and channel == expected_channel:
                    return state == self.OPEN
        print("set_relay_on: wrong result, data is not the same")
        return False

    def set_relay_off(self, index):
        packet = self.generate_control_instruction(self.CMD_SHUT_DOWN, index)
        self.write(packet)
        read_packet = self.read(self.CONTROL_INSTRUCTION_RESPONSE_LEN)
        if read_packet is not None and len(read_packet) == self.CONTROL_INSTRUCTION_RESPONSE_LEN:
            crc = read_packet[-2:]
            expected_crc = self.get_check_sum(read_packet[:-2])
            if expected_crc == crc:
                address = read_packet[0]
                function = read_packet[1]
                channel = (read_packet[2] << 8) + read_packet[3]
                state = read_packet[4]
                expected_address, expected_channel = self.get_address_channel_from_index(index)
                if address == expected_address and function == self.FUNCTION_CONTROL_INSTRUCTION and channel == expected_channel:
                    return state == self.CLOSED
        print("set_relay_off: wrong result, data is not the same")
        return False

    def get_relay_state(self, index):
        packet = self.generate_read_status(index)
        self.write(packet)
        read_packet = self.read(self.READ_STATUS_RESPONSE_LEN)
        if read_packet is not None and len(read_packet) == self.READ_STATUS_RESPONSE_LEN:
            crc = read_packet[-2:]
            expected_crc = self.get_check_sum(read_packet[:-2])
            if expected_crc == crc:
                address = read_packet[0]
                function = read_packet[1]
                data_len = read_packet[2]
                relay_status = (read_packet[3] << 8) + read_packet[4]
                expected_address, expected_channel = self.get_address_channel_from_index(index)
                if address == expected_address and function == self.FUNCTION_READ_STATUS and data_len == 2:
                    return relay_status
        print("get_relay_state: can't parse")
        return None

    def is_responsive(self):
        return self.get_relay_state(0x01) is not None
