# uro-fMRI

uro-fMRI is the implementation of an fMRI study from the Department of Rehabilitation Sciences at Ghent University.
The experiment uses an Aroflex INFSYS-2 system (https://aroflex.ch/) to control bladder filling and emptying.

uro-fMRI consists of 2 tools and some helper scripts:
- uro_fMRI.py: the actual experiment
- uro_air_removal: tool to assist in the removal of air from the INFSYS-2 device
- zaber_tools: basic wrapper to connect to the Zaber device

# Depencencies
uro-fMRI depends on the following tools:
- PsychopPy3 http://www.psychopy.org
PsychoPy is an open-source package for running experiments in Python.
PsychoPy was initially created and maintained by Jon Peirce.
More information on PsychoPy can be found at http://www.psychopy.org

References to PsychoPy:
Peirce, JW (2007) PsychoPy - Psychophysics software in Python. 
J Neurosci Methods, 162(1-2):8-13

Peirce JW (2009) Generating stimuli for neuroscience using PsychoPy.
Front. Neuroinform. 2:10. doi:10.3389/neuro.11.010.2008

- [Zaber Motion Library for Python](https://www.zaber.com/software/docs/motion-library/binary/)
The Python implementation of the binary protocol for Zaber devices.

- [ScannerTrigger module](https://github.com/GIfMI/ScannerTrigger/)
This module is a wrapper class for all devices which can import a trigger from
eg the MR scanner to PsychoPy.
