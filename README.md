# ase-vasp-workflows

Lightweight Python and ASE workflows for VASP calculation analysis and post-processing.

## Features

- Read VASP `OUTCAR` files using ASE
- Extract the final total energy
- Report the chemical formula
- Report the number of atoms
- Perform a basic convergence check

## Requirements

- Python 3
- Atomic Simulation Environment (ASE)

Install ASE using:

```bash
pip install ase
```

## Usage

Run the VASP summary script with a VASP `OUTCAR` file:

```bash
python3 scripts/vasp_summary.py OUTCAR
```

You can also provide the full path to an `OUTCAR` file:

```bash
python3 scripts/vasp_summary.py /path/to/calculation/OUTCAR
```

## Example Output

```text
VASP Calculation Summary
------------------------
File:         OUTCAR
Formula:      Fe2Ni6O16
Atoms:        24
Final energy: -123.456789 eV
Converged:    Yes
```

The values shown above are illustrative example data.

## Repository Structure

```text
ase-vasp-workflows/
├── scripts/
│   └── vasp_summary.py
├── .gitignore
├── LICENSE
└── README.md
```

## Author

Radha Somaiya

## License

This project is released under the MIT License.
