# Cocoha Project

This repository contains the code and instructions for working with the **Cocoha Dataset**, which is used for analyzing EEG responses to auditory stimuli using the **Eelbrain toolkit**: [Eelbrain toolkit](https://elifesciences.org/articles/85012).

## Dataset Information

- **Dataset**: [Zenodo - Cocoha Dataset](https://zenodo.org/records/1199011)
- **Article**: [Describing the Dataset](https://www.sciencedirect.com/science/article/pii/S105381191730318X?via=ihub#s0010)

---

## Folder Structure

After downloading and preparing the dataset, your folder structure should look like this:

```
cocoha/
├── data_preprocessed/   # Preprocessed EEG data (downloaded from Zenodo)
├── stimuli/             # Audio stimuli (downloaded from Zenodo)
├── envelopes/           # Precomputed envelopes (created in load_data/)
├── eeg/                 # Preprocessed EEG data (created in load_data/)
├── TRFs/                # TRF estimates (created in analysis/)
├── figures/             # Figures (created in figures/)
```

---

## Steps to Process the Data

### 1. **Download and Prepare the Dataset**

1. Use `load_data/import-data.ipynb` or download yourself from the following:
   1. Download the **preprocessed data**: [DATA_preproc.zip](https://zenodo.org/record/1199011/files/DATA_preproc.zip)
   2. Download the **stimuli**: [AUDIO.zip](https://zenodo.org/record/1199011/files/AUDIO.zip)
   3. Extract the contents into the `data_preprocessed/` and `stimuli/` folders, respectively.

---

### 2. **Load and Process Predictors**

There are two approaches for creating acoustic predictors:

#### Option A: Load Pre-computed Predictors from MAT Files

Run the notebook `load_data/mat_file_predictors.ipynb` to load envelope predictors that are already included in the downloaded `.mat` files.

```bash
jupyter notebook load_data/mat_file_predictors.ipynb
```

This will:

- Load pre-computed attended (wavA) and ignored (wavB) acoustic envelopes from `data_preprocessed/`
- Compute edge-detected onsets using Eelbrain's `edge_detector` function
- Concatenate trials for each subject and attention condition
- Save results in `predictors/mat_file/` and `predictors/concatenated/mat_file/`
- **Advantage**: Fast, uses envelopes exactly as provided in the dataset
- **Predictors**: Envelope, Envelope Onset

#### Option B: Self-Computed Predictors from Audio Stimuli (Currently does not give good results)

Run the notebook `load_data/self-computed-predictors.ipynb` to compute predictors directly from the audio stimuli.

```bash
jupyter notebook load_data/self-computed-predictors.ipynb
```

This will:

- Create a 128-band gammatone spectrogram for each audio stimulus (simulating cochlear processing)
- Derive multiple predictor types from the spectrogram:
  - Full-band envelope (sum across frequencies)
  - Full-band envelope onset
  - 8-band spectrogram (binned across frequency)
  - 8-band spectrogram onset
- Match predictors to trials based on attend/ignored condition from `expinfo.csv`
- Concatenate predictors across trials for each subject and attention condition
- Save results in `predictors/self_computed/` and `predictors/concatenated/self_computed/`
- **Advantage**: More detailed frequency/onset analysis, consistent predictor computation
- **Predictors**: Envelope, Envelope Onset, Spectrogram (8-band), Spectrogram Onset (8-band)

---

### 3. **Preprocess EEG Data**

Run the notebook `load_data/load_eeg.ipynb` to process the EEG data and save it in a ready-to-use format.

```bash
# Example command to run the notebook
jupyter notebook load_data/load_eeg.ipynb
```

This will:

- Load the `.mat` files from `data_preprocessed/`
- Process the EEG data
- Save the results in the `eeg/` folder

---

### 4. **Estimate TRFs (Multiple Options)**

The analysis folder contains several notebooks for estimating different kinds of TRFs using the precomputed envelopes:

- `analysis/estimate_trfs.ipynb` — standard forward TRF estimation
- `analysis/estimate_decoder_trfs.ipynb` — backward (decoder) TRF estimation
- `analysis/estimate_decoder_trfs_basis.ipynb` — decoder TRFs with basis functions
- `analysis/estimate_padded_trfs.ipynb` — padded TRF estimation

```bash
# Example command to run the notebook
jupyter notebook analysis/estimate_trfs.ipynb
```

This step may take over an hour to complete, depending on your system.

---

### 5. **Visualize Results**

Run the notebooks in `figures/` to generate and save figures.

```bash
# Example command to run the notebook
jupyter notebook figures/aad_topo_map.ipynb
```

This will:

- Load the TRF estimates
- Generate visualizations
- Save the figures in the `figures/` folder

---

## Summary of Outputs

- **Envelopes**: `envelopes/`
- **EEG Data**: `eeg/`
- **TRFs**: `TRFs/`
- **Figures**: `figures/`

---

## Notes

- Ensure all dependencies are installed before running the notebooks.
- The processing steps may take significant time depending on the size of the dataset and your system's performance.
