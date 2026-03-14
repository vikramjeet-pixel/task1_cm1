# 1. Introduction

This project implements a menu-driven calculator and memory utility in Python, simulating basic 16-bit processor operations. It includes functions for decimal-to-hexadecimal conversion, little-endian byte packing/unpacking, ASCII memory dumping, array addressing, and stack frame simulation.

# 2. Core Logic Functions

The project uses a functional programming style for the core logic, with type hints and docstrings.

## 2.1. `convert_decimal(n)`

Converts an integer to its hexadecimal representation, 16-bit binary string, and signed 16-bit integer value.

- **Input**: `n` (integer, 0-65535)
- **Output**: `(hex_val, bin_val, signed_val)`
- **Logic**: Uses Python's built-in `hex()` and `bin()` functions with string formatting for padding.

## 2.2. `pack_u16_le(n)` and `unpack_u16_le(low, high)`

Implements little-endian byte packing and unpacking for 16-bit unsigned integers.

- **Packing**: Splits a 16-bit integer into low and high bytes.
- **Unpacking**: Reconstructs the integer from low and high bytes.

## 2.3. `get_ascii_info(s)`

Generates an ASCII memory dump for a given string, including a null terminator.

- **Base Address**: Starts at `0x1000`
- **Null Terminator**: Appends `0x00` at the end of the dump
- **Output**: List of `(address, hex_value)` tuples and string length

## 2.4. `calculate_address(base, index, size)`

Calculates memory addresses using the formula: `base + index * size`.

## 2.5. `get_stack_frame(a, b)`

Simulates a stack frame with return address and two local variables.

- **Offsets**: `bp`, `bp+2`, `bp+4`
- **Registers**: Returns `AX`, `BX`, and their sum

# 3. Toy Memory Model

A simple dictionary-based memory simulation is implemented for testing purposes.

- **`toy_memory`**: Dictionary storing memory addresses and values
- **`memory_write(addr, val)`**: Writes a value to memory
- **`memory_read(addr)`**: Reads a value from memory (returns 0 if address is empty)

# 4. Menu Interface

The main program provides an interactive menu to test each function.

## 4.1. Menu Options

1. **Convert**: Decimal to hex and binary
2. **Pack/Unpack**: Little-endian operations
3. **ASCII Dump**: String to memory dump
4. **Array Addressing**: Address calculation with read/write
5. **Stack Frame**: Stack simulation
0. **Exit**

## 4.2. Input Validation

- **Integers**: Validated to be within 0-65535 for packing/unpacking
- **Addresses**: Can be entered with or without `0x` prefix
- **Strings**: Truncated to 10 characters
- **Mode**: Case-insensitive (read/write)

# 5. Unit Tests

The project includes a comprehensive test suite using Python's `unittest` framework.

## 5.1. Test Coverage

- **Option 1**: Binary length, signed boundaries, format validation
- **Option 2**: Pack/unpack boundaries, byte values
- **Option 3**: ASCII dump logic, null terminator, empty strings
- **Option 4**: Address calculation variations
- **Option 5**: Stack frame structure and register values
- **Additional Tests**: Zero input, max values, memory operations

## 5.2. Running Tests

```bash
python3 -m unittest testA.py
```

# 6. Usage Examples

## 6.1. Decimal Conversion

```
Enter option (0-5): 1
Enter integer (0-65535): 4660
HEX 0x1234
BIN (16) = 0001001000110100
SIGNED16 4660
```

## 6.2. Little-Endian Packing

```
Enter option (0-5): 2
Enter integer (0-65535): 4660
Enter address (e.g. 0x2000): 0x2000
LOW BYTE = 52
HIGH BYTE = 18
MEM [0x2000] = 0X34
MEM [0x2001] = 0X12
UNPACKED 4660
```

## 6.3. ASCII Dump

```
Enter option (0-5): 3
Enter string (max 10 chars): HELLO
0x1000: 0x48
0x1001: 0x45
0x1002: 0x4C
0x1003: 0x4C
0x1004: 0x4F
0x1005: 0x00
LENGTH (until 0x00) = 5
```

## 6.4. Array Addressing

```
Enter option (0-5): 4
Base address: 0x1000
Index: 2
Size (1 or 2): 2
Mode (read/write): write
Value: 1234
WRITE size=2 value=1234 to ADDRESS 0x1004
```

## 6.5. Stack Frame

```
Enter option (0-5): 5
Enter a: 10
Enter b: 20
bp : RETURN
bp+2 : a = 10
bp+4 : b = 20
AX=10
BX=20
AX (AX+BX) = 30
```

# 7. Implementation Details

## 7.1. Type Hinting

All core functions use type hints for better code readability and maintainability:

```python
def convert_decimal(n: int) -> tuple[str, str, int]:
    """Option 1: Returns hex string, 16-bit binary, and signed interpretation."""
```

## 7.2. String Formatting

- **Hexadecimal**: `hex(n).upper().replace("0X", "0x")` ensures consistent formatting
- **Binary**: `bin(n)[2:].zfill(16)` pads with leading zeros to 16 bits

## 7.3. Memory Management

The `toy_memory` dictionary is cleared at the start of each test run to ensure test isolation.

# 8. Getting Started

## 8.1. Prerequisites

- **Python 3.6+**: The project is compatible with modern Python 3.
- No external libraries or tools are required. Everything is built-in within the Standard Library.

## 8.2. Running the main application

To load the interactive subroutines menu in your terminal console, run:

```bash
python programa.py
```

This will initialize the loop allowing you to toggle smoothly between operations (0 through 5).

## 8.3. Running the Test Suite

To execute the series of unit checks on formatting logic, bounds handling, and isolated runtime logic, run:

```bash
python -m unittest testA.py
```

# 9. Project Structure

- `programa.py`: Implements numerical formats logic, standard routines, dummy registers and stack states structure, alongside a text interface via `run_menu()`.
- `testA.py`: Wraps functions into isolated behaviors via testing framework, explicitly making boundaries calculations deterministic.
