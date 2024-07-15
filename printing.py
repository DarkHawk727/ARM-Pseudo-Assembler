import re
from typing import Dict

from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Define colors for different field types
OPCODE_COLOR = Fore.RED
RD_COLOR = Fore.BLUE
RN_COLOR = Fore.GREEN
RM_COLOR = Fore.YELLOW
RT_COLOR = Fore.MAGENTA
IMM_COLOR = Fore.CYAN
SHAMT_COLOR = Fore.LIGHTBLUE_EX
OP_COLOR = Fore.LIGHTRED_EX

# Update color schemes
color_schemes = {
    "B": [(OPCODE_COLOR, 6, "opcode"), (IMM_COLOR, 26, "imm26")],
    "ADD": [
        (OPCODE_COLOR, 11, "opcode"),
        (RM_COLOR, 5, "Rm"),
        (SHAMT_COLOR, 6, "shamt"),
        (RN_COLOR, 5, "Rn"),
        (RD_COLOR, 5, "Rd"),
    ],
    "SUB": [
        (OPCODE_COLOR, 11, "opcode"),
        (RM_COLOR, 5, "Rm"),
        (SHAMT_COLOR, 6, "shamt"),
        (RN_COLOR, 5, "Rn"),
        (RD_COLOR, 5, "Rd"),
    ],
    "ADDI": [
        (OPCODE_COLOR, 10, "opcode"),
        (IMM_COLOR, 12, "imm12"),
        (RN_COLOR, 5, "Rn"),
        (RD_COLOR, 5, "Rd"),
    ],
    "SUBI": [
        (OPCODE_COLOR, 10, "opcode"),
        (IMM_COLOR, 12, "imm12"),
        (RN_COLOR, 5, "Rn"),
        (RD_COLOR, 5, "Rd"),
    ],
    "CBZ": [(OPCODE_COLOR, 8, "opcode"), (IMM_COLOR, 19, "imm19"), (RT_COLOR, 5, "Rt")],
    "CBNZ": [
        (OPCODE_COLOR, 8, "opcode"),
        (IMM_COLOR, 19, "imm19"),
        (RT_COLOR, 5, "Rt"),
    ],
    "LDUR": [
        (OPCODE_COLOR, 11, "opcode"),
        (IMM_COLOR, 9, "imm9"),
        (OP_COLOR, 2, "op"),
        (RN_COLOR, 5, "Rn"),
        (RT_COLOR, 5, "Rt"),
    ],
    "STUR": [
        (OPCODE_COLOR, 11, "opcode"),
        (IMM_COLOR, 9, "imm9"),
        (OP_COLOR, 2, "op"),
        (RN_COLOR, 5, "Rn"),
        (RT_COLOR, 5, "Rt"),
    ],
}


def print_legend():
    print("Legend:")
    field_colors = {
        "opcode": OPCODE_COLOR,
        "Rd": RD_COLOR,
        "Rn": RN_COLOR,
        "Rm": RM_COLOR,
        "Rt": RT_COLOR,
        "imm": IMM_COLOR,
        "shamt": SHAMT_COLOR,
        "op": OP_COLOR,
    }
    for field, color in field_colors.items():
        print(f"{color}{field}{Style.RESET_ALL}", end=" ")
    print("\n")


def color_binary_instruction(binary: int, OPCODE_MAP: Dict[str, int]) -> str:
    bin_str = format(binary, "032b")

    for instr, opcode in OPCODE_MAP.items():
        mask = (1 << 32) - 1
        shift = 0
        while opcode & 1 == 0:
            opcode >>= 1
            mask >>= 1
            shift += 1
        if (binary & (mask << shift)) == OPCODE_MAP[instr]:
            scheme = color_schemes[instr]
            result = ""
            start = 0
            for color, length, _ in scheme:
                end = start + length
                result += f"{color}{bin_str[start:end]}{Style.RESET_ALL}"
                start = end
            return result

    return f"Unknown instruction: {bin_str}"


def color_string_instruction(instruction: str) -> str:
    parts = instruction.replace(",", "").split()
    opcode = parts[0]

    if opcode == "B":
        return f"{OPCODE_COLOR}{opcode}{Style.RESET_ALL} {IMM_COLOR}{parts[1]}{Style.RESET_ALL}"
    elif opcode in ["ADD", "SUB"]:
        return f"{OPCODE_COLOR}{opcode}{Style.RESET_ALL} {RD_COLOR}{parts[1]}{Style.RESET_ALL}, {RN_COLOR}{parts[2]}{Style.RESET_ALL}, {RM_COLOR}{parts[3]}{Style.RESET_ALL}"
    elif opcode in ["ADDI", "SUBI"]:
        return f"{OPCODE_COLOR}{opcode}{Style.RESET_ALL} {RD_COLOR}{parts[1]}{Style.RESET_ALL}, {RN_COLOR}{parts[2]}{Style.RESET_ALL}, {IMM_COLOR}{parts[3]}{Style.RESET_ALL}"
    elif opcode in ["CBZ", "CBNZ"]:
        return f"{OPCODE_COLOR}{opcode}{Style.RESET_ALL} {RT_COLOR}{parts[1]}{Style.RESET_ALL}, {IMM_COLOR}{parts[2]}{Style.RESET_ALL}"
    elif opcode in ["LDUR", "STUR"]:
        return f"{OPCODE_COLOR}{opcode}{Style.RESET_ALL} {RT_COLOR}{parts[1]}{Style.RESET_ALL}, [{RN_COLOR}{parts[2][1:]}{Style.RESET_ALL}, {IMM_COLOR}{parts[3][:-1]}{Style.RESET_ALL}]"
    else:
        return f"Unknown instruction: {instruction}"
