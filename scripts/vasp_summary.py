"""
vasp_summary.py

A lightweight utility python script for extracting basic information
from a completed VASP calculation using ASE.

Author: Radha Somaiya
"""

import sys
from ase.io import read


def read_outcar_text(filename):
    """Read the OUTCAR file as plain text."""

    with open(filename, "r", errors="ignore") as file:
        return file.read()


def check_electronic_convergence(content):
    """
    Check whether the electronic SCF loop reached convergence.

    VASP commonly writes:
    'aborting loop because EDIFF is reached'
    when the electronic minimization satisfies EDIFF.
    """

    return "aborting loop because EDIFF is reached" in content


def get_nsw(content):
    """
    Extract NSW from the OUTCAR.

    NSW = 0 usually indicates a static calculation.
    NSW > 0 indicates that ionic steps were allowed.
    """

    nsw = None

    for line in content.splitlines():
        if "NSW" in line and "=" in line:
            parts = line.split()

            for i, part in enumerate(parts):
                if part == "NSW" and i + 2 < len(parts):
                    try:
                        nsw = int(parts[i + 2])
                        return nsw
                    except ValueError:
                        pass

    return nsw


def check_ionic_convergence(content, nsw):
    """
    Determine whether ionic convergence was reached.

    Returns:
        'N/A' for static calculations
        'Yes' if VASP reports that the required accuracy was reached
        'No' otherwise
    """

    if nsw == 0:
        return "N/A"

    if "reached required accuracy - stopping structural energy minimisation" in content:
        return "Yes"

    return "No"


def main():
    """Read a VASP OUTCAR file and print a calculation summary."""

    if len(sys.argv) != 2:
        print("Usage: python3 vasp_summary.py OUTCAR")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        atoms = read(filename)

        energy = atoms.get_potential_energy()
        formula = atoms.get_chemical_formula()
        natoms = len(atoms)

        content = read_outcar_text(filename)

        electronic_converged = check_electronic_convergence(content)
        nsw = get_nsw(content)
        ionic_converged = check_ionic_convergence(content, nsw)

        print("\nVASP Calculation Summary")
        print("------------------------")
        print(f"File:                   {filename}")
        print(f"Formula:                {formula}")
        print(f"Atoms:                  {natoms}")
        print(f"Final energy:           {energy:.6f} eV")
        print(
            f"Electronic convergence: "
            f"{'Yes' if electronic_converged else 'No'}"
        )
        print(f"Ionic convergence:      {ionic_converged}")

    except FileNotFoundError:
        print(f"Error: File '{filename}' was not found.")
        sys.exit(1)

    except Exception as error:
        print(f"Error while reading VASP output: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
