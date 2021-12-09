#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Script to calculate the number and volume of syringes for the fMRI study.
Some stuff is hard-coded, with some effort it can be parameterized.
"""
# Part of the URO library
# Copyright (C) 2021 Pieter Vandemaele
# Distributed under the terms of the GNU General Public License (GPL).

from psychopy import core, clock, visual, event, gui, logging
import numpy as np

# ######################################################################
# HELPER FUNCTIONS
# ######################################################################


def print_log(txt):
    # PRINT
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    print('> {} {}'.format(dt_string, txt))


# ######################################################################
# PREPARE PSYCHOPY
# ######################################################################
# Window
win = visual.Window([1280, 1024], monitor="testMonitor", units="norm")

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
height_syr = 0.25
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

# ## SYRINGE 1
rect_syr1Box_size = np.array([(1 - 3*margin)/2, height_syr])
rect_syr1Hdr_size = np.array([rect_syr1Box_size[0], 0.1])

rect_syr1Box_pos = np.array([rect_syr1Box_size[0]/2+margin, 0.5])
rect_syr1Hdr_pos = np.array([rect_syr1Box_pos[0], rect_syr1Box_pos[1] + rect_syr1Hdr_size[1]/2 + rect_syr1Box_size[1]/2])

txt_syr1Box_pos = rect_syr1Box_pos.copy()
txt_syr1Box_wrap = rect_syr1Box_size[0] - 0.05

txt_syr1Hdr_pos = rect_syr1Hdr_pos.copy()
txt_syr1Hdr_wrap = rect_syr1Hdr_size[0] - 0.05

# ## SYRINGE 2
rect_syr2Box_size = rect_syr1Box_size.copy()
rect_syr2Hdr_size = np.array([rect_syr2Box_size[0], 0.1])

rect_syr2Box_pos = np.array([1-rect_syr2Box_size[0]/2-margin, 0.5])
rect_syr2Hdr_pos = np.array([rect_syr2Box_pos[0], rect_syr2Box_pos[1] + rect_syr2Hdr_size[1]/2 + rect_syr2Box_size[1]/2])

txt_syr2Box_pos = rect_syr2Box_pos.copy()
txt_syr2Box_wrap = rect_syr2Box_size[0] - 0.05

txt_syr2Hdr_pos = rect_syr2Hdr_pos.copy()
txt_syr2Hdr_wrap = rect_syr2Hdr_size[0] - 0.05


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

# ## SYRINGE 1
rect_syr1Box_pos = (rect_syr1Box_pos*2)-1
rect_syr1Box_size = rect_syr1Box_size*2

rect_syr1Hdr_pos = (rect_syr1Hdr_pos*2)-1
rect_syr1Hdr_size = rect_syr1Hdr_size*2

txt_syr1Box_pos = (txt_syr1Box_pos*2)-1
txt_syr1Box_wrap = txt_syr1Box_wrap*2

txt_syr1Hdr_pos = (txt_syr1Hdr_pos*2)-1
txt_syr1Hdr_wrap = txt_syr1Hdr_wrap*2


# ## SYRINGE 2
rect_syr2Box_pos = (rect_syr2Box_pos*2)-1
rect_syr2Box_size = rect_syr2Box_size*2

rect_syr2Hdr_pos = (rect_syr2Hdr_pos*2)-1
rect_syr2Hdr_size = rect_syr2Hdr_size*2

txt_syr2Box_pos = (txt_syr2Box_pos*2)-1
txt_syr2Box_wrap = txt_syr2Box_wrap*2

txt_syr2Hdr_pos = (txt_syr2Hdr_pos*2)-1
txt_syr2Hdr_wrap = txt_syr2Hdr_wrap*2

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
    height=0.15, alignText='center', text="URO-MRI\nSYRINGE CALCULATOR", wrapWidth=txt_titleBox_wrap)

# ## SYRINGE 1
# ### RECTANGLES
rect_syr1Box = visual.Rect(
    win=win,
    size=rect_syr1Box_size,
    pos=rect_syr1Box_pos,
    lineWidth=1.0, colorSpace='rgb255', lineColor=col_paneBox, fillColor=col_paneBox,
    opacity=None, depth=-1.0, interpolate=True, autoDraw=False)

rect_syr1Hdr = visual.Rect(
    win=win,
    size=rect_syr1Hdr_size,
    pos=rect_syr1Hdr_pos,
    lineWidth=1.0, colorSpace='rgb255', lineColor=col_paneHdr, fillColor=col_paneHdr,
    opacity=None, depth=-1.0, interpolate=True, autoDraw=False)

# ### TEXT
txt_syr1Hdr = visual.TextStim(
    win=win,
    pos=txt_syr1Hdr_pos,
    height=0.15, alignText='left', text="Command", wrapWidth=txt_syr1Hdr_wrap)

txt_syr1Box = visual.TextStim(
    win=win,
    pos=txt_syr1Box_pos,
    height=0.10, alignText='left', text="Here comes the command", wrapWidth=txt_syr1Box_wrap)

# ## SYRINGE 2
# ### RECTANGLES
rect_syr2Box = visual.Rect(
    win=win,
    size=rect_syr2Box_size,
    pos=rect_syr2Box_pos,
    lineWidth=1.0, colorSpace='rgb255', lineColor=col_paneBox, fillColor=col_paneBox,
    opacity=None, depth=-1.0, interpolate=True, autoDraw=False)

rect_syr2Hdr = visual.Rect(
    win=win,
    size=rect_syr2Hdr_size,
    pos=rect_syr2Hdr_pos,
    lineWidth=1.0, colorSpace='rgb255', lineColor=col_paneHdr, fillColor=col_paneHdr,
    opacity=None, depth=-1.0, interpolate=True, autoDraw=False)

# ### TEXT
txt_syr2Hdr = visual.TextStim(
    win=win,
    pos=txt_syr2Hdr_pos,
    height=0.15, alignText='left', text="Command", wrapWidth=txt_syr2Hdr_wrap)

txt_syr2Box = visual.TextStim(
    win=win,
    pos=txt_syr2Box_pos,
    height=0.10, alignText='left', text="Here comes the command", wrapWidth=txt_syr2Box_wrap)

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
def draw_hdr_ftr():
    rect_titleBox.draw()

    txt_titleBox.draw()
    txt_copyr.draw()


def draw_dashboard():
    draw_hdr_ftr()

    rect_syr1Box.draw()
    rect_syr1Hdr.draw()
    txt_syr1Hdr.draw()
    txt_syr1Box.draw()

    rect_syr2Box.draw()
    rect_syr2Hdr.draw()
    txt_syr2Hdr.draw()
    txt_syr2Box.draw()

    rect_contBox.draw()
    txt_contBox.draw()


def present_text(info=['', ''], cont='', quit=True, wait=True, col='white', title=['', '']):
    txt_syr1Box.text = info[0]
    txt_syr1Hdr.text = title[0]
    txt_syr2Box.text = info[1]
    txt_syr2Hdr.text = title[1]
    txt_contBox.text = cont

    draw_dashboard()

    win.update()

    if wait:
        pressed = event.waitKeys(keyList=['space', 'escape'])

        if 'escape' in pressed and quit:
            core.quit()


def calc_syr(vol, vol_syr):
    nr_syrs = int(np.ceil(vol/vol_syr))
    vol_syrs = np.ones(nr_syrs) * vol_syr
    vol_syrs[-1] = np.mod(vol, vol_syrs[-1])
    return nr_syrs, vol_syrs

# ######################################################################
# RUN EXPERIMENT
# ######################################################################

present_text(wait=False)

# ######################################################################
# EXPERIMENT INFO
# ######################################################################
expName = "URO"
expInfo = {'subject ID': 1,
           'maximum volume': 750,
           'syringe volume': 60,
           }

dlg = gui.DlgFromDict(dictionary=expInfo, title=expName, order=list(expInfo.keys()), sortKeys=False)

if dlg.OK is False:
    core.quit()

vol_max = int(expInfo['maximum volume'])
vol_syr = int(expInfo['syringe volume'])

vol_40 = vol_max * 0.4
vol_65 = vol_max * 0.65 - vol_40

nr_syr_40, syr_40 = calc_syr(vol_40, vol_syr)
nr_syr_65, syr_65 = calc_syr(vol_65, vol_syr)

syr1_str = ''
for i in range(0, nr_syr_40-1):
    syr1_str = syr1_str + 'syringe {}: {} ml\n'.format(i+1, syr_40[i])

syr2_str = ''
for i in range(0, nr_syr_65-1):
    syr2_str = syr2_str + 'syringe {}: {} ml\n'.format(i+1, syr_65[i])

# ####### EXTEND/RETRACT LOOP
present_text([syr1_str.strip(), syr2_str.strip()],
             'Push space to quit',
             title=['Volume 40%', 'Volume 65%'])
