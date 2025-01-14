#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::: Hash Breakdown by Silvia Binda Heiserova :::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::: MAIN CODE EXECUTED FROM RASPBERRY PI 4 MODEL B:::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

# Last adjustment: 23/04/2024 

# ! duration of 1 hashing cycle (now is cca. 4 minutes)

#import logging #for logging, testing and debugging purpose
from time import sleep
import sys
import traceback # library for printing errors
import pyttsx3 # library for converting text to speech 
import random
from socket import * # library for network communication
from database_feminism_05_03_2024 import database_feminism # importing our database python file and the array of definitions titled "database_feminism"
from auto_search_adv import parse_definitions # importing our automated internet search made in python
import auto_search_adv
import _thread # library for threads
import threading # python library for threads (higher level than _thread library)

# ANSI escape codes for colors so I can print text in color to terminal
PINK = '\033[91m'
BLACK = '\033[30m'
WHITE = '\033[37m'
BLUE = '\033[34m' 
MAGENTA = '\033[35m'
LIGHT_MAGENTA = '\033[95m'
MAGENTA_BACKGROUND = '\033[45m'
LIGHT_MAGENTA_BACKGROUND = '\033[105m'
BLUE_BACKGROUND = '\033[44m'
CYAN_BACKGROUND = '\033[46m'
RESET = '\033[0m'  # Reset to default terminal color

s = socket(AF_INET, SOCK_DGRAM) # for network UDP communication
#s.bind(('127.0.0.1', 8345)) #TESTING !!

OFF_DB_LIMIT = 1 # number of tries before accessing the online database again

info_running = True

ESP32_port = 8888
ESP32_binary_display = ('192.168.0.101', 8345)
ESP32_i2c_lcd = ('192.168.0.102', 8345)
ESP32_tft_small = ('192.168.0.103', 8345)
ESP32_oled_display = ('192.168.0.104', 8345)
 
# initial settings for text to speech conversion:
engine = pyttsx3.init() # object creation for tts
rate = engine.getProperty('rate') # to set rate of the speaking voice
engine.setProperty('rate', 140)
volume = engine.getProperty('volume') # to set the volume level of the speaking voice (min=0 and max=1)
engine.setProperty('volume', 1) 
voices = engine.getProperty('voices') # to set the type of the voice speaking
engine.setProperty('voice', voices[0].id) # changing index changes voices (0 for male, 1 for female...in total there are 18 differen voices)

# There are 2 constants in SHA256: h_hex and K:
# h_0 to h_7 are initial hash values constants
# h_0 to h_7 (first 32 bits of the fractional parts of the square roots of the first 8 primes 2..19):
h_hex = ['0x6a09e667', '0xbb67ae85', '0x3c6ef372', '0xa54ff53a', '0x510e527f', '0x9b05688c', '0x1f83d9ab', '0x5be0cd19']

# 0x before the word means it is a hexadecimal code

#SHA-256 uses a sequence of sixty-four constant 32-bit words. These words represent the first thirty-two bits of the fractional parts of
#the cube roots of the first sixty-four prime numbers. In hex, these constant words are:
K = ['0x428a2f98', '0x71374491', '0xb5c0fbcf', '0xe9b5dba5', '0x3956c25b', '0x59f111f1', '0x923f82a4',
 '0xab1c5ed5', '0xd807aa98', '0x12835b01', '0x243185be', '0x550c7dc3', '0x72be5d74', '0x80deb1fe', 
 '0x9bdc06a7', '0xc19bf174', '0xe49b69c1', '0xefbe4786', '0x0fc19dc6', '0x240ca1cc', '0x2de92c6f', 
 '0x4a7484aa', '0x5cb0a9dc', '0x76f988da', '0x983e5152', '0xa831c66d', '0xb00327c8', '0xbf597fc7', 
 '0xc6e00bf3', '0xd5a79147', '0x06ca6351', '0x14292967', '0x27b70a85', '0x2e1b2138', '0x4d2c6dfc', 
 '0x53380d13', '0x650a7354', '0x766a0abb', '0x81c2c92e', '0x92722c85', '0xa2bfe8a1', '0xa81a664b', 
 '0xc24b8b70', '0xc76c51a3', '0xd192e819', '0xd6990624', '0xf40e3585', '0x106aa070', '0x19a4c116', 
 '0x1e376c08', '0x2748774c', '0x34b0bcb5', '0x391c0cb3', '0x4ed8aa4a', '0x5b9cca4f', '0x682e6ff3', 
 '0x748f82ee', '0x78a5636f', '0x84c87814', '0x8cc70208', '0x90befffa', '0xa4506ceb', '0xbef9a3f7', 
 '0xc67178f2']   

