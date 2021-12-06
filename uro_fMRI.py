from psychopy import core, clock, visual, event, gui, logging
import time
from datetime import datetime
from math import floor, ceil
import numpy as np
import csv
import os
import pathlib as pl
import scannertrigger as s
import zaber_tools
from zaber_motion.binary import CommandCode, BinarySettings
from zaber_motion import Units, FirmwareVersion, Measurement, Tools

# ######################################################################
# HELPER FUNCTIONS
# ######################################################################


def print_log(txt):
    # PRINT
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    print('> {} {}'.format(dt_string, txt))

print_log('Started experiment')

# ######################################################################
# DEFINE THE PARADIGM
# ######################################################################
# Parameters
dur_baseline = 1
dur_runout = 1
dur_pause1 = 1
dur_pause2 = 1
dur_infuse = 12
dur_withdraw = 12
rate_infuse = 100
rate_withdraw = 100

# dur_baseline = 3
# dur_runout = 2
# dur_pause1 = 3
# dur_pause2 = 3
# dur_infuse = 3
# dur_withdraw = 3
# rate_infuse = 100
# rate_withdraw = 100

dur_baseline = 2
dur_runout = 2
dur_pause1 = 2
dur_pause2 = 2
dur_infuse = 5
dur_withdraw = 5
rate_infuse = 500
rate_withdraw = 500

paradigm = [
    ['baseline', 'rest', dur_baseline, 'Baseline'],
    ['event 1',  'pause', dur_pause1, 'Event 1\nPause 1'],
    ['event 1',  'infuse', dur_infuse, 'Event 1\nInfuse', rate_infuse],
    ['event 1',  'pause', dur_pause2, 'Event 1\nPause 2'],
    ['event 1',  'withdraw', dur_withdraw, 'Event 1\nWithdraw', rate_withdraw],
    ['event 2',  'pause', dur_pause1, 'Event 2\nPause 1'],
    ['event 2',  'infuse', dur_infuse, 'Event 2\nInfuse', rate_infuse],
    ['event 2',  'pause', dur_pause2, 'Event 2\nPause 2'],
    ['event 2',  'withdraw', dur_withdraw, 'Event 2\nWithdraw', rate_withdraw],
    ['event 3',  'pause', dur_pause1, 'Event 3\nPause 1'],
    ['event 3',  'infuse', dur_infuse, 'Event 3\nInfuse', rate_infuse],
    ['event 3',  'pause', dur_pause2, 'Event 3\nPause 2'],
    ['event 3',  'withdraw', dur_withdraw, 'Event 3\nWithdraw', rate_withdraw],
    ['event 4',  'pause', dur_pause1, 'Event 4\nPause 1'],
    ['event 4',  'infuse', dur_infuse, 'Event 4\nInfuse', rate_infuse],
    ['event 4',  'pause', dur_pause2, 'Event 4\nPause 2'],
    ['event 4',  'withdraw', dur_withdraw, 'Event 4\nWithdraw', rate_withdraw],
    ['runout', 'rest', dur_runout, 'Run out'],
    ]

col_command = {
    'rest': (1.0, 0.776470588, 0.109803922),
    'pause': (0.2, 0.654901961, 0.792156863),
    'infuse': (0.850980392, 0.37254902, 0.168627451),
    'withdraw': (0.48627451, 0.701960784, 0.243137255),
    }
# paradigm_file = gui.fileOpenDlg(tryFilePath='', tryFileName='', prompt='Select file to open', allowed=None)
#
# if not paradigm_file:
#     core.quit()
# else:
#     paradigm_file = paradigm_file[0]
#
# paradigm = []
#
# with open(paradigm_file) as csvfile:
#     paradigmreader = csv.reader(csvfile, delimiter=',')
#     paradigm = []
#     for row in paradigmreader:
#         print(row)
#         row = [x.strip(' ') for x in row]
#         print(row)
#         row = [x.replace('\\n', '\n') for x in row]
#         print(row)
#         row[2] = int(row[2])
#         print(row)
#         if len(row)>4:
#             row[4] = int(row[4])
#         print(row)
#         print('---------------------')
#         paradigm.append(row)
#
# print(paradigm)

# ######################################################################
# EXPERIMENT INFO
# ######################################################################
expName = "URO"
expInfo = {
            'subject ID': 1,
            'session ID': [1, 2],
            'triggering': ['keyboard',
                           'serial',
                           'parallel',
                           'cedrus',
                           'launchscan',
                           'dummy'],
            'skip scans': 0,
            'COM Port (MRI)': "COM1",
            'COM Port (Zaber)': "COM9",
            'Zaber': ['off', 'on']
            # 'Paradigm from file': ['yes', 'no'],
           }

