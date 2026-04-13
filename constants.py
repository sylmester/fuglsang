from pathlib import Path
from enum import Enum


# =============================================================================
# SIGNAL PROCESSING
# =============================================================================

GAMMATONE_SPECTROGRAM_BANDS      = 128
GAMMATONE_FREQUENCY_RANGE_LOW    = 80
GAMMATONE_FREQUENCY_RANGE_HIGH   = 15000

EEG_SAMPLING_RATE                = 64
EEG_BANDPASS_FILTER_LOW          = 0.5
EEG_BANDPASS_FILTER_HIGH         = 20

PADDING_ONSET                    = 0.1
PADDING_OFFSET                   = 1.0

# =============================================================================
# TRF
# =============================================================================

TRF_LAG_START                    = -0.100
TRF_LAG_END                      =  1.000
BASIS_FUNCTION_WIDTH             =  0.050

# =============================================================================
# ENUMS
# =============================================================================

class PREDICTOR_TYPE(Enum):
    ENVELOPE                 = "envelope"
    ENVELOPE_ONSET           = "envelope_onset"
    SPECTROGRAM_8_BAND       = "spectrogram_8_band"
    SPECTROGRAM_ONSET_8_BAND = "spectrogram_onset_8_band"

class ATTENTION_TYPE(Enum):
    ATTENDED = "attended"
    IGNORED  = "ignored"

class MODEL_TYPE(Enum):
    FORWARD  = "forward"
    BACKWARD = "backward"

# =============================================================================
# DOWNLOAD URLs
# =============================================================================

AUDIO_URL        = 'https://zenodo.org/record/1199011/files/AUDIO.zip'
DATA_PREPROC_URL = 'https://zenodo.org/record/1199011/files/DATA_preproc.zip'

# =============================================================================
# DIRECTORIES
# =============================================================================

DATA_ROOT                   = Path("~").expanduser() / 'Data' / 'cocoha4'

DATA_RAW                    = DATA_ROOT / 'data_raw'
DATA_PREPROC                = DATA_ROOT / 'data_preprocessed'
STIMULUS_DIR                = DATA_ROOT / 'stimuli'
ENVELOPES_DIR               = DATA_ROOT / 'envelopes'
EEG_DIR                     = DATA_ROOT / 'eeg'
TRF_DIR                     = DATA_ROOT / 'TRFs'
SELF_COMPUTED_TRF_DIR       = TRF_DIR / 'self_computed'
MAT_FILE_TRF_DIR            = TRF_DIR / 'mat_file'
FIGURES_DIR                 = DATA_ROOT / 'figures'

PREDICTOR_DIR               = DATA_ROOT / 'predictors'
SELF_COMPUTED_DIR           = PREDICTOR_DIR / 'self_computed'
MAT_FILE_DIR                = PREDICTOR_DIR / 'mat_file'
CONCAT_DIR                  = PREDICTOR_DIR / 'concatenated'
SELF_COMPUTED_CONCAT_DIR    = CONCAT_DIR / 'self_computed'
MAT_FILE_CONCAT_DIR         = CONCAT_DIR / 'mat_file'

for _dir in [
    DATA_PREPROC,
    STIMULUS_DIR,
    ENVELOPES_DIR,
    EEG_DIR,
    TRF_DIR,
    FIGURES_DIR,
    SELF_COMPUTED_DIR,
    MAT_FILE_DIR,
    SELF_COMPUTED_CONCAT_DIR,
    MAT_FILE_CONCAT_DIR,
]:
    _dir.mkdir(parents=True, exist_ok=True)