#utils:
def isTrue(x): return x == 1
def if_(i, y, z): return y if isTrue(i) else z
def and_(i, j): return if_(i, j, 0)
def AND(i, j): return [and_(ia, ja) for ia, ja in zip(i,j)] 
def not_(i): return if_(i, 0, 1)
def NOT(i): return [not_(x) for x in i]
def xor(i, j): return if_(i, not_(j), j)
def XOR(i, j): return [xor(ia, ja) for ia, ja in zip(i, j)]
def xorxor(i, j, l): return xor(i, xor(j, l))
def XORXOR(i, j, l): return [xorxor(ia, ja, la) for ia, ja, la, in zip(i, j, l)]
def maj(i,j,k): return max([i,j,], key=[i,j,k].count)
def rotr(x, n): return x[-n:] + x[:-n]
def shr(x, n): return n * [0] + x[:-n]
def add(i, j):
  length = len(i)
  sums = list(range(length))
  c = 0
  for x in range(length-1,-1,-1):
    sums[x] = xorxor(i[x], j[x], c)
    c = maj(i[x], j[x], c)
  return sums

# function for progressive print of text
# prints the message progressively on a single line
# it takes two paramenters: 
# message (str or list) is the message to be printed, it can be a string or a list of integers;
# delay (int or float, optional) is the time delay between progressive prints, default is 0.1 second.
def progressive_print(message, delay=0.10):
    if isinstance(message, str):
        message_str = message
    elif isinstance(message, list):
        message_str = ', '.join(map(str, message))
    else:
        raise ValueError("Unsupported message type")
    for i in range (0, len(message_str)):
        print(message_str[i], end="")
        sys.stdout.flush()  # Flush the output to the terminal
        sleep(delay)    
    print()  # Move to a new line after finishing

#function for sending data to esp32's
def send_to_esp32(text, esp32):
    if not isinstance(text, str):
        text = str(text)
    try:
        # print("sending to esp32:", text) # uncomment for debugging
        s.sendto(text.encode(), esp32)
    except Exception:
        #traceback.print_exc() # prints the error details
        pass
# !!!
# function for searching empty space in ascii conversion part
def search_n_space (message, n):
    space_counter = 0
    index = 0
    for character in message:
        #print (character)
        if character == " ":
            space_counter+= 1
            if space_counter == n:
                return index
        index+= 1
    return len(message)


# Antoher function to progressively print a message
def progressive_print1(printed_message, stop_event):
    for char in printed_message:
        print(char, end='', flush=True)  # Adjusted line
        sleep(0.0)  # Adjust the speed of printing here
        if stop_event.is_set():  # Stop if the stop_event is set
            break
    print()  # Ensure the output goes to a new line after finishing
    stop_event.set()  # Signal to stop the spoken message loop