dlg = gui.DlgFromDict(dictionary=expInfo, title=expName, order=list(expInfo.keys()), sortKeys=False)

if dlg.OK is False:
    core.quit()

# ######################################################################
# PREPARE PSYCHOPY
# ######################################################################
# Global experiment clock
global_clock = core.Clock()

# Logging
paradigm_loglevel = logging.FATAL+1
logging.addLevel(paradigm_loglevel, 'PARADIGM')
logging.setDefaultClock(global_clock)
logging.console.setLevel(logging.CRITICAL)

sub = expInfo['subject ID']
ses = expInfo['session ID']

if sub is str:
    sub.strip()

if ses is str:
    ses.strip()

curdir = pl.Path('.')
logdir = pl.Path('.', 'log')
logtime = datetime.now().strftime('%Y%m%d_%H%M%S')
logfname = 'sub-{}_ses-{}_{}.txt'.format(sub, ses, logtime)
logfname1 = 'sub-{}_ses-{}_{}_all.txt'.format(sub, ses, logtime)

if not logdir.exists():
    try:
        logdir.mkdir()
    except Exception as e:
        print_log("LOGGING ERROR: {0}".format(e))
        core.quit()

try:
    logData = logging.LogFile(str(pl.Path(logdir, logfname1).resolve()),
                              filemode='w',
                              level=logging.INFO)
    logParadigm = logging.LogFile(str(pl.Path(logdir, logfname).resolve()),
                                  filemode='w',
                                  level=paradigm_loglevel)

except Exception as e:
    print_log("LOGGING ERROR: {0}".format(e))
    core.quit()

print_log('Logging to file {}'.format(pl.Path(logdir, logfname).absolute()))

# Window
win = visual.Window([1280, 1024], monitor="testMonitor", units="norm")
win.update()
event.waitKeys()

# ######################################################################
# DASHBOARD
# ######################################################################
print_log('Setting up dashboard')
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
height_command = 0.22
height_flow = 0.0
height_cntr = 0.0
height_copyr = 0.05
height_hdr = 0.1

# # PARAMETERS INITIALISATION
# ## TITLE
rect_titleBox_size = np.array([1, height_title])
rect_titleBox_pos = np.array([rect_titleBox_size[0]/2, 1-rect_titleBox_size[1]/2])

txt_titleBox_pos = rect_titleBox_pos.copy()
txt_titleBox_wrap = rect_titleBox_size[0] - 0.05

# ## COMMAND
rect_cmdBox_size = np.array([1 - 2*margin, height_command])
rect_cmdHdr_size = np.array([rect_cmdBox_size[0], height_hdr])

rect_cmdBox_pos = np.array([rect_cmdBox_size[0]/2+margin, 1-margin - rect_cmdHdr_size[1] - rect_cmdBox_size[1]/2 - rect_titleBox_size[1]])
rect_cmdHdr_pos = np.array([rect_cmdBox_pos[0], 1 - margin - rect_cmdHdr_size[1]/2 - rect_titleBox_size[1]])

txt_cmdBox_pos = rect_cmdBox_pos.copy()
txt_cmdBox_wrap = rect_cmdBox_size[0] - 0.05

txt_cmdHdr_pos = rect_cmdHdr_pos.copy()
txt_cmdHdr_wrap = rect_cmdHdr_size[0] - 0.05

# ## FLOW
a = 1-(margin + height_copyr + height_hdr+margin + rect_cmdBox_size[1] + height_hdr + margin + height_title)

rect_flowBox_size = np.array([0.5, a])
rect_flowHdr_size = np.array([rect_flowBox_size[0], height_hdr])

rect_flowBox_pos = np.array([rect_flowBox_size[0]/2+margin, rect_flowBox_size[1]/2+margin + height_copyr])
rect_flowHdr_pos = np.array([rect_flowBox_pos[0], rect_flowBox_pos[1] + rect_flowBox_size[1]/2 + rect_flowHdr_size[1]/2])

txt_flowBox_pos = rect_flowBox_pos.copy()
txt_flowBox_wrap = rect_flowBox_size[0] - 0.05

txt_flowHdr_pos = rect_flowHdr_pos.copy()
txt_flowHdr_wrap = rect_flowBox_size[0] - 0.05

