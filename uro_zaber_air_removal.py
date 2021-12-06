from psychopy import core, clock, visual, event, gui, logging
import time
from datetime import datetime
from math import floor, ceil
import numpy as np
import zaber_tools
from zaber_motion.binary import CommandCode, BinarySettings
from zaber_motion import Units, FirmwareVersion, Measurement, Tools
# from zaber_motion import BinaryCommandFailedExceptionData

# ######################################################################
# HELPER FUNCTIONS
# ######################################################################


def print_log(txt):
    # PRINT
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    print('> {} {}'.format(dt_string, txt))

# ######################################################################
# SET PARAMETERS
# ######################################################################

comPort_Zaber = 'COM9'  # expInfo['COM Port (Zaber)']
target_speed = 10
speed_factor = 2/3

demo = False

if demo:
    wait_val = True
else:
    wait_val = False

# ######################################################################
# EXPERIMENT INFO
# ######################################################################

# ######################################################################
# PREPARE PSYCHOPY
# ######################################################################
# Window
win = visual.Window([1280, 1024], monitor="testMonitor", units="norm")
win.update()
event.waitKeys()
# ######################################################################
# DASHBOARD
# ######################################################################
margin = 0.05

# Color lut for text
col_lut = {
    'white': (255, 255, 255),
    'yellow': (255, 198, 28),
    'blue': (51, 167, 202),
    'red': (217, 95, 43),
    'green': (124, 179, 62)
    }

col_titleBox = (31, 42, 53)

# Color lut for graphical elements
col_background = (21, 35, 46)
col_paneHdr = (75, 100, 129)
col_paneBox = (48, 63, 81)
col_panetitletext = (1, 1, 1)
col_panebodytext = (1, 1, 1)

win.colorSpace = 'rgb255'
win.color = col_background
win.update()

height_title = 0.18
height_info = 0.25
height_cont = 0.10
height_cntr = 0.0
height_copyr = 0.05
height_hdr = 0.1

# # PARAMETERS INITIALISATION

# ## TITLE
rect_titleBox_size = np.array([1, height_title])
rect_titleBox_pos = np.array([rect_titleBox_size[0]/2, 1-rect_titleBox_size[1]/2])

txt_titleBox_pos = rect_titleBox_pos.copy()
txt_titleBox_wrap = rect_titleBox_size[0] - 0.05

# ## INFO
rect_infoBox_size = np.array([1 - 2*margin, height_info])
rect_infoHdr_size = np.array([rect_infoBox_size[0], 0.1])

rect_infoBox_pos = np.array([rect_infoBox_size[0]/2+margin, 0.5])
rect_infoHdr_pos = np.array([rect_infoBox_pos[0], rect_infoBox_pos[1] + rect_infoHdr_size[1]/2 + rect_infoBox_size[1]/2])

txt_infoBox_pos = rect_infoBox_pos.copy()
txt_infoBox_wrap = rect_infoBox_size[0] - 0.05

txt_infoHdr_pos = rect_infoHdr_pos.copy()
txt_infoHdr_wrap = rect_infoHdr_size[0] - 0.05

# ## CONTINUE
rect_contBox_size = np.array([1 - 2*margin, height_cont])
rect_contBox_pos = np.array([rect_contBox_size[0]/2+margin, height_copyr + 2*margin + rect_contBox_size[1]/2])

txt_contBox_pos = rect_contBox_pos.copy()
txt_contBox_wrap = rect_contBox_size[0] - 0.05

# ## COPYRIGHT
txt_copyr_size = np.array([1, height_copyr])
txt_copyr_pos = np.array([txt_copyr_size[0]/2, txt_copyr_size[1]/2])
txt_copyr_wrap = txt_copyr_size[0] - 0.05

# # PARAMETERS UPDATE
# ## TITLE
rect_titleBox_pos = (rect_titleBox_pos*2)-1
rect_titleBox_size = rect_titleBox_size*2

txt_titleBox_pos = (txt_titleBox_pos*2)-1
txt_titleBox_wrap = txt_titleBox_wrap*2