# sha-256 hashing help functions:
def translate(message):
    
    charcodes = [ord(c) for c in message]
    charcodes_str = [str(ord(c)) for c in message]
    print(LIGHT_MAGENTA + "Hi there! I am an automated code parsing definitions related to feminism from the world wide web. Please wait..." + RESET)
    engine.setProperty('voice', voices[0].id)
    engine.say("Hi there! I am an automated code parsing definitions related to feminism from the world wide web. Please wait... The definition I found is:")    
    engine.runAndWait()
    
    print(MAGENTA_BACKGROUND + "***",message,"***" + RESET)
    engine.setProperty('voice', voices[10].id)
    engine.setProperty('rate', 120)
    engine.say(message)
    send_to_esp32(message, ESP32_tft_small)
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 140)
    engine.say("Now lets hash this definition using the SHA-256 hashing algorithm. This is the breakdown of the process:")
    engine.runAndWait() 
    
    engine.setProperty('voice', voices[0].id)
    send_to_esp32("...processing...", ESP32_i2c_lcd)
    engine.say("First step is the conversion of the definition into ASCII character codes. Please see the LCD display on the right. This definition related to feminism in ASCII is:")
    engine.runAndWait()
    print(BLUE_BACKGROUND + "*** Converting the definition into ASCII character codes ***" + RESET)
    #send_to_esp32("test", ESP32_tft_small) # uncomment for testing purposes
    #print (charcodes)
    #print(charcodes_str)
    clean_message = ' '.join(charcodes_str) #join is a function that takes elements from the list (in our case charcodes) and puts a space ('') between every element
    print (clean_message)
    send_to_esp32(charcodes, ESP32_i2c_lcd) #zmena
    
    #send_to_esp32 (progressive_print (charcodes), ESP32_oled_display)
    #sleep(2)
    engine.setProperty('rate', 150) # good rate is 150 to 200
    
    #engine.say(clean_message[:50])
    engine.say(clean_message[:(search_n_space(clean_message, 10))])
    engine.say("and so on ...")
    engine.runAndWait()
    bytes = []
    for char in charcodes:
        bytes.append(bin(char)[2:].zfill(8))
        
    engine.setProperty('rate', 140)
    engine.setProperty('voice', voices[0].id)
    
    #zmena
    print (BLUE_BACKGROUND + "*** Converting the definition related to feminism from ASCII character codes into bytes ***" + RESET)
    engine.say("Converting the definition related to feminism from ASCII character codes into bytes. Please see the small display on the left.")
    engine.runAndWait()
    printed_message = ' '.join(bytes)
    send_to_esp32(printed_message[:1024], ESP32_oled_display) #the limit is 1024 because otherwise the upd protocol will not receive a longer
    print (printed_message)
    sleep(10)
    
    try:
        print (BLUE_BACKGROUND + "*** Converting the definition related to feminism from bytes into bits ***" + RESET)
        bits = []
        for byte in bytes:
            for bit in byte:
                bits.append(int(bit))
        print("Conversion to bits successful, number of bits: ", len(bits))
    except Exception as e:
        print("Failed during bytes-to-bits conversion: ", str(e))
        #zmena !!! vsade kde bolo "of feminism"
    engine.say("Now I will be converting the definition related to feminism from bytes into bits. Please see the binary display in the center.")
    engine.runAndWait()
    
    # converting it to string to be spoken out loud
    bits_string = ''.join(str(bit) for bit in bits)
    engine.setProperty('rate', 100)
    engine.say(bits_string[:20])
    send_to_esp32(bits_string[:60], ESP32_binary_display)
    engine.setProperty('rate', 140)
    engine.say("and so on ...")
    engine.runAndWait()

    #progressive_print (bits)
    sleep(2)
    number_of_bits = str(len(bits))
    print (BLUE_BACKGROUND + "*** Number of bits of this definition related to feminism is: ***" + RESET)
    engine.say("The number of bits of the definition related to feminism is:") #zmena
    engine.runAndWait()
    #sleep(2)
    #send_to_esp32  #zmena, doplnit sem na tft display aj s \n !!!
    progressive_print(str(len(bits)))
    engine.setProperty('voice', voices[10].id)
    engine.setProperty('rate', 120)
    engine.say(number_of_bits)
    engine.runAndWait()
    sleep(2)
    return bits

#divide the message in parts of 512 bits and for each part create a 64 array message of 32-bit words
def chunker(bits, chunk_length=8):
    chunked = []
    for b in range(0, len(bits), chunk_length):
        chunked.append(bits[b:b+chunk_length]) 
        chunked_append = chunked.append(bits[b:b+chunk_length]) #zmena
        print (b)
    if chunked != 16:
        print("")
    else:
        print (BLUE_BACKGROUND + "*** The number of 512 bits parts is: ***" + RESET)
        engine.say("The number of 512 bits parts now is:")
        engine.say(str(len(chunked)))
        engine.runAndWait()
    print(len(chunked))
    return chunked

def fillZeros(bits, length=8, endian='LE'):
    l = len(bits)
    if endian == 'LE':
        for i in range(l, length):
            bits.append(0)
    else: 
        while l < length:
            bits.insert(0, 0)
            l = len(bits)
    return bits

