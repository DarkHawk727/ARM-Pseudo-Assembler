import argparse
import sys
from typing import List

from assembler import convert_instruction_to_int, parse
from printing import color_binary_instruction, color_string_instruction

OPCODE_MAP = {
    "B": 0b000101 << 26,
    "ADD": 0b10001011000 << 21,
    "ADDI": 0b1001000100 << 22,
    "CBZ": 0b10110100 << 24,
    "CBNZ": 0b10110101 << 24,
    "SUB": 0b11001011000 << 21,
    "SUBI": 0b1101000100 << 22,
    "STUR": 0b11111000000 << 21 | 0b01 << 19,
    "LDUR": 0b11111000010 << 21 | 0b10 << 19,
}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Process and display ARM assembly instructions."
    )
    parser.add_argument(
        "input_file", help="Input file containing ARM assembly instructions"
    )
    parser.add_argument(
        "-p",
        "--print",
        action="store_true",
        help="Print colored instructions and binary representation",
    )
    args = parser.parse_args()

    binaries = []
    with open(args.input_file, "r") as program:
        if args.print:
            print(f"{' PROGRAM ':=^30}")
        for i, line in enumerate(program.readlines()):
            toks: List[str | int] = parse(line)
            binary = convert_instruction_to_int(toks, OPCODE_MAP)

            if toks[0] == "B":
                binary = binary & ((1 << 32) - 1)  # Mask to 32 bits

            binaries.append(binary)
            if args.print:
                print(f"{i}: {color_string_instruction(line.strip())}")

    if args.print:
        print(f"{' BINARY ':=^30}")
        for i, entry in enumerate(binaries):
            print(f"{i}: {color_binary_instruction(entry, OPCODE_MAP)}")

    output_file = f"{(args.input_file.split('.')[0])}.binasm"
    with open(output_file, "w") as out:
        for line in binaries:
            out.write(f"{format(line, '032b')}\n")

    if args.print:
        print(f"\nBinary output written to {output_file}")


if __name__ == "__main__":
    main()