# ## INFO
rect_infoBox_pos = (rect_infoBox_pos*2)-1
rect_infoBox_size = rect_infoBox_size*2

rect_infoHdr_pos = (rect_infoHdr_pos*2)-1
rect_infoHdr_size = rect_infoHdr_size*2

txt_infoBox_pos = (txt_infoBox_pos*2)-1
txt_infoBox_wrap = txt_infoBox_wrap*2

txt_infoHdr_pos = (txt_infoHdr_pos*2)-1
txt_infoHdr_wrap = txt_infoHdr_wrap*2

# ## CONTINUE
rect_contBox_pos = (rect_contBox_pos*2)-1
rect_contBox_size = rect_contBox_size*2

txt_contBox_pos = (txt_contBox_pos*2)-1
txt_contBox_wrap = txt_contBox_wrap*2

# ## COPYRIGHT
txt_copyr_pos = (txt_copyr_pos*2)-1
txt_copyr_wrap = txt_copyr_wrap*2

# # VISUAL COMPONENTS
# ## TITLE
# ### RECTANGLES
rect_titleBox = visual.Rect(
    win=win,
    size=rect_titleBox_size,
    pos=rect_titleBox_pos,
    lineWidth=1.0, colorSpace='rgb255', lineColor=col_paneBox, fillColor=col_titleBox,
    opacity=None, depth=-1.0, interpolate=True, autoDraw=False)

# ### TEXT
txt_titleBox = visual.TextStim(
    win=win,
    pos=txt_titleBox_pos,
    height=0.15, alignText='center', text="URO-MRI\nAIR REMOVAL TOOL", wrapWidth=txt_titleBox_wrap)

# ## INFO
# ### RECTANGLES
rect_infoBox = visual.Rect(
    win=win,
    size=rect_infoBox_size,
    pos=rect_infoBox_pos,
    lineWidth=1.0, colorSpace='rgb255', lineColor=col_paneBox, fillColor=col_paneBox,
    opacity=None, depth=-1.0, interpolate=True, autoDraw=False)

rect_infoHdr = visual.Rect(
    win=win,
    size=rect_infoHdr_size,
    pos=rect_infoHdr_pos,
    lineWidth=1.0, colorSpace='rgb255', lineColor=col_paneHdr, fillColor=col_paneHdr,
    opacity=None, depth=-1.0, interpolate=True, autoDraw=False)

# ### TEXT
txt_infoHdr = visual.TextStim(
    win=win,
    pos=txt_infoHdr_pos,
    height=0.15, alignText='left', text="Command", wrapWidth=txt_infoHdr_wrap)

txt_infoBox = visual.TextStim(
    win=win,
    pos=txt_infoBox_pos,
    height=0.12, alignText='left', text="Here comes the command", wrapWidth=txt_infoBox_wrap)

# ## CONTINUE
# ### RECTANGLES
rect_contBox = visual.Rect(
    win=win,
    size=rect_contBox_size,
    pos=rect_contBox_pos,
    lineWidth=1.0, colorSpace='rgb255', lineColor=col_paneBox, fillColor=col_paneBox,
    opacity=None, depth=-1.0, interpolate=True, autoDraw=False)

# ### TEXT
txt_contBox = visual.TextStim(
    win=win,
    pos=txt_contBox_pos,
    height=0.10, alignText='center', text="Here comes the command", wrapWidth=txt_contBox_wrap)

# ## COPYRIGHT
# ### RECTANGLES

# ### TEXT
txt_copyr = visual.TextStim(
    win=win,
    pos=txt_copyr_pos,
    height=0.05, alignText='left', text="(C) 2021 Pieter Vandemaele", wrapWidth=txt_copyr_wrap)

# ######################################################################
# OTHER GRAPHICAL COMPONENTS
# ######################################################################

# ######################################################################
# OTHER INITIALIZATION
# ######################################################################


