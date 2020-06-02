#!/usr/bin/python

import random
import string

def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def main():
    f = open("largeFile.txt", "w")
    for i in range(1,2000000):
        if (i%2) == 0:
            f.write('\n')
        f.write(randomString(random.randint(1,13)))

    f.close()

if __name__ == "__main__":
    main()
