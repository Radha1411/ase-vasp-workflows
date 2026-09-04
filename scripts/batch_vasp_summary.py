"""
batch_vasp_summary.py

This will scan subdirectories for VASP OUTCAR files (OER intermediates) and print
a compact summary table using ASE.

Author: Radha Somaiya
"""

import os
from ase.io import read


def read_outcar_text(filename):
    """Read OUTCAR as plain text."""
    with open(filename, "r", errors="ignore") as file:
        return file.read()


def check_electronic_convergence(content):
    """Check whether the electronic SCF loop reached EDIFF."""
    return "aborting loop because EDIFF is reached" in content


def get_nsw(content):
    """Extract NSW from OUTCAR."""
    for line in content.splitlines():
        if "NSW" in line and "=" in line:
            parts = line.split()

            for i, part in enumerate(parts):
                if part == "NSW" and i + 2 < len(parts):
                    try:
                        return int(parts[i + 2])
                    except ValueError:
                        pass

    return None


def check_ionic_convergence(content, nsw):
    """Check ionic convergence for relaxation calculations."""

    if nsw == 0:
        return "N/A"

    if (
        "reached required accuracy - stopping structural energy minimisation"
        in content
    ):
        return "Yes"

    return "No"


def summarize_outcar(folder, outcar):
    """Extract summary information from one OUTCAR."""

    atoms = read(outcar)

    energy = atoms.get_potential_energy()
    formula = atoms.get_chemical_formula()
    natoms = len(atoms)

    content = read_outcar_text(outcar)

    electronic = (
        "Yes"
        if check_electronic_convergence(content)
        else "No"
    )

    nsw = get_nsw(content)
    ionic = check_ionic_convergence(content, nsw)

    return {
        "folder": folder,
        "formula": formula,
        "natoms": natoms,
        "energy": energy,
        "electronic": electronic,
        "ionic": ionic,
    }


def main():
    """Scan subdirectories for OUTCAR files."""

    results = []

    for entry in sorted(os.listdir(".")):
        if not os.path.isdir(entry):
            continue

        outcar = os.path.join(entry, "OUTCAR")

        if os.path.isfile(outcar):
            try:
                result = summarize_outcar(entry, outcar)
                results.append(result)

            except Exception as error:
                print(f"Warning: Could not read {outcar}: {error}")

    if not results:
        print("No OUTCAR files found in subdirectories.")
        return

    print()
    print(
        f"{'Folder':<16}"
        f"{'Formula':<24}"
        f"{'Atoms':>8}"
        f"{'Energy (eV)':>16}"
        f"{'Elec. Conv.':>14}"
        f"{'Ionic Conv.':>14}"
    )

    print("-" * 92)

    for result in results:
        print(
            f"{result['folder']:<16}"
            f"{result['formula']:<24}"
            f"{result['natoms']:>8}"
            f"{result['energy']:>16.6f}"
            f"{result['electronic']:>14}"
            f"{result['ionic']:>14}"
        )


if __name__ == "__main__":
    main()
