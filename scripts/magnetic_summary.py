"""
magnetic_summary.py

Extract final energy, total magnetic moment, and
atom-resolved magnetic moments for selected species
from a VASP calculation.

Usage:
    python3 magnetic_summary.py OSZICAR OUTCAR Fe Ni

Output:
    E0 TotalMag Fe_moments... Ni_moments...

Author: Radha Somaiya
"""

import re
import sys
from ase.io import read


def get_final_oszicar_values(filename):
    """
    Extract the final E0 energy and total magnetic moment
    from OSZICAR.
    """

    final_e0 = None
    final_mag = None

    with open(filename, "r", errors="ignore") as file:

        for line in file:

            # Extract E0
            e0_match = re.search(
                r"E0=\s*"
                r"([+-]?(?:\d+(?:\.\d*)?|\.\d+)"
                r"(?:[Ee][+-]?\d+)?)",
                line,
            )

            if e0_match:
                final_e0 = float(e0_match.group(1))

            # Extract total magnetic moment
            mag_match = re.search(
                r"\bmag=\s*"
                r"([+-]?(?:\d+(?:\.\d*)?|\.\d+)"
                r"(?:[Ee][+-]?\d+)?)",
                line,
            )

            if mag_match:
                final_mag = float(mag_match.group(1))

    return final_e0, final_mag


def get_final_magnetization_table(filename):
    """
    Extract the final magnetization (x) table from OUTCAR.

    Returns:
        dictionary:
            atom_number -> magnetic_moment
    """

    with open(filename, "r", errors="ignore") as file:
        lines = file.readlines()

    table_starts = []

    for i, line in enumerate(lines):

        if "magnetization (x)" in line.lower():
            table_starts.append(i)

    if not table_starts:
        raise ValueError(
            "No 'magnetization (x)' table found in OUTCAR."
        )

    # Use the final magnetization table
    start = table_starts[-1]

    magnetic_moments = {}

    for line in lines[start + 1:]:

        parts = line.split()

        # Atomic rows begin with the VASP atom number
        if len(parts) >= 5 and parts[0].isdigit():

            atom_index = int(parts[0])

            try:
                moment = float(parts[-1])

            except ValueError:
                continue

            magnetic_moments[atom_index] = moment

        elif magnetic_moments:

            # Stop at the total row
            if parts and parts[0].lower() == "tot":
                break

    if not magnetic_moments:

        raise ValueError(
            "Could not extract atomic magnetic moments "
            "from OUTCAR."
        )

    return magnetic_moments


def get_atomic_symbols(outcar):
    """
    Read atomic symbols from OUTCAR using ASE.
    """

    atoms = read(outcar)

    return atoms.get_chemical_symbols()


def get_selected_moments(
    symbols,
    magnetic_moments,
    selected_species,
):
    """
    Collect magnetic moments for the requested species.

    The order of selected_species is preserved.
    """

    selected = {
        species: []
        for species in selected_species
    }

    for atom_index, symbol in enumerate(
        symbols,
        start=1,
    ):

        if symbol in selected:

            if atom_index in magnetic_moments:

                selected[symbol].append(
                    (
                        atom_index,
                        magnetic_moments[atom_index],
                    )
                )

    return selected


def format_summary(
    final_e0,
    final_mag,
    selected_moments,
):
    """
    Produce one space-separated numeric line.

    Example:
    -578.199810 40.0012 3.962 4.214 4.221 4.205 1.007 ...
    """

    output = []

    # Final E0
    if final_e0 is not None:
        output.append(
            f"{final_e0:.6f}"
        )

    # Total magnetic moment
    if final_mag is not None:
        output.append(
            f"{final_mag:.4f}"
        )

    # Individual magnetic moments
    for species, moments in selected_moments.items():

        for atom_index, moment in moments:

            output.append(
                f"{moment:.3f}"
            )

    return " ".join(output)


def main():
    """
    Main program.
    """

    if len(sys.argv) < 4:

        print(
            "Usage: python3 magnetic_summary.py "
            "OSZICAR OUTCAR SPECIES [SPECIES ...]"
        )

        sys.exit(1)

    oszicar = sys.argv[1]
    outcar = sys.argv[2]

    selected_species = sys.argv[3:]

    try:

        final_e0, final_mag = (
            get_final_oszicar_values(
                oszicar
            )
        )

        magnetic_moments = (
            get_final_magnetization_table(
                outcar
            )
        )

        symbols = get_atomic_symbols(
            outcar
        )

        selected_moments = (
            get_selected_moments(
                symbols,
                magnetic_moments,
                selected_species,
            )
        )

        summary = format_summary(
            final_e0,
            final_mag,
            selected_moments,
        )

        print(summary)

    except FileNotFoundError as error:

        print(
            f"Error: {error}"
        )

        sys.exit(1)

    except Exception as error:

        print(
            f"Error while reading VASP results: {error}"
        )

        sys.exit(1)


if __name__ == "__main__":
    main()
