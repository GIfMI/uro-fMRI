from psychopy import visual, gui
import numpy as np

# ######################################################################
# EXPERIMENT INFO
# ######################################################################
expName = "URO"
expInfo = { 'subject ID': 1,
            'maximum volume': 100,
            'syringe volume': 60, 
            }

dlg = gui.DlgFromDict(dictionary=expInfo, title=expName, order = list(expInfo.keys()), sortKeys = False)

if dlg.OK is False:
    core.quit()

def calc_syr(vol, vol_syr):
    nr_syrs = int(np.ceil(vol/vol_syr))
    vol_syrs = np.ones(nr_syrs) * vol_syr
    vol_syrs[-1] = np.mod(vol, vol_syrs)
    return nr_syrs, vol_syrs

vol_max = expInfo['maximum volume']
vol_syr = expInfo['syringe volume']

vol_40 = vol_max * 0.4
vol_65 = vol_max * 0.65 - vol_40

nr_syr_40, syr_40 = calc_syr(vol_40, vol_syr)
nr_syr_65, syr_65 = calc_syr(vol_65, vol_syr)



    
