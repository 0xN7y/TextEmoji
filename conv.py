#N7y
from sys import argv


if len(argv) < 2:
    print("Encode string to Emojie\n\t\tAuther: N7y")
    print("USAGE : python3 conv.py 'hi' ")
    exit()
elif len(argv) > 3:
    c = argv[1]

    text = ' '.join(argv[1:])
else:

    text = argv[1]
    


# 6-bit len  = 2^6 = (64 emojis) 
bin_e6bit = {
    '000000': '😀', '000001': '😁', '000010': '😂', '000011': '🤣', '000100': '😃', '000101': '😄', 
    '000110': '😅', '000111': '😆', '001000': '😉', '001001': '😊', '001010': '😋', '001011': '😎', 
    '001100': '😍', '001101': '😘', '001110': '🥰', '001111': '😗', '010000': '😙', '010001': '😚', 
    '010010': '🙂', '010011': '🤗', '010100': '🤔', '010101': '🤩', '010110': '🤨', '010111': '😐', 
    '011000': '😑', '011001': '😶', '011010': '🙄', '011011': '😏', '011100': '😣', '011101': '😥', 
    '011110': '😮', '011111': '😴', '100000': '🤤', '100001': '🤢', '100010': '🤧', '100011': '😷', 
    '100100': '🤯', '100101': '🤠', '100110': '🥳', '100111': '🥺', '101000': '🤖', '101001': '👾', 
    '101010': '👽', '101011': '👻', '101100': '👹', '101101': '👺', '101110': '💀', '101111': '☠️', 
    '110000': '👿', '110001': '😈', '110010': '🧛', '110011': '🧟', '110100': '🧞', '110101': '🧜', 
    '110110': '🧚', '110111': '🧙', '111000': '🦸', '111001': '🦹', '111010': '🧑', '111011': '👤', 
    '111100': '👥', '111101': '🗣️', '111110': '🧠', '111111': '🦴'
}

# rev mapping for dec
emoji_bin6bit = {v: k for k, v in bin_e6bit.items()}

# t to bin
def convtxt(txt):
    return ''.join(f'{ord(c):08b}' for c in txt)

# (RLE)

def rlecompress(txt):
    compressed = []
    count = 1
    for i in range(1, len(txt)):
        if txt[i] == txt[i-1]:
            count += 1
        else:
            compressed.append(txt[i-1] + str(count))
            count = 1
    compressed.append(txt[-1] + str(count))
    return ''.join((compressed))



# error detection
def add_parity_bit(binary):
    count_ones = binary.count('1')
    parity_bit = '0' if count_ones % 2 == 0 else '1'
    return binary + parity_bit

#pad binary string for 6-bit encoding
def pad_binary_6bit(binary):
    remainder = len(binary) % 6
    if remainder != 0:
        padding_bits = 6 - remainder
        binary += '0' * padding_bits
        return binary, padding_bits
    return binary, 0


def bin_to_e6bit(binary):
    binary_groups = [binary[i:i+6] for i in range(0, len(binary), 6)]
    return ''.join(bin_e6bit[group] for group in binary_groups)


def encode_tto_emo(txt):
    compressed_t = rlecompress(txt)
    binary = convtxt(compressed_t)
    bin_w_parity = add_parity_bit(binary)

    padded_bin, padding_bits = pad_binary_6bit(bin_w_parity)

    enc_em = bin_to_e6bit(padded_bin)
    
    return enc_em, padding_bits



def rm_parity_bit(binary):
    # rm last bit
    return binary[:-1]

def binary_to_txt(binary):
    binary_chunks = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(chunk, 2)) for chunk in binary_chunks)

def rle_decompress(txt):
    decompressed = []
    i = 0
    while i < len(txt):
        char = txt[i]
        count = ''
        while i + 1 < len(txt) and txt[i+1].isdigit():
            count += txt[i+1]
            i += 1
        decompressed.append(char * int(count))
        i += 1
    return ''.join(decompressed)

# decode emojis back into txt
def decode_emojis_to_txt(emojis, padding_bits):
    binary = ''.join(emoji_bin6bit[emoji] for emoji in emojis) # if emoji in bin_e6bit)
    if padding_bits > 0:
        binary = binary[:-padding_bits]
    bin_no_parity = rm_parity_bit(binary)
    
    decompressed = binary_to_txt(bin_no_parity)
    return rle_decompress(decompressed)


enc_em, padding_bits = encode_tto_emo(text)
decoded_txt = decode_emojis_to_txt(enc_em, padding_bits)


print(decoded_txt," = ",enc_em)
