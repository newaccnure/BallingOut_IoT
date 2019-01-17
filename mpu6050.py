#!/usr/bin/python

import smbus
import time
import sys
import csv

# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
bus = smbus.SMBus(0)  # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68  # This is the address value read via the i2cdetect command


def read_byte(adr):
    return bus.read_byte_data(address, adr)


def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr + 1)
    val = (high << 8) + low
    return val


def read_word_2c(adr):
    val = read_word(adr)
    if val >= 0x8000:
        return -((65535 - val) + 1)
    else:
        return val


def record_data(execution_time, frequency):
    # execution_time = 3
    # frequency = 10

    feature_number = 6
    records_number = execution_time * frequency
    # Now wake the 6050 up as it starts in sleep mode
    bus.write_byte_data(address, power_mgmt_1, 0)

    data = [[0] * feature_number] * records_number

    for i in range(records_number):
        # Getting data from MPU6050
        gyro_xout = read_word_2c(0x43)
        gyro_yout = read_word_2c(0x45)
        gyro_zout = read_word_2c(0x47)
        accel_xout = read_word_2c(0x3b)
        accel_yout = read_word_2c(0x3d)
        accel_zout = read_word_2c(0x3f)

        gyro_xout_scaled = gyro_xout / 131.0
        gyro_yout_scaled = gyro_yout / 131.0
        gyro_zout_scaled = gyro_zout / 131.0

        accel_xout_scaled = accel_xout / 16384.0
        accel_yout_scaled = accel_yout / 16384.0
        accel_zout_scaled = accel_zout / 16384.0

        # Add data to array
        data[i] = [gyro_xout_scaled,
                   gyro_yout_scaled,
                   gyro_zout_scaled,
                   accel_xout_scaled,
                   accel_yout_scaled,
                   accel_zout_scaled]

        # Print out to console
        print("Gyro data:",
              "gyro_x: ", round(gyro_xout_scaled, 2),
              "gyro_y: ", round(gyro_yout_scaled, 2),
              "gyro_z: ", round(gyro_zout_scaled, 2),
              "Accelerometer data:",
              "accel_x: ", round(accel_xout_scaled, 2),
              "accel_y: ", round(accel_yout_scaled, 2),
              "accel_z: ", round(accel_zout_scaled, 2), end='\r')

        sys.stdout.flush()
        time.sleep(1 / frequency)

    print()
    return data
