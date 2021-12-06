"""Some simple wrapper functions to control a Zaber device using the binary 
protocol.
This module allows to connect to a Zaber device and do some conversion
calculations
Features:
- Connect to a Zaber device
- Conversions of distance and velocity to and from microsteps and millimeter

Adjust the parameters between the dashed lines according to your device.
For detailed information and an example, see the README.TXT file shipped with
this module.
Copyright (C) 2018 Pieter Vandemaele
Distributed under the terms of the GNU General Public License (GPL).
"""

from zaber_motion import Library
from zaber_motion import DeviceDbSourceType
from zaber_motion import LogOutputMode
from zaber_motion import Units, FirmwareVersion, Measurement, Tools
from zaber_motion.binary import Connection
from zaber_motion.binary import DeviceSettings
from zaber_motion.binary import BinarySettings
from zaber_motion.binary import DeviceType
from zaber_motion.binary import CommandCode, ReplyCode, ErrorCode
from zaber_motion.binary import DeviceIdentity
from zaber_motion.binary import ReplyOnlyEvent


class zaber_tools:
    # #### ZABER SPECIFIC SETTINGS
    # microstep_size = 0.49609375  # T-LSR150B
    
    # ADJUST THE PARAMETERS BETWEEN THE DASHED LINES
    # -------------------------------------------------
    zb_max_speed = 20  # mm/s2
    zb_steps_per_revolution = 200
    zb_linear_motion_per_revolution = 25.4  # mm
    # -------------------------------------------------
    
    
    zb_microstep_size = 0  # µm
    zb_microstep_resolution = 0  # steps
    connection = []

    # #### CONVERSION FUNCTIONS
    # Convention
    # data = data returned from the device
    # vel = velocity sent to system

    def __init__(self, com_port='COM9'):
        self.com_port = com_port
        try:
            # Update device database
            Library.enable_device_db_store()  # default file
            Library.enable_device_db_store("./device-db-store")  # custom file

            # Connect to device
            self.connection = Connection.open_serial_port(self.com_port)
            device_list = self.connection.detect_devices()
            self.device = device_list[0]
            self.device.identify()

            # Retrieve some information
            resp = self.connection.generic_command(1, CommandCode.RETURN_SETTING,  37, timeout=0.0, check_errors=True)
            self.zb_microstep_resolution = resp.data
            self.zb_microstep_size = self.zb_linear_motion_per_revolution / (self.zb_steps_per_revolution * self.zb_microstep_resolution * 4) * 1000  # what is 4?

            self.errorDict = {1: ['Cannot home', 'Home - Device has traveled a long distance without triggering the home sensor. Device may be stalling or slipping.'],
                              2: ['Device number invalid', 'Renumbering data out of range.'],
                              14: ['Voltage low', 'Power supply data too low.'],
                              15: ['Voltage high', 'Power supply data too high.'],
                              18: ['Stored position invalid', 'The position stored in the requested register is no longer valid. This is probably because the maximum range was reduced.'],
                              20: ['Absolute position invalid', 'Move Absolute - Target position out of range.'],
                              21: ['Relative position invalid', 'Move Relative - Target position out of range.'],
                              22: ['Velocity invalid', 'Constant velocity move. Velocity out of range.'],
                              36: ['Peripheral ID invalid', 'Restore Settings - peripheral id is invalid. Please use one of the peripheral ids listed in the user manual, or 0 for default.'],
                              37: ['Resolution invalid', 'Invalid microstep resolution. Resolution may only be 1, 2, 4, 8, 16, 32, 64, 128.'],
                              38: ['Run current invalid', 'Run current out of range. See command 38 for allowable values.'],
                              39: ['Hold current invalid', 'Hold current out of range. See command 39 for allowable values.'],
                              40: ['Mode invalid', 'Set Device Mode - one or more of the mode bits is invalid'],
                              41: ['Home speed invalid', 'Home speed out of range. The range of home speed is determined by the resolution.'],
                              42: ['Speed invalid', 'Target speed out of range. The range of target speed is determined by the resolution.'],
                              43: ['Acceleration invalid', 'Target acceleration out of range. The range of target acceleration is determined by the resolution'],
                              44: ['Maximum range invalid', 'The maximum range may only be set between 1 and the resolution limit of the stepper controller, which is 16,777,215.'],
                              45: ['Current position invalid', 'Current position out of range. Current position must be between 0 and the maximum range.'],
                              46: ['Maximum relative move invalid', 'Max relative move out of range. Must be between 0 and 16,777,215.'],
                              47: ['Offset invalid', 'Home offset out of range. Home offset must be between 0 and maximum range.'],
                              48: ['Alias invalid', 'Alias out of range.'],
                              49: ['Lock state invalid', 'Lock state must be 1 (locked) or 0 (unlocked).'],
                              53: ['Setting invalid', 'Return Setting - data entered is not a valid setting command number. Valid setting command numbers are the command numbers of any "Set ..." instructions.'],
                              64: ['Command invalid', 'Command number not valid in this firmware version.'],
                              255: ['Busy', 'Another command is executing and cannot be pre-empted. Either stop the previous command or wait until it finishes before trying again.'],
                              1600: ['Save position invalid', 'Save Current Position register out of range (must be 0-15).'],
                              1601: ['Save position not homed', 'Save Current Position is not allowed unless the device has been homed.'],
                              1700: ['Return position invalid', 'Return Stored Position register out of range (must be 0-15).'],
                              1800: ['Move position invalid', 'Move to Stored Position register out of range (must be 0-15).'],
                              1801: ['Move position not homed', 'Move to Stored Position is not allowed unless the device has been homed.'],
                              2146: ['Relative position limited', 'Move Relative (command 20) exceeded maximum relative move range. Either move a shorter distance, or change the maximum relative move (command 46).'],
                              3600: ['Settings locked', 'Must clear Lock State (command 49) first. See the Set Lock State command for details.'],
                              4008: ['Disable auto home invalid', 'Set Device Mode - this is a linear actuator; Disable Auto Home is used for rotary actuators only.'],
                              4010: ['Bit 10 invalid', 'Set Device Mode - bit 10 is reserved and must be 0.'],
                              4012: ['Home switch invalid', 'Set Device Mode - this device has integrated home sensor with preset polarity; mode bit 12 cannot be changed by the user.'],
                              4013: ['Bit 13 invalid', 'Set Device Mode - bit 13 is reserved and must be 0.']}

        except Exception as ex:
            raise ex

        else:
            print('ZABER DEVICE INFORMATION')
            print('------------------------')
            print('Maximum speed: {} mm/s'.format(self.zb_max_speed))
            print('Steps per revolution: {} steps'.format(self.zb_steps_per_revolution))
            print('Linear motion per revolution: {} mm'.format(self.zb_linear_motion_per_revolution))
            print('Microstep size: {} µm'.format(self.zb_microstep_size))
            print('Microstep resolution: {} steps'.format(self.zb_microstep_resolution))

    def dist_mm_to_mustep(self, dist_mm):
        # Convert mm to microsteps
        dist_microns = dist_mm * 1000.
        dist_microsteps = dist_microns / self.zb_microstep_size
        rounded_dist_microsteps = int(round(dist_microsteps))
        return rounded_dist_microsteps

    def dist_mustep_to_mm(self, dist_microsteps):
        # Convert microsteps to mm
        return dist_microsteps * self.zb_microstep_size * 0.001

    def dist_data_to_mustep(self, data):
        # Convert data to microsteps
        return data

    def dist_data_to_mm(self, data):
        # Convert data to mm
        return self.dist_mustep_to_mm(data)

    def vel_data_to_mustep_per_s(self, data):
        # Convert velocity to microsteps per second
        return data * 9.375

    def vel_data_to_mm_per_s(self, data):
        # Convert velocity to microsteps per second
        return self.dist_mustep_to_mm(data) * 9.375

    def vel_mustep_per_s_to_vel(self, vel):
        # Convert microsteps per second to velocity
        return vel / 9.375

    def vel_mm_per_s_to_vel(self, vel):
        # Convert microsteps per second to velocity
        return self.dist_mm_to_mustep(vel) / 9.375
