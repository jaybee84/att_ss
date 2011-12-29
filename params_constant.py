import numpy as np
from tools import sound_freq_sweep
from psychopy.sound import Sound

p = dict(
    # Display:
    monitor = 'ESI_psychophys',
    full_screen = False,
    screen_number = 0, #1,
    refresh_rate = 60, # Hz
   # General:
    n_trials = 250,
    break_trials = 50,
    fixation_size = 0.25,
    rgb = np.array([1.,1.,1.]),
    cue_reliability = 0.7,
    # Stimuli:
    res = 128,
    temporal_freq = 4, # 0 for no flicker
    sf = 4, # cycles/deg
    ecc = 6, # dva 
    center_size = 3,
    surr_size = 8,
    center_contrast = np.array([0.5]), #np.array([0.2, 0.3, 0.5, 0.7]),
    center_comparison = np.array([-0.3, -0.2, -0.15, -0.1, -0.05, 0, 0.05, 0.1,
                                  0.15, 0.2, 0.3 ]),
    surr_contrast = 1,
    div_color = -1,
    # Timing: 
    cue_dur = 0.5,
    cue_to_stim = 0.3,
    stim_dur = 0.38,
    stim_to_stim = 0.4,
    iti = .2,
    )
