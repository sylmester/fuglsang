import file_paths
import re
import numpy as np
import eelbrain



# Utility function to get subject list
def get_subjects():
    SUBJECTS = [path.stem.split("_")[0] for path in file_paths.DATA_PREPROC.glob("*.mat")]
    SUBJECTS = sorted(SUBJECTS, key=lambda x: int(re.search(r'S(\d+)', x).group(1)))
    return SUBJECTS

# Utility function to get stimulus paths
def get_stimuli_paths():
    return [stimulus.stem for stimulus in file_paths.STIMULUS_DIR.glob("*.wav")]

# Get subject data file path
def get_subject_data_file(subject: str):
    return file_paths.DATA_PREPROC / f"{subject}_data_preproc.mat"


# Utility function to convert mat_struct to python dict
def matobj_to_dict(matobj):
    """
    Recursively convert mat_struct to Python dict.
    """
    import scipy.io
    
    if isinstance(matobj, scipy.io.matlab.mio5_params.mat_struct):
        d = {}
        for fieldname in matobj._fieldnames:
            value = getattr(matobj, fieldname)
            d[fieldname] = matobj_to_dict(value)
        return d
    elif isinstance(matobj, (np.ndarray, list)):
        return [matobj_to_dict(e) for e in matobj]
    else:
        return matobj


# Function estimating TRFs
def estimate_subjects_trfs(subjects, trf_name, predictor_name):
    for subject in subjects:
        print("-" * 50)
        print(f"Processing subject {subject}...")
        
        # Check if all TRF files already exist
        trf_dir = file_paths.TRF_DIR / f"{subject}"
        trf_path = trf_dir / f"{subject}_{trf_name}.pickle"
        
        
        if trf_path.exists():
            print(f"{trf_name} TRF file for {subject} already exist, skipping.")
            continue
        
        # Load EEG data from pickle file
        eeg_path = file_paths.EEG_DIR / subject / f"{subject}_eeg.pickle"
        eeg = eelbrain.load.unpickle(eeg_path)


        # Load predictor data
        predictor_path = file_paths.ENVELOPES_DIR / subject / f"{subject}_{predictor_name}.pickle"
        predictor = eelbrain.load.unpickle(predictor_path)

        print(f"EEG: {eeg}")
        print(f"Predictor {predictor_name}: {predictor}")

        # Estimate TRFs for attended and unattended conditions using boosting
        print(f"Estimating {trf_name} TRF...")
        trf = eelbrain.boosting(
                eeg,
                predictor,
                -0.100,
                1.000,
                error='l1',
                basis=0.050,
                partitions=5,
                test=1, # use cross-validation
                selective_stopping=True
            )

        # Save TRF
        trf_dir.mkdir(exist_ok=True, parents=True)
        eelbrain.save.pickle(trf, trf_path)
        print(f"Saved {trf_name} TRF to {trf_path}")