def preprocessMessage(message):
    bits = translate(message)
    length = len(bits)
    message_len = [int(b) for b in bin(length)[2:].zfill(64)]
    if length < 448:
        bits.append(1)
        print(BLUE_BACKGROUND + "*** Appending a single '1' bit at the end ***" + RESET)
        engine.say("Appending a single '1' bit at the end")
        engine.runAndWait()
        sleep(2)
        print(str(bits)[1:-1])
        sleep(2)
        bits = fillZeros(bits, 448, 'LE')
        
        print ("*** Padding the definition so the length will be a multiple of 512 bits ***")
        engine.say("Padding the definition so the length will be a multiple of 512 bits")
        engine.runAndWait()
        sleep(2)
        print ("*** Padding the message | part 1 = appending '0' bits ***")
        sleep(2)
        print (bits)
        sleep(2)
        bits = bits + message_len
        print ("*** Padding the message | part 2 = appending original message length as 64-bit big-endian integer ***")
        sleep(2)
        print (bits)
        sleep(2)
        print ("*** New message length is: ***")
        sleep(2)
        progressive_print(str(len(bits)))
        sleep(2)
        return [bits]
    elif 448 <= length <= 512:
        bits.append(1)
        print("*** Appending a single '1' bit at the end ***")
        engine.say("Appending a single '1' bit at the end")
        engine.runAndWait()
        
        sleep(2)
        print(str(bits))
        sleep(2)
        bits = fillZeros(bits, 1024, 'LE')
        bits[-64:] = message_len
        return chunker(bits, 512)
    else:
        bits.append(1)
        print("*** Appending a single '1' bit at the end ***")
        engine.say("Appending a single '1' bit at the end")
        engine.runAndWait()
        sleep(2)
        print(str(bits))
        sleep(2)
        while (len(bits)+64) % 512 != 0:
            bits.append(0)
        bits = bits + message_len
        return chunker(bits, 512)

def initializer(values):
    binaries = [bin(int(v, 16))[2:] for v in values]
    words = []
    for binary in binaries:
        word = []
        for b in binary:
            word.append(int(b))
        words.append(fillZeros(word, 32, 'BE'))
    return words

def b2Tob16(value):
    value = ''.join([str(x) for x in value])
    binaries = []
    clean_binaries = ' '.join(binaries)
    print("binaries:")
    for d in range(0, len(value), 4):
        binaries.append(value[d:d+4])
        hexes = ''
        clean_binaries = ' '.join(binaries)
        print (f"{MAGENTA_BACKGROUND}{clean_binaries}{RESET}")
    print("hexadecimal:")
    for b in binaries:
        hexes += hex(int(b ,2))[2:]
        print(f"{BLUE}{CYAN_BACKGROUND}{hexes}{RESET}")
    return hexes
    
# main function:
#@snoop(depth=3) #use snoop if we want to show all the execution of code
def sha256(message): 
    x=1
    k = initializer(K)
    sleep(2)
    h0, h1, h2, h3, h4, h5, h6, h7 = initializer(h_hex)
    chunks = preprocessMessage(message)
    # only if the number of 512 bits parts is 16, the message is preprocessed:
    if chunker == 16:
        print("The number of 512 bits parts is 16, now the definition is preprocessed")
    for chunk in chunks:
        w = chunker(chunk, 32)
        for _ in range(48):
            w.append(32 * [0])
        for i in range(16, 64):
            s0 = XORXOR(rotr(w[i-15], 7), rotr(w[i-15], 18), shr(w[i-15], 3) ) 
            s1 = XORXOR(rotr(w[i-2], 17), rotr(w[i-2], 19), shr(w[i-2], 10))
            w[i] = add(add(add(w[i-16], s0), w[i-7]), s1)
        
        # Initialize working variables to current hash value:
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
        f = h5
        g = h6
        h = h7
        
        print("...updating the working variables...")
        engine.say("updating the working variables, please wait...")
        engine.runAndWait()
        
        #compression function:
        for j in range(64):
            S1 = XORXOR(rotr(e, 6), rotr(e, 11), rotr(e, 25) )
            ch = XOR(AND(e, f), AND(NOT(e), g))
            temp1 = add(add(add(add(h, S1), ch), k[j]), w[j])
            S0 = XORXOR(rotr(a, 2), rotr(a, 13), rotr(a, 22))
            m = XORXOR(AND(a, b), AND(a, c), AND(b, c))
            temp2 = add(S0, m)
            
            # update the workign variables:
            h = g
            g = f
            f = e
            e = add(d, temp1)
            d = c
            c = b
            b = a
            a = add(temp1, temp2)
            
        a_hex = [hex(x)[2:].zfill(8) for x in a]
        b_hex = [hex(x)[2:].zfill(8) for x in b]
        c_hex = [hex(x)[2:].zfill(8) for x in c]
        d_hex = [hex(x)[2:].zfill(8) for x in d]
        e_hex = [hex(x)[2:].zfill(8) for x in e]
        f_hex = [hex(x)[2:].zfill(8) for x in f]
        g_hex = [hex(x)[2:].zfill(8) for x in g]
        h1_hex = [hex(x)[2:].zfill(8) for x in h]

        #print(f"Round {i + 1} - a: {a_hex}, b: {b_hex}, c: {c_hex}, d: {d_hex}, e: {e_hex}, f: {f_hex}, g: {g_hex}, h: {h1_hex}")

        # Adding the compressed chunk to the current hash value:
        print(" *** Adding the compressed chunk to the current hash value ***")
        engine.setProperty('rate', 140)
        engine.setProperty('voice', voices[10].id)
        engine.say("Adding the compressed chunk to the current hash value")
        engine.runAndWait()
        
        h0 = add(h0, a)
        h1 = add(h1, b)
        h2 = add(h2, c)
        h3 = add(h3, d)
        h4 = add(h4, e)
        h5 = add(h5, f)
        h6 = add(h6, g)
        h7 = add(h7, h)
    digest = ''
   
    send_to_esp32 ("...processing...", ESP32_oled_display)
   # Produce the final hash value 
    for val in [h0, h1, h2, h3, h4, h5, h6, h7]:
        print("producing the final hash value")
        engine.setProperty('voice', voices[random.choice([0,10])].id)
        engine.say("Producing the final hash value")
        engine.runAndWait()
        engine.setProperty('voice', voices[10].id)
        digest += b2Tob16(val)
    return digest