# ######################################################################
# FUNCTIONS
# ######################################################################
def zaber_connect(comPort):
    # OPEN A ZABER CONNECTION
    print_log('CONNECTING TO ZABER')
    try:
        zt = zaber_tools.zaber_tools(comPort)
        # device id
        resp = zt.connection.generic_command(1, CommandCode.RETURN_SETTING,  50, timeout=0.0, check_errors=True)
        print_log(' Connected to Zaber on {} | Device ID: {}'.format(comPort, resp.data))

    except Exception as e:
        print_log("ZABER ERROR: {0}".format(e))
        core.quit()

    return zt, resp.data


def zaber_disconnect(zt):
    # DISCONNECT A ZABER CONNECTION
    print_log('DISCONNECT FROM ZABER')
    try:
        zt.device.stop()
        zt.close()
    except Exception as e:
        pass


def zaber_get_limits(zt):
    # GET MINIMUM AND MAXIMUM POSITIONS
    print_log('GET MINIMUM AND MAXIMUM POSITIONS')
    min_pos = 0
    max_pos = 0
    try:
        min_pos = zt.device.settings.get(BinarySettings.MINIMUM_POSITION, Units.NATIVE)
        max_pos = zt.device.settings.get(BinarySettings.MAXIMUM_POSITION, Units.NATIVE)
    except Exception as e:
        print_log("ZABER ERROR: {0}".format(e))
    return [min_pos, max_pos]


def zaber_set_target_speed(zt, target_speed):
    # SET TARGET SPEED
    print_log('SET TARGET SPEED')
    try:
        zt.device.settings.set(BinarySettings.TARGET_SPEED, target_speed, Units.VELOCITY_MILLIMETRES_PER_SECOND)
    except Exception as e:
        print_log("ZABER ERROR: {0}".format(e))


def zaber_set_home(zt, home_pos):
    # SET HOME OFFSET TO MINIMUM POSITION AND HOME
    print_log('SET HOME OFFSET TO MINIMUM POSITION AND HOME')
    try:
        zt.device.settings.set(BinarySettings.HOME_OFFSET, home_pos, Units.LENGTH_MILLIMETRES)
        zaber_move_abs(zt, home_pos, interrupt=False)
    except Exception as e:
        print_log("ZABER ERROR: {0}".format(e))


def zaber_move_abs(zt, position, interrupt=True):
    # MOVE TO ABSOLUTE POSITION
    go = True
    pressed = []

    try:
        resp = zt.connection.generic_command(1, CommandCode.RETURN_CURRENT_POSITION)
        cur_pos = resp.data
    except Exception as e:
        print_log("ZABER ERROR: {0}".format(e))
        core.quit()

    if cur_pos > position:
        print_log('RETRACTING DEVICE')
    else:
        print_log('EXTENDING DEVICE')

    try:
        zt.connection.generic_command_no_response(1, CommandCode.MOVE_ABSOLUTE,  int(position))

        while zt.device.is_busy() and go:
            pressed = event.getKeys(keyList=['escape', 'space'])

            if len(pressed) > 0:
                # filter out space pressed while interrupt is False
                if not (not interrupt and 'space' in pressed):
                    go = False

        if not go:
            print_log('DEVICE MOTION INTERRUPTED BY USER')
            try:
                zt.device.stop()
            except Exception as e:
                print_log("ZABER ERROR: {0}".format(e))

            if 'escape' in pressed:
                zaber_disconnect(zt)
                core.quit()

    except Exception as e:
        print_log("ZABER ERROR: {0}".format(e))
        core.quit()
    return go


def zaber_extend_retract_loop(zt, target):
    # EXTEND AND RETRACT LOOP
    go = True
    idx = 0
    while go:
        core.wait(2)
        idx = (idx + 1) % 2
        go = zaber_move_abs(zt,  int(target[idx]))


def print_log(txt):
    # PRINT
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    print('> {} {}'.format(dt_string, txt))


def draw_hdr_ftr():
    rect_titleBox.draw()

    txt_titleBox.draw()
    txt_copyr.draw()


def draw_dashboard():
    draw_hdr_ftr()
#    rect_titleBox.draw()
#    txt_titleBox.draw()

    rect_infoBox.draw()
    rect_infoHdr.draw()
    txt_infoHdr.draw()
    txt_infoBox.draw()

    rect_contBox.draw()
    txt_contBox.draw()

