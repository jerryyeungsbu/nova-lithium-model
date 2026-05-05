# Nova Lithium Model

A Python-based model for simulating the time evolution of neutral lithium (Li I) column densities in classical novae ejecta
This model simulates how Li I absorption in nova ejecta evolves over time, driven by two competing processes
- Geometric dilution as the shell expands (`∝ 1/R²`)
- Recombination as the ejecta cools, converting ionized Li II to neutral Li I

The model incorporates
- 7Be → 7Li radioactive decay (half-life: 53.22 days)
- Photospheric visibility effects (line-of-sight column)
- Optional Saha equation for ionization equilibrium

## Installation

```bash
git clone https://github.com/jerryeungsbu/nova-lithium-model.git
cd nova-lithium-model
pip install numpy matplotlib scipy
```

## Files
| `nova_model.py` | General model - predicts Li I column density over time |
| `saha_model.py` | Saha ionization model - predicts neutral Li fraction |
| `requirements.txt` | Python dependencies |
| `example.py` | Run both models with one command |