# ## COUNTER
rect_cntrBox_size = np.array([1 - rect_flowBox_size[0] - 3*margin, rect_flowBox_size[1]])
rect_cntrHdr_size = np.array([rect_cntrBox_size[0], height_hdr])

rect_cntrBox_pos = np.array([1 - rect_cntrBox_size[0]/2 - margin, rect_cntrBox_size[1]/2+margin + height_copyr])
rect_cntrHdr_pos = np.array([rect_cntrBox_pos[0], rect_cntrBox_pos[1] + rect_cntrBox_size[1]/2 + rect_cntrHdr_size[1]/2])

txt_cntrBox_pos = rect_cntrBox_pos.copy()
txt_cntrBox_wrap = rect_cntrBox_size[0] - 0.05

txt_cntrHdr_pos = rect_cntrHdr_pos.copy()
txt_cntrHdr_wrap = rect_cntrBox_size[0] - 0.05

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

# ## FLOW
rect_flowBox_pos = (rect_flowBox_pos*2)-1
rect_flowBox_size = rect_flowBox_size*2

rect_flowHdr_pos = (rect_flowHdr_pos*2)-1
rect_flowHdr_size = rect_flowHdr_size*2

txt_flowBox_pos = (txt_flowBox_pos*2)-1
txt_flowBox_wrap = txt_flowBox_wrap*2

txt_flowHdr_pos = (txt_flowHdr_pos*2)-1
txt_flowHdr_wrap = txt_flowHdr_wrap*2

# ### COMMAND
rect_cmdBox_pos = (rect_cmdBox_pos*2)-1
rect_cmdBox_size = rect_cmdBox_size*2

rect_cmdHdr_pos = (rect_cmdHdr_pos*2)-1
rect_cmdHdr_size = rect_cmdHdr_size*2

txt_cmdBox_pos = (txt_cmdBox_pos*2)-1
txt_cmdBox_wrap = txt_cmdBox_wrap*2

txt_cmdHdr_pos = (txt_cmdHdr_pos*2)-1
txt_cmdHdr_wrap = txt_cmdHdr_wrap*2

# ## COUNTER
rect_cntrBox_pos = (rect_cntrBox_pos*2)-1
rect_cntrBox_size = rect_cntrBox_size*2

rect_cntrHdr_pos = (rect_cntrHdr_pos*2)-1
rect_cntrHdr_size = rect_cntrHdr_size*2

txt_cntrBox_pos = (txt_cntrBox_pos*2)-1
txt_cntrBox_wrap = txt_cntrBox_wrap*2

txt_cntrHdr_pos = (txt_cntrHdr_pos*2)-1
txt_cntrHdr_wrap = txt_cntrHdr_wrap*2

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
    height=0.15, alignText='center', text="URO-MRI\nfMRI Tool", wrapWidth=txt_titleBox_wrap)

# ## FLOW
# ### RECTANGLES
rect_flowBox = visual.Rect(
    win=win,
    size=rect_flowBox_size,
    pos=rect_flowBox_pos,
    lineWidth=1.0, colorSpace='rgb255', lineColor=col_paneBox, fillColor=col_paneBox,
    opacity=None, depth=-1.0, interpolate=True, autoDraw=False)

rect_flowHdr = visual.Rect(
    win=win,
    size=rect_flowHdr_size,
    pos=rect_flowHdr_pos,
    lineWidth=1.0, colorSpace='rgb255', lineColor=col_paneHdr, fillColor=col_paneHdr,
    opacity=None, depth=-1.0, interpolate=True, autoDraw=False)

# ### TEXT
txt_flowHdr = visual.TextStim(
    win=win,
    pos=txt_flowHdr_pos,
    height=0.15, alignText='left', text="Flow info", wrapWidth=txt_flowHdr_wrap)

txt_flowBox = visual.TextStim(
    win=win,
    pos=txt_flowBox_pos,
    height=0.12, alignText='left', text="Flow: xxxxx\n\nRate: yyyyy", wrapWidth=txt_flowBox_wrap)

# ## COMMAND
# ### RECTANGLES
rect_cmdBox = visual.Rect(
    win=win,
    size=rect_cmdBox_size,
    pos=rect_cmdBox_pos,
    lineWidth=1.0, colorSpace='rgb255', lineColor=col_paneBox, fillColor=col_paneBox,
    opacity=None, depth=-1.0, interpolate=True, autoDraw=False)

