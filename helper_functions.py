from pathlib import Path
import re
import numpy as np
import eelbrain
import matplotlib.pyplot as plt
from constants import *
import os
import pandas as pd




# Utility function to get subject list --------------------------------------------------
def get_subjects():
    SUBJECTS = [path.stem.split("_")[0] for path in DATA_PREPROC.glob("*.mat")]
    SUBJECTS = sorted(SUBJECTS, key=lambda x: int(re.search(r'S(\d+)', x).group(1)))
    return SUBJECTS

# Utility function to get stimulus paths --------------------------------------------------
def get_stimuli_paths():
    return [stimulus.stem for stimulus in STIMULUS_DIR.glob("*.wav")]

# Get subject data file path --------------------------------------------------
def get_subject_data_file(subject: str):
    return DATA_PREPROC / f"{subject}_data_preproc.mat"




def get_trials(subject):
    csv_path = os.path.join(DATA_RAW, f'{subject}_expinfo.csv')
    
    if not os.path.exists(csv_path):
        print(f"Missing expinfo CSV for {subject}: {csv_path}")
        return {}

    expinfo = pd.read_csv(csv_path)
    trials  = {}
    trial_idx = 0

    for _, row in expinfo.iterrows():
        if row['n_speakers'] == 1:
            continue

        if row['attend_mf'] == 1:
            attended_wavfile = Path(row['wavfile_male']).stem.strip("'\"")
            ignored_wavfile  = Path(row['wavfile_female']).stem.strip("'\"")
        else:
            attended_wavfile = Path(row['wavfile_female']).stem.strip("'\"")
            ignored_wavfile  = Path(row['wavfile_male']).stem.strip("'\"")

        trials[trial_idx] = {
            'attended': attended_wavfile,
            'ignored':  ignored_wavfile
        }
        trial_idx += 1

    print(f"{subject}: loaded {len(trials)} trials")
    return trials


# Utility function to process predictors --------------------------------------------------
def process_predictor(predictor, padded = True):
    # DATA PROCESSING OF ENVELOPES
    LOW_FREQUENCY = 0.5
    HIGH_FREQUENCY = 20

    # Resample spectrograms to 64 hz, offset and filter
    x = predictor
    x = x.bin(1/64, dim='time', label='start')
    if padded:
        x = eelbrain.pad(x, tstart=-PADDING_ONSET, tstop=x.time.tstop + PADDING_OFFSET)
    x = eelbrain.filter_data(x, LOW_FREQUENCY, HIGH_FREQUENCY)
    
    return x


def get_predictor_name(predictors, padded=False) -> str:
    """
    Format:
        <predictor1+predictor2+...>[ _padded ]

    Example:
        envelope+envelope_onset_padded
    """
    if isinstance(predictors, PREDICTOR_TYPE):
        predictors = [predictors]

    predictors = sorted(predictors, key=lambda p: p.value)
    name = "+".join(p.value for p in predictors)

    if padded:
        name += "_padded"

    return name


def get_attentional_predictor_name(predictors, attention: ATTENTION_TYPE, padded=False) -> str:
    """
    Format:
        <attention_type>_<predictor_combination>

    Example:
        attended_envelope+envelope_onset_padded
    """
    return f"{attention.value}_{get_predictor_name(predictors, padded)}"


def get_trf_model_name(predictors, attention: ATTENTION_TYPE, model: MODEL_TYPE, padded=False) -> str:
    """
    Format:
        <model_type>_<predictor_name>

    Example:
        backward_attended_envelope+envelope_onset_padded
    """
    return f"{model.value}_{get_attentional_predictor_name(predictors, attention, padded)}"



def set_plot_style():
    FONT      = 'Arial'
    FONT_SIZE = 8
    RC = {
        'figure.dpi':          100,
        'savefig.dpi':         300,
        'savefig.transparent': True,
        'font.family':         'sans-serif',
        'font.sans-serif':     FONT,
        'font.size':           FONT_SIZE,
        'figure.labelsize':    FONT_SIZE,
        'figure.titlesize':    FONT_SIZE,
        'axes.labelsize':      FONT_SIZE,
        'axes.titlesize':      FONT_SIZE,
        'xtick.labelsize':     FONT_SIZE,
        'ytick.labelsize':     FONT_SIZE,
        'legend.fontsize':     FONT_SIZE,
    }
    plt.rcParams.update(RC)


def load_trfs(checks, trf_dir=MAT_FILE_TRF_DIR):
    """
    Load TRFs for all subjects and checks.

    Returns:
        trf_data:   dict keyed by model_name -> list of TRFs (one per subject)
        n_subjects: number of subjects successfully loaded
    """
    subjects  = get_subjects()
    trf_data  = {get_trf_model_name(p, a, m, pad): [] for p, a, m, pad in checks}
    skipped   = []
    loaded    = []

    for subject in subjects:
        missing = [
            get_trf_model_name(p, a, m, pad)
            for p, a, m, pad in checks
            if not (trf_dir / subject / f"{subject}_{get_trf_model_name(p, a, m, pad)}_trf.pickle").exists()
        ]

        if missing:
            print(f"  ✗ {subject}: skipping — missing {len(missing)} TRF(s):")
            for name in missing:
                print(f"      - {name}")
            skipped.append(subject)
            continue

        for p, a, m, pad in checks:
            name = get_trf_model_name(p, a, m, pad)
            path = trf_dir / subject / f"{subject}_{name}_trf.pickle"
            trf_data[name].append(eelbrain.load.unpickle(path))

        loaded.append(subject)
        print(f"  ✓ {subject}")

    print(f"\nLoaded: {len(loaded)} subjects | Skipped: {len(skipped)} subjects")
    if skipped:
        print(f"  Skipped: {skipped}")

    n_subjects = len(loaded)
    return trf_data, n_subjects

# Utility function to get significance marker based on p-value --------------------------------------------------
def sig_marker(p):
        if p < 0.001:  return '***'
        elif p < 0.01: return '**'
        elif p < 0.05: return '*'
        else:          return 'n.s.'


# Utility function to add significance lines to plots --------------------------------------------------
def add_sig_line(ax, x1, x2, y, text, color='k'):
    ax.plot([x1, x1, x2, x2], [y, y + 0.0005, y + 0.0005, y], color=color, linewidth=1)
    ax.text((x1 + x2) / 2, y + 0.0005, text, ha='center', va='bottom', fontsize=10)