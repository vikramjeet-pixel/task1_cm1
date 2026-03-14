import unittest
from programa import (
    convert_decimal, pack_u16_le, unpack_u16_le, 
    get_ascii_info, calculate_address, get_stack_frame,
    memory_read, memory_write, toy_memory
)

class TestCalculator(unittest.TestCase):

    # Option 1 Tests [cite: 576, 577]
    def test_conversion_binary_length(self):
        _, b, _ = convert_decimal(255)
        self.assertEqual(len(b), 16)

    def test_signed_16_boundary(self):
        _, _, s = convert_decimal(65535)
        self.assertEqual(s, -1)
        _, _, s2 = convert_decimal(32768)
        self.assertEqual(s2, -32768)

    # Option 2 Tests [cite: 572]
    def test_pack_unpack_boundaries(self):
        for n in [0, 1, 255, 256, 65535]:
            low, high = pack_u16_le(n)
            self.assertEqual(unpack_u16_le(low, high), n)

    # Option 3 Tests [cite: 573]
    def test_ascii_dump_logic(self):
        dump, length = get_ascii_info("HELLO")
        self.assertEqual(length, 5)
        self.assertEqual(dump[-1][1], "0x00") # Null terminator check

    # Option 4 Tests [cite: 574]
    def test_array_addressing(self):
        addr = calculate_address(1000, 3, 2)
        self.assertEqual(addr, 1006)

    # Option 5 Tests [cite: 575]
    def test_stack_frame_sum(self):
        _, regs = get_stack_frame(10, 20)
        self.assertEqual(regs['SUM'], 30)

    # Additional Quality Tests [cite: 644]
    def test_zero_input(self):
        h, b, s = convert_decimal(0)
        self.assertEqual(h, "0x0")
        self.assertEqual(s, 0)

    def test_max_byte_packing(self):
        low, high = pack_u16_le(65535)
        self.assertEqual(low, 255)
        self.assertEqual(high, 255)

    def test_convert_decimal_format(self):
        h, b, s = convert_decimal(255)
        self.assertEqual(h, "0xFF")
        self.assertEqual(b, "0000000011111111")
        self.assertEqual(s, 255)

        h2, b2, s2 = convert_decimal(4660)
        self.assertEqual(h2, "0x1234")
        self.assertEqual(b2, "0001001000110100")
        self.assertEqual(s2, 4660)

    def test_pack_u16_le_values(self):
        low, high = pack_u16_le(0x1234)
        self.assertEqual(low, 0x34)
        self.assertEqual(high, 0x12)

    def test_get_ascii_info_values(self):
        dump, length = get_ascii_info("A")
        self.assertEqual(length, 1)
        self.assertEqual(dump[0], (hex(0x1000), "0x41"))
        self.assertEqual(dump[1], (hex(0x1001), "0x00"))

    def test_get_ascii_info_empty(self):
        dump, length = get_ascii_info("")
        self.assertEqual(length, 0)
        self.assertEqual(dump[0], (hex(0x1000), "0x00"))

    def test_calculate_address_variations(self):
        self.assertEqual(calculate_address(0x1000, 0, 1), 0x1000)
        self.assertEqual(calculate_address(0x1000, 5, 2), 0x100A)
        self.assertEqual(calculate_address(0x200, 10, 4), 0x228)

    def test_get_stack_frame_structure(self):
        frame, regs = get_stack_frame(5, 7)
        self.assertEqual(regs['AX'], 5)
        self.assertEqual(regs['BX'], 7)
        self.assertEqual(regs['SUM'], 12)
        
        self.assertEqual(frame[0], ("bp", "RETURN"))
        self.assertEqual(frame[1], ("bp+2", "a = 5"))
        self.assertEqual(frame[2], ("bp+4", "b = 7"))

    def test_memory_read_write(self):
        toy_memory.clear()
        memory_write(0x1000, 0xAA)
        self.assertEqual(memory_read(0x1000), 0xAA)
        self.assertEqual(memory_read(0x1001), 0)

if __name__ == "__main__":
    unittest.main()