rect_cmdHdr = visual.Rect(
    win=win,
    size=rect_cmdHdr_size,
    pos=rect_cmdHdr_pos,
    lineWidth=1.0, colorSpace='rgb255', lineColor=col_paneHdr, fillColor=col_paneHdr,
    opacity=None, depth=-1.0, interpolate=True, autoDraw=False)

# ### TEXT
txt_cmdHdr = visual.TextStim(
    win=win,
    pos=txt_cmdHdr_pos,
    height=0.15, alignText='left', text="Command", wrapWidth=txt_cmdHdr_wrap)

txt_cmdBox = visual.TextStim(
    win=win,
    pos=txt_cmdBox_pos,
    height=0.15, alignText='left', text="Here comes the command", wrapWidth=txt_cmdBox_wrap)

# ## COUNTER
# ### RECTANGLES
rect_cntrBox = visual.Rect(
    win=win,
    size=rect_cntrBox_size,
    pos=rect_cntrBox_pos,
    lineWidth=1.0, colorSpace='rgb255', lineColor=col_paneBox, fillColor=col_paneBox,
    opacity=None, depth=-1.0, interpolate=True, autoDraw=False)

rect_cntrHdr = visual.Rect(
    win=win,
    size=rect_cntrHdr_size,
    pos=rect_cntrHdr_pos,
    lineWidth=1.0, colorSpace='rgb255', lineColor=col_paneHdr, fillColor=col_paneHdr,
    opacity=None, depth=-1.0, interpolate=True, autoDraw=False)

# ### TEXT
txt_cntrHdr = visual.TextStim(
    win=win,
    pos=txt_cntrHdr_pos,
    height=0.15, alignText='left', text="Timer", wrapWidth=txt_cntrHdr_wrap)

txt_cntrBox = visual.TextStim(
    win=win,
    pos=txt_cntrBox_pos,
    height=0.4, alignText='center', text="10", wrapWidth=txt_cntrBox_wrap)

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
txt_endofsession = visual.TextStim(
    win=win,
    name='text',
    text='Session finished',
    font='Arial',
    pos=(0, 0),
    height=0.1,
    wrapWidth=None,
    ori=0,
    color='white',
    colorSpace='rgb',
    opacity=1,
    depth=0.0
    )

# ######################################################################
# OTHER INITIALIZATION
# ######################################################################

# ######################################################################
# FUNCTIONS
# ######################################################################


def process_paradigm(paradigm):
    #    0: event
    #    1: command
    #    2: duration
    #    3: info
    #    4: rate

    for entry in paradigm:
        event = entry[0]
        command = entry[1]
        duration = entry[2]
        info = entry[3]

        if len(entry) > 4:
            rate = entry[4]

            if zaber_on:
                distance_mustep = zt.dist_mm_to_mustep(duration*rate/60)
                velocity_mustep = int(ceil(zt.vel_mm_per_s_to_vel(rate/60)))
                distance_mm = duration*rate/60
            else:
                distance_mustep = 0
                velocity_mustep = 0
                distance_mm = duration*rate/60

            if command == 'infuse':
                distance_mustep = abs(distance_mustep)
                distance_mm = abs(distance_mm)
            elif command == 'withdraw':
                distance_mustep = -abs(distance_mustep)
                distance_mm = -abs(distance_mm)

            entry.append([distance_mm, distance_mustep, velocity_mustep])
    return paradigm


def present_condition(win, start_time, entry, countdown):
    name = entry[0]
    command = entry[1]
    duration = entry[2]
    info = entry[3]
    txt_cmdBox.text = info

    try:
        txt_cmdBox.color = col_command[command]
    except:
        txt_cmdBox.color = (0, 0, 0)

    end_time = start_time + duration

    logstr = '{}, {}, {}, {:.3f}, {:.3f}'.format(name, command, info.replace("\n", " "), start_time, global_clock.getTime())
    logging.data(logstr)
    logging.log(logstr, paradigm_loglevel)

    # start movement
    if (command == 'infuse' or command == 'withdraw'):
        rate = entry[4]
        distance_mm = entry[5][0]
        distance_mustep = entry[5][1]
        velocity_mustep = entry[5][2]

        if zaber_on:
            try:
                reply = zt.connection.generic_command(1, CommandCode.SET_TARGET_SPEED, velocity_mustep,  timeout=0)
                zt.connection.generic_command_no_response(1, CommandCode.MOVE_RELATIVE,  distance_mustep)
            except Exception as e:
                logging.error('Zaber command failed')
                logging.flush()
                print_log("ZABER ERROR: {0}".format(e))
                core.quit()
    else:
        distance_mm = 0
        rate = 0

    logging.flush()
    txt_flowBox.text = 'Volume: {:.1f} ml\n\nRate: {} ml/s'.format(distance_mm, rate)
    print_log('---> Presenting event: {} | command: {} | volume: {} ml | velocity {} ml/s'.format(name, command, distance_mm, rate))

    go = True
    if countdown:
        while global_clock.getTime() < end_time and go:
            txt_cntrBox.text = str(ceil(end_time - global_clock.getTime()))

