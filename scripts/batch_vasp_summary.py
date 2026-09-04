"""
batch_vasp_summary.py

Scan subdirectories for VASP OUTCAR files, print
a compact summary table, and save the results to CSV.

Author: Radha Somaiya
"""

import os
import csv
from ase.io import read


def read_outcar_text(filename):
    """Read OUTCAR as plain text."""

    with open(filename, "r", errors="ignore") as file:
        return file.read()


def check_electronic_convergence(content):
    """
    Check whether the electronic SCF loop reached EDIFF.
    """

    return "aborting loop because EDIFF is reached" in content


def get_nsw(content):
    """
    Extract NSW from OUTCAR.

    NSW = 0 usually indicates a static calculation.
    NSW > 0 indicates that ionic steps were allowed.
    """

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
    """
    Check ionic convergence.

    Returns:
        N/A  -> static calculation
        Yes  -> ionic relaxation converged
        No   -> ionic relaxation did not reach convergence
    """

    if nsw == 0:
        return "N/A"

    if (
        "reached required accuracy - stopping structural energy minimisation"
        in content
    ):
        return "Yes"

    return "No"


def summarize_outcar(folder, outcar):
    """
    Extract useful information from one VASP OUTCAR file.
    """

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


def print_results(results):
    """
    Print results as a formatted table.
    """

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


def save_csv(results, filename="vasp_summary.csv"):
    """
    Save batch results to a CSV file.
    """

    fieldnames = [
        "Folder",
        "Formula",
        "Atoms",
        "Energy_eV",
        "Electronic_Convergence",
        "Ionic_Convergence",
    ]

    with open(filename, "w", newline="") as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=fieldnames
        )

        writer.writeheader()

        for result in results:
            writer.writerow(
                {
                    "Folder": result["folder"],
                    "Formula": result["formula"],
                    "Atoms": result["natoms"],
                    "Energy_eV": f"{result['energy']:.6f}",
                    "Electronic_Convergence": result["electronic"],
                    "Ionic_Convergence": result["ionic"],
                }
            )

    print()
    print(f"Results saved to: {filename}")


def main():
    """
    Scan subdirectories for OUTCAR files.
    """

    results = []

    for entry in sorted(os.listdir(".")):

        if not os.path.isdir(entry):
            continue

        outcar = os.path.join(entry, "OUTCAR")

        if os.path.isfile(outcar):

            try:
                result = summarize_outcar(
                    entry,
                    outcar
                )

                results.append(result)

            except Exception as error:
                print(
                    f"Warning: Could not read "
                    f"{outcar}: {error}"
                )

    if not results:
        print(
            "No OUTCAR files found "
            "in subdirectories."
        )
        return

    print_results(results)

    save_csv(results)


if __name__ == "__main__":
    main()
