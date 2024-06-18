import math


def float_to_integer(float_int: int, exp_width: int, sig_width: int) -> (float):
    """
        Converts integer in generic floating-point representation to a float with decimal representation

        Args:
            float_int (int): The floating-point number
            exp_width (int): The exponent width of the floating-point number 
            sig_width (int): The significant width (precision-1) of the floating-point number

        Returns:
            float: The decimal representation
    """

    sign = (float_int >> (sig_width + exp_width)) & 1
    exp_biased = (float_int >> sig_width) & (2 ** exp_width - 1)
    significand = (float_int & (2 ** sig_width - 1))

    if exp_biased == (2 ** exp_width - 1) and significand == 0:
        return (-1)**sign * float('inf')
    if exp_biased == (2 ** exp_width - 1) and significand != 0:
        return (-1)**sign * float('nan')

    if exp_biased == 0:
        exp_unbiased = -(2 ** (exp_width - 1) - 1) + 1
        mantissa = significand
    else:
        exp_unbiased = exp_biased - (2 ** (exp_width - 1) - 1)
        mantissa = significand + (1 << sig_width)

    decimal_out = mantissa / (2 ** (sig_width - exp_unbiased))
    decimal_out = (-1)**sign * decimal_out
    return decimal_out


if __name__ == '__main__':
    message = ""
    while message == "" or not message.isnumeric():
        message = input("Set exp_width: ")
    exp_width = int(message)

    message = ""
    while message == "" or not message.isnumeric():
        message = input("Set sig_width: ")
    sig_width = int(message)

    radix = 16
    print(f"\nStarting Calculator for sig_width={sig_width}, exp_width={exp_width}")
    print("-Use 'hex' and 'bin' to change input radix")
    print("Use <_0> or <_1> postfix to pad the end of number")
    print("-Press exit or quit(q) to finish")
    print("====================================================")
    while True:
        message = ""
        while message == "" or not (message.isalnum() or (message[0:-2].isalnum() and
                                    (message.endswith("_1") or message.endswith("_0"))) or
                                    message == "hex" or message == "bin" or message == "exit"
                                    or message == "quit" or message == "q"):
            if message != "":
                print("Wrong")
            if radix == 2:
                message = input("Enter float (binary): ")
            else:
                message = input("Enter float (hex): ")

        # Exit Calc Loop
        if message == "exit" or message == "quit" or message == "q":
            break

        # Change radix
        if message == "hex":
            radix = 16
            continue
        if message == "bin":
            radix = 2
            continue

        # Set padding
        if message.endswith("_0"):
            pad_zeros = True
            pad_ones = False
            message = message[0:-2]
        elif message.endswith("_1"):
            pad_zeros = False
            pad_ones = True
            message = message[0:-2]
        else:
            pad_zeros = False
            pad_ones = False

        # Interpret Number
        try:
            float_int = int(message, radix)
        except Exception as e:
            print(e)
            continue

        # Pad Number
        if radix == 2:
            float_str = bin(float_int)
        else:
            float_str = hex(float_int)
        if pad_zeros:
            float_int = int(
                float_str.ljust(math.ceil((sig_width + exp_width + 1) / (math.ceil(math.log2(radix)))) + 2, "0"),
                radix)
        if pad_ones:
            pad_char = "1" if radix == 2 else "F"
            float_int = int(
                float_str.ljust(math.ceil((sig_width + exp_width + 1) / (math.ceil(math.log2(radix)))) + 2, pad_char),
                radix)

        # Conversion
        decimal_out = float_to_integer(float_int, exp_width, sig_width)

        # Print Output
        print(f"Decimal: {decimal_out}")
        print("--------------------------------")

    print("Exited calculator")
