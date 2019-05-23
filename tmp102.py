import time
import smbus

i2c_ch = 1

i2c_address = 0x48

reg_temp = 0x00
reg_config = 0x01


def twos_comp(val, bits):
    if(val & (1 << (bits - 1))) != 0:
       val = val - (1 << bits)
    return val

def read_temp():

    val = bus.read_i2c_block_data(i2c_address, reg_temp, 2)
    temp_c = (val[0] << 4) | (val[1] >> 5)

    temp_c = twos_comp(temp_c, 12)

    temp_c = temp_c * 0.0625

    return temp_c

bus = smbus.SMBus(i2c_ch)

val = bus.read_i2c_block_data(i2c_address, reg_config, 2)
print("old CONFIG:", val)


val[1] = val[1] & 0b00111111
val[1] = val[1] | (0b10 << 6)

bus.write_i2c_block_data(i2c_address, reg_config, val)

val = bus.read_i2c_block_data(i2c_address, reg_config, 2)
print("New CONFIG:", val)


while True:
    temperature = read_temp()
    print(round(temperature, 2), "C")
    time.sleep(1)

