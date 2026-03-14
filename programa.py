import sys

# --- CORE LOGIC FUNCTIONS (Functional Style) ---

def convert_decimal(n):
    """Option 1: Returns hex string, 16-bit binary, and signed interpretation."""
    hex_val = hex(n).upper().replace("0X", "0x")
    bin_val = bin(n)[2:].zfill(16)
    # SIGNED16 rules [cite: 490, 491]
    signed_val = n if n < 32768 else n - 65536
    return hex_val, bin_val, signed_val

def pack_u16_le(n):
    """Option 2: Returns (low_byte, high_byte)[cite: 506]."""
    low = n & 0xFF
    high = (n >> 8) & 0xFF
    return low, high

def unpack_u16_le(low, high):
    """Option 2: Reconstructs n from bytes[cite: 507]."""
    return low + (high << 8)

def get_ascii_info(s):
    """Option 3: Returns list of (address, hex_val) tuples and length[cite: 517]."""
    base = 0x1000
    dump = []
    for i, char in enumerate(s):
        dump.append((hex(base + i), hex(ord(char)).upper().replace("0X", "0x")))
    # Add null terminator [cite: 520]
    null_addr = hex(base + len(s))
    dump.append((null_addr, "0x00"))
    return dump, len(s)

def calculate_address(base, index, size):
    """Option 4: base + index * size[cite: 533]."""
    return base + (index * size)

def get_stack_frame(a, b):
    """Option 5: Returns offsets and register values [cite: 552-567]."""
    # bp is a placeholder for offsets
    frame = [
        ("bp", "RETURN"),
        ("bp+2", f"a = {a}"),
        ("bp+4", f"b = {b}")
    ]
    registers = {"AX": a, "BX": b, "SUM": a + b}
    return frame, registers

# --- TOY MEMORY MODEL [cite: 446, 599] ---
toy_memory = {}

def memory_write(addr, val):
    toy_memory[addr] = val

def memory_read(addr):
    return toy_memory.get(addr, 0)

# --- MENU INTERFACE (Imperative Style) ---

def run_menu():
    while True:
        print("\n" + "="*30)
        print("1) Convert (decimal -> hex and 16-bit binary)")
        print("2) Little-endian pack/unpack (16-bit)")
        print("3) ASCII memory dump")
        print("4) Array addressing")
        print("5) Stack frame (bp offsets)")
        print("0) Exit")
        print("="*30)
        
        choice = input("Enter option (0-5): ")

        if choice == "1":
            n = int(input("Enter integer (0-65535): "))
            h, b, s = convert_decimal(n)
            print(f"HEX {h}")
            print(f"BIN (16) = {b}")
            print(f"SIGNED16 {s}")

        elif choice == "2":
            n = int(input("Enter integer (0-65535): "))
            addr_input = input("Enter address (e.g. 0x2000): ")
            addr = int(addr_input, 16) if "0x" in addr_input else int(addr_input)
            
            low, high = pack_u16_le(n)
            print(f"LOW BYTE = {low}")
            print(f"HIGH BYTE = {high}")
            
            memory_write(addr, low)
            memory_write(addr + 1, high)
            
            r_low = memory_read(addr)
            r_high = memory_read(addr + 1)
            
            print(f"MEM [{hex(addr)}] = {hex(r_low).upper()}")
            print(f"MEM [{hex(addr+1)}] = {hex(r_high).upper()}")
            print(f"UNPACKED {unpack_u16_le(r_low, r_high)}")

        elif choice == "3":
            s = input("Enter string (max 10 chars): ")[:10]
            dump, length = get_ascii_info(s)
            for addr, val in dump:
                print(f"{addr}: {val}")
            print(f"LENGTH (until 0x00) = {length}")

        elif choice == "4":
            base = int(input("Base address: "), 16)
            idx = int(input("Index: "))
            size = int(input("Size (1 or 2): "))
            mode = input("Mode (read/write): ").lower()
            
            target = calculate_address(base, idx, size)
            print(f"ADDRESS base + index*size\n{hex(target)}")
            
            if mode == "write":
                val = int(input("Value: "))
                if size == 1:
                    memory_write(target, val & 0xFF)
                else:
                    low, high = pack_u16_le(val)
                    memory_write(target, low)
                    memory_write(target + 1, high)
                print(f"WRITE size={size} value={val} to ADDRESS {hex(target)}")
            else:
                if size == 1:
                    res = memory_read(target)
                else:
                    res = unpack_u16_le(memory_read(target), memory_read(target+1))
                print(f"READ size={size} from ADDRESS {hex(target)} = {res}")

        elif choice == "5":
            a = int(input("Enter a: "))
            b = int(input("Enter b: "))
            frame, regs = get_stack_frame(a, b)
            for label, val in frame:
                print(f"{label} : {val}")
            print(f"AX={regs['AX']}")
            print(f"BX={regs['BX']}")
            print(f"AX (AX+BX) = {regs['SUM']}")

        elif choice == "0":
            print("Exiting...")
            break

if __name__ == "__main__":
    run_menu()