#    txt_copyr.draw()


def present_text(info='', button='', quit=True, wait=True, col='white', check='', title=''):
    txt_infoBox.text = info
    txt_infoHdr.text = title
    txt_contBox.text = button

    draw_dashboard()

    if check:
        txt_check[check].draw()

    win.update()

    if wait:
        pressed = event.waitKeys(keyList=['space', 'escape'])

        if 'escape' in pressed and quit:
            if not demo:
                zaber_disconnect(zt)
            core.quit()


# ######################################################################
# RUN EXPERIMENT
# ######################################################################

if not demo:
    zt, data = zaber_connect(comPort_Zaber)
    limits = zaber_get_limits(zt)
    max_pos = limits[1]
    limits[1] = limits[1]*0.7
    zaber_set_target_speed(zt, target_speed)
else:
    limits = [0, 10000]
    max_pos = 10000
    data = 12345
# limits = [0, 10079]


# ############### PREPARE ###############
# ####### CONNECT TO ZABER
present_text('Connected to Zaber on {}\nDevice ID: {}'.format(comPort_Zaber, data),
             'Push space to continue',
             title='INFO')

# ############### PHASE 1 ###############
# ####### MOVE SLAVE TO RECTRACTED
present_text('Move slave to retracted position with the knob',
             'Push space to continue',
             title='INSTRUCTION')

# ####### OPEN VALVES
present_text('Open valves',
             'Push space to continue',
             title='INSTRUCTION')

# ####### EXTENDING
present_text('Ready to move master to extended position',
             'Push space to continue', title='INFO')

present_text('Moving master to extended position',
             '',
             title='ACTION',
             wait=wait_val)

if not demo:
    zaber_set_target_speed(zt, target_speed*speed_factor)
    zaber_set_home(zt, limits[0])

present_text('Master in extended position',
             'Push space to continue',
             title='INFO',
             check='')

# ####### EXTEND/RETRACT LOOP
present_text('Ready for extend-retract loop',
             'Push space to continue',
             title='INFO')

present_text('Running extend-retract loop',
             'Push space to continue',
             title='ACTION',
             wait=wait_val)

if not demo:
    zaber_set_target_speed(zt, target_speed)
    zaber_extend_retract_loop(zt, limits)

# ####### MOVE MASTER TO EXTENDED
present_text('Moving master to extended position',
             '',
             title='ACTION',
             wait=wait_val)

if not demo:
    zaber_set_target_speed(zt, target_speed*speed_factor)
    zaber_move_abs(zt, limits[0], interrupt=False)

present_text('Master in extended position',
             'Push space to continue',
             title='INFO',
             check='')

# ####### CLOSE VALVES
present_text('Close valves',
             'Push space to continue',
             title='INSTRUCTION')

# ############### PHASE 2 ###############
# ####### MOVE SLAVE TO EXTENDED
present_text('Move slave to extended position with the knob',
             'Push space to continue',
             title='INSTRUCTION')

# ####### OPEN VALVES
present_text('Open valves',
             'Push space to continue',
             title='INSTRUCTION')

# ####### EXTEND/RESTRACT LOOP
present_text('Ready for extend-retract loop',
             'Push space to continue',
             title='INFO')

present_text('Running extend-retract loop',
             'Push space to continue',
             title='ACTION',
             wait=wait_val)
if not demo:
    zaber_set_target_speed(zt, target_speed)
    zaber_extend_retract_loop(zt, limits)

# ####### MOVE MASTER TO RECTRACTED
present_text('Moving master to retracted position',
             '',
             title='ACTION',
             wait=wait_val)
if not demo:
    zaber_set_target_speed(zt, target_speed*speed_factor)
    zaber_move_abs(zt, limits[1], interrupt=False)

present_text('Master in retracted position',
             'Push space to continue',
             title='INFO',
             check='')

# ###### CLOSE VALVES
present_text('Close valves',
             'Push space to continue',
             title='INSTRUCTION')
if not demo:
    zaber_disconnect(zt)

# ###### CLOSE VALVES
present_text('Air removal procedure finished',
             'Push space to quit',
             title='INFO')