#            if (command == 'infuse' or command == 'withdraw'):
#                txt_flowBox.text = 'Volume: {}\n\nRate: {}'.format(distance_mm, rate)
#                txt_flowBox.draw()
            draw_dashboard()
            win.update()

            pressed = event.getKeys(keyList=["escape"])
            if len(pressed) > 0:
                go = False
    else:
        draw_dashboard()
        win.update()

    # wait for device if still busy
    if zaber_on:
        while zt.device.is_busy() and go:
            pressed = event.getKeys(keyList=["escape"])
            if len(pressed) > 0:
                go = False
            pass

    if not go:
        try:
            zt.device.stop()
        except Exception as e:
            logging.error('Zaber command failed')
            logging.flush()
            print_log("ZABER ERROR: {0}".format(e))
            core.quit()

    return go


def draw_hdr_ftr():
    rect_titleBox.draw()

    txt_titleBox.draw()
    txt_copyr.draw()


def draw_dashboard():
    draw_hdr_ftr()
    rect_flowBox.draw()
    rect_flowHdr.draw()
    rect_cmdBox.draw()
    rect_cmdHdr.draw()
    rect_cntrBox.draw()
    rect_cntrHdr.draw()

    txt_flowHdr.draw()
    txt_flowBox.draw()
    txt_cmdHdr.draw()
    txt_cmdBox.draw()
    txt_cntrHdr.draw()
    txt_cntrBox.draw()

# ######################################################################
# SCANNER TRIGGER SETUP
# ######################################################################
print_log('Setting up scanner trigger')
logging.info('Open ScanTrigger connection')

# Wait for scanner text
txt_scannertrigger = visual.TextStim(
    win=win,
    name='text',
    text='Wait for trigger...',
    font='Arial',
    pos=(0, 0),
    height=0.1,
    wrapWidth=None,
    ori=0,
    color='white',
    colorSpace='rgb',
    opacity=1,
    depth=0.0
    )

# Setup scanner trigger configuration
portType = expInfo['triggering']
dummyScans = int(expInfo['skip scans'])
comPort_MRI = expInfo['COM Port (MRI)']
if portType == "keyboard":
    # Keyboard specific settings
    MR_settings = {
        'keyList': 't',
        'maxWait': 9999999,
        }
elif portType == "dummy":
    # Dummy specific settings
    MR_settings = {
        'tr': 1,
        }
elif portType == "serial":
    # Serial port specific settings
    MR_settings = {
        'port': comPort_MRI,
        'baudrate': 9600,
        'sync': '5'
        }
elif portType == "parallel":
    # Parallelport specific settings
    MR_settings = {
        'address': '0x0378',
        'pin': 10,
        'edge': s.RISING
        }
elif portType == "cedrus":
    # Cedrus specific settings
    MR_settings = {
        'devicenr': 0,
        'sync': 4,
        }
elif portType == "launchscan":
    # launchScan specific settings
    MR_settings = {
        'wait_msg': 'Waiting for scanner',
        'esc_key': 'escape',
        'log': True,
        'wait_timeout': 100,
        'settings': {
            'TR': 1,
            'volumes': 100,
            'sync': 't',
            'skip': dummyScans,
            'sound': False,
            }
        }
else:
    raise ValueError("The selected Port type does not exist!")

# OPEN A SCANNERTRIGGER CONNECTION
scantrig = []
try:
    scantrig = s.ScannerTrigger.create(
                win,
                global_clock,
                portType,
                portConfig=MR_settings,
                timeout=99999,
                logLevel=logging.DATA,
                esc_key='escape')
    scantrig.open()
