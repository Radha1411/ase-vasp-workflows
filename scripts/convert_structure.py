"""
convert_structure.py

Convert atomic structures between common file formats using ASE.

Supported examples:
    VASP:
        python3 convert_structure.py CONTCAR relaxed.cif
        python3 convert_structure.py POSCAR structure.xyz

    Quantum ESPRESSO:
        python3 convert_structure.py scf.in structure.cif

Author: Radha Somaiya
"""

import sys
import os
from ase.io import read, write


def read_structure(filename):
    """
    Read an atomic structure.

    Quantum ESPRESSO input files commonly use the .in extension,
    which does not uniquely identify the file format. Therefore,
    ASE is explicitly told to use the espresso-in reader.
    """

    extension = os.path.splitext(filename)[1].lower()

    if extension == ".in":
        return read(filename, format="espresso-in")

    return read(filename)


def main():
    """Convert an atomic structure from one file format to another."""

    if len(sys.argv) != 3:
        print(
            "Usage: python3 convert_structure.py "
            "INPUT_FILE OUTPUT_FILE"
        )
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        atoms = read_structure(input_file)

        write(output_file, atoms)

        print("Structure conversion completed")
        print("------------------------------")
        print(f"Input:   {input_file}")
        print(f"Output:  {output_file}")
        print(f"Formula: {atoms.get_chemical_formula()}")
        print(f"Atoms:   {len(atoms)}")

    except FileNotFoundError:
        print(f"Error: File '{input_file}' was not found.")
        sys.exit(1)

    except Exception as error:
        print(f"Error during structure conversion: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
