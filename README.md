# ase-vasp-workflows

Lightweight Python and Atomic Simulation Environment (ASE) workflows for VASP and Quantum ESPRESSO calculation analysis and post-processing.

The repository contains small command-line utilities developed for common tasks in computational materials and catalysis workflows, including calculation summaries, convergence checks, batch analysis, structure conversion, and magnetic-moment extraction.

## Features

- Read VASP `OUTCAR` files using ASE
- Extract final VASP total energies
- Report chemical formula and number of atoms
- Check electronic and ionic convergence
- Scan multiple VASP calculation directories automatically
- Export batch calculation summaries to CSV
- Convert VASP structures to CIF, XYZ, and other ASE-supported formats
- Convert Quantum ESPRESSO input structures (`scf.in`) to CIF and other formats
- Extract final `E0` and total magnetic moment from VASP `OSZICAR`
- Extract atom-resolved magnetic moments for selected chemical species from `OUTCAR`

## Repository Structure

```text
ase-vasp-workflows/
├── scripts/
│   ├── vasp_summary.py
│   ├── batch_vasp_summary.py
│   ├── convert_structure.py
│   └── magnetic_summary.py
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## Requirements

- Python 3
- Atomic Simulation Environment (ASE)

Install the required Python package with:

```bash
pip install -r requirements.txt
```

or install ASE directly:

```bash
pip install ase
```

## Usage

### 1. VASP Calculation Summary

Extract basic information from a VASP `OUTCAR`:

```bash
python3 scripts/vasp_summary.py OUTCAR
```

Example output:

```text
VASP Calculation Summary
------------------------
File:                   OUTCAR
Formula:                Fe2Ni6O16
Atoms:                  24
Final energy:           -123.456789 eV
Electronic convergence: Yes
Ionic convergence:      Yes
```

The numerical values above are illustrative example data.

---

### 2. Batch VASP Summary

Scan subdirectories for VASP `OUTCAR` files:

```bash
python3 scripts/batch_vasp_summary.py
```

For a directory structure such as:

```text
calculations/
├── state_A/
│   └── OUTCAR
├── state_B/
│   └── OUTCAR
└── state_C/
    └── OUTCAR
```

the script prints a compact summary table containing:

- calculation directory
- chemical formula
- number of atoms
- final energy
- electronic convergence
- ionic convergence

The results are also written automatically to:

```text
vasp_summary.csv
```

This allows the calculation data to be used directly in spreadsheets or subsequent Python analysis.

---

### 3. Structure Conversion

Convert structures between formats supported by ASE.

#### VASP to CIF

```bash
python3 scripts/convert_structure.py CONTCAR relaxed.cif
```

#### VASP to XYZ

```bash
python3 scripts/convert_structure.py POSCAR structure.xyz
```

#### Quantum ESPRESSO to CIF

```bash
python3 scripts/convert_structure.py scf.in structure.cif
```

Quantum ESPRESSO `.in` files are explicitly read using ASE's `espresso-in` format.

---

### 4. VASP Energy and Magnetic-Moment Summary

Extract the final `E0` energy and total magnetic moment from `OSZICAR`, together with atom-resolved magnetic moments for selected species from the final `magnetization (x)` table in `OUTCAR`.

For example:

```bash
python3 scripts/magnetic_summary.py OSZICAR OUTCAR Fe Ni
```

Example output:

```text
-123.456789 12.3456 3.821 3.764 1.215 1.187
```

The output is intentionally provided as a single space-separated numeric line:

```text
E0  TotalMag  Species1_moments...  Species2_moments...
```

The order of the requested species determines the order of the atom-resolved magnetic moments.

For example:

```bash
python3 scripts/magnetic_summary.py OSZICAR OUTCAR Ni Fe
```

reports the Ni moments before the Fe moments.

This format is convenient for copying values into data files or redirecting the output:

```bash
python3 scripts/magnetic_summary.py OSZICAR OUTCAR Fe Ni >> magnetic_data.dat
```

The current implementation is intended for standard collinear spin-polarized VASP calculations containing a `magnetization (x)` table.

## Notes

These scripts are intended as lightweight research utilities rather than replacements for comprehensive VASP or Quantum ESPRESSO analysis packages.

Users should verify calculated quantities and convergence criteria for their specific computational setup before using results in scientific analysis.

## Author

Radha Somaiya

## License

This project is released under the MIT License.

You are free to use, modify, and redistribute the code under the terms of the license.