except Exception as e:
    logging.error('ScannerTrigger connection could not be established')
    logging.flush()
    draw_hdr_ftr()
    txt_scannertrigger.text = 'Could not connect to the scanner trigger'
    txt_scannertrigger.draw()
    win.update()
    print_log("SCANNERTRIGGER ERROR: {0}".format(e))
    event.waitKeys()
    core.quit()

logging.info('ScannerTrigger connection established')
logging.flush()
print_log('\tScannerTrigger connection established')

# ######################################################################
# ZABER SETUP
# ######################################################################
print_log('Setting up Zaber')
logging.info('Open Zaber connection')

# Zaber connection feedback
zaber_on = expInfo['Zaber'] == 'on'

txt_zaber = visual.TextStim(
    win=win,
    name='text',
    text='Wait for trigger...',
    font='Arial',
    pos=(0, 0),
    height=0.1,
    wrapWidth=None,
    ori=0,
    color='white',
    colorSpace='rgb',
    opacity=1,
    depth=0.0
    )

comPort_Zaber = expInfo['COM Port (Zaber)']

# OPEN A ZABER CONNECTION
try:
    if zaber_on:
        zt = zaber_tools.zaber_tools(comPort_Zaber)
        # device id
        resp = zt.connection.generic_command(1, CommandCode.RETURN_SETTING,  50, timeout=0.0, check_errors=True)
        txt_zaber.text = 'Connected to Zaber on {}\Device ID: {}'.format(comPort_Zaber, resp.data)
        print_log('\tConnected to Zaber on {}\Device ID: {}'.format(comPort_Zaber, resp.data))
    else:
        txt_zaber.text = 'Running in emulation mode\nZaber connection bypassed'
        print_log('\tRunning in emulation mode')

except Exception as e:
    logging.error('Zaber connection could not be established')
    logging.flush()
    draw_hdr_ftr()
    txt_zaber.text = 'Could not connect to Zaber on {}'.format(comPort_Zaber)
    txt_zaber.draw()
    win.update()
    print_log("ZABER ERROR: {0}".format(e))
    event.waitKeys()
    core.quit()

logging.info('Zaber connection established')
logging.flush()
print_log('\tZaber connection established')

draw_hdr_ftr()
txt_zaber.draw()
win.update()
event.waitKeys()

# ######################################################################
# RUN EXPERIMENT
# ######################################################################
print_log('Processing paradigm')
paradigm = process_paradigm(paradigm)

print_log('Starting paradigm')
draw_hdr_ftr()
txt_scannertrigger.draw()
win.flip()

# SCANNER SYNCHRONIZATION
try:
    logging.info('Waiting for scanner trigger')
    # Comment this out of you would like to generate emulated keyboard presses.
    # syncPulse = SyncGenerator(TR=1, volumes=100, sync='t', skip=0)
    # syncPulse.start()  # start emitting sync pulses
    # core.runningThreads.append(syncPulse)
    # event.clearEvents()
    print_log("Waiting for the scanner trigger")
    triggered = scantrig.waitForTrigger(skip=dummyScans)
    logging.log('trigger, trigger , MRI Trigger, {:.3f}'.format(scantrig.firstTriggerTime), paradigm_loglevel)
    logging.flush()
except Exception as e:
    logging.error('Wait for scanner trigger failed')
    # In case of errors
    logging.flush()
    print_log("SCANNERTRIGGER ERROR: {0}".format(e))
    core.quit()

# MAIN LOOP
################################################################################
time_offset = global_clock.getTime()
tt = time_offset
countdown = True

for entry in paradigm:
    # Prepare Zaber
    duration = entry[2]
    start_time = time_offset
    time_offset += entry[2]
#   color = col_command[entry[1]]
    command = entry[1]
    info = entry[3]

#    present_condition(win, start_time, *entry[1:4], countdown)
    go = present_condition(win, start_time, entry, countdown)

    if not go:
        logging.info('Experiment aborted manually')
        print_log('Experiment aborted manually')
        break

try:
    if zaber_on:
        zt.connection.close()

except Exception as e:
    logging.error('Zaber command failed')
    logging.flush()
    print_log("ZABER ERROR: {0}".format(e))
    core.quit()

logging.info('Zaber connection closed')
print_log('Zaber connection closed')

try:
    scantrig.close()
except:
    pass
logging.info('ScannerTrigger connection closed')
print_log('ScannerTrigger connection closed')

draw_hdr_ftr()
txt_endofsession.draw()
win.update()
event.clearEvents()
event.waitKeys()
print_log('Experiment finished')
logging.flush()
