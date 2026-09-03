"""
vasp_summary.py

A lightweight utility for extracting basic information
from a completed VASP calculation using ASE.

Author: Radha Somaiya
"""

import sys
from ase.io import read


def check_convergence(filename):
    """Check whether VASP reports electronic/ionic convergence."""

    with open(filename, "r", errors="ignore") as file:
        content = file.read()

    convergence_messages = [
        "reached required accuracy",
        "aborting loop because EDIFF is reached"
    ]

    return any(message in content for message in convergence_messages)


def main():
    """Read a VASP OUTCAR file and print a calculation summary."""

    if len(sys.argv) != 2:
        print("Usage: python vasp_summary.py OUTCAR")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        atoms = read(filename)

        energy = atoms.get_potential_energy()
        formula = atoms.get_chemical_formula()
        natoms = len(atoms)

        converged = check_convergence(filename)

        print("\nVASP Calculation Summary")
        print("------------------------")
        print(f"File:         {filename}")
        print(f"Formula:      {formula}")
        print(f"Atoms:        {natoms}")
        print(f"Final energy: {energy:.6f} eV")
        print(f"Converged:    {'Yes' if converged else 'No'}")

    except FileNotFoundError:
        print(f"Error: File '{filename}' was not found.")
        sys.exit(1)

    except Exception as error:
        print(f"Error while reading VASP output: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