if __name__ == '__main__':
    #logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p', filename='hash_breakdown.log', level=logging.INFO)
    #logger.info('Logging started')
    print ("*** Initializing HASH BREAKDOWN ***")
    send_to_esp32 ("hello world", ESP32_oled_display) #debugging purpose
    sleep(1)
    print ("*** Initializing HASH BREAKDOWN ***")
    sleep(1)
    print ("*** Initializing HASH BREAKDOWN ***")
    sleep(1)
    online_database = []  # ??? preco to nemam mat vo While True cykle ?
    while True:
        
        try:
            
            try:
                #logger.info('Starting')
                online_database = parse_definitions()
            except Exception as e:
                print('Exception ocurred', e) 
                #traceback.print_exc() # prints the error details

            #print ("Found", len(online_database), "results")
            if len(online_database) == 0:
                print ("Using the parsed database.")
                #logger.info('Accessing offline database')
                random.shuffle(database_feminism) # we randomly change the order of the offline database definitions
                online_database = database_feminism[:OFF_DB_LIMIT]

            try:     
                counter = 0
                for input_message in online_database:
                    counter+=1
                    print ("*** Initializing HASH BREAKDOWN ***")
                    #send_to_esp32("hello", ESP32_oled_display)
                    sleep(1)
                    print ("*** Initializing HASH BREAKDOWN ***")
                    sleep(1)
                    print ("*** Initializing HASH BREAKDOWN ***")
                    sleep(1)
                    #logger.info('Starting the hashing process')
                    #print('Definition Nr.'+str(counter)+': ', input_message)
                    hash_result = sha256(input_message)
                    print('Hash:'+hash_result)
                    format_hash_result = ', '.join(hash_result)
                    engine.setProperty('rate', 140)
                    engine.setProperty('voice', voices[10].id)
                    engine.say("The final hash is:"+format_hash_result+".")
                    engine.runAndWait()
                    engine.say("While the hashing process normally takes milliseconds, this was a detailed breakdown of the SHA-256 hashing algorithm. Thank you for your attention. Lets start again with another definition to hash.")
                    print("While the hashing process normally takes milliseconds, this was a detailed breakdown of the SHA-256 hashing algorithm. Thank you for your attention. Lets start again with another definition to hash.")
                    engine.runAndWait() 
                    #logger.info('Ending hashing process')
                  
            except Exception as e:
                print('Exception ocurred', e) 
                #traceback.print_exc() # prints the error details, uncomment for debugging
                continue

        except KeyboardInterrupt:
            print ("\nProcess was interrupted by user. Ending ...")
            #logger.info('Process interrupted by user')
            break 
        
        except BaseException:
            #traceback.print_exc() # prints the error details, uncomment for debugging
            continue