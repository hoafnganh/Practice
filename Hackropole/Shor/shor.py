# Homemade RSA key generation for this challenge,
# but you don't need to know the details to solve.
import rsa

# you don't have access to the implementation details of our quantum computer
import quantum_computer

def challenge(choice):
    assert choice in [1, 2]

    print("Generating RSA key ...")
    e = 2 ** 16 + 1
    n, p, q, iq, dp, dq, d = rsa.keygen(1024, e)

    print("Here is the public modulus:")
    print(f"n = {int(n)}")

    if choice == 1:
        base = 3
        c = quantum_computer.QFT(n)
    else:
        base, c = quantum_computer.QFTrevenge(n)

    print("Here is the output of the quantum computer:")
    print(f"{base=}")
    print(f"{c=}")

    print("Please provide any non-trivial factor of the public modulus:")

    factor = int(input(">>> "))
    if factor == p or factor == q:
        print("Congrats! Here is the flag:")
        if choice == 1:
            print(open("flag.txt").read())
        if choice == 2:
            print(open("flag_revenge.txt").read())
    else:
        print("Nope!")

if __name__ == "__main__":
    try:
        while True:
            print("Which flag do you want to grab?")
            print("  0. Quit.")
            print("  1. Shor - fixed base.")
            print("  2. Shor Revenge - random base.")
            choice = int(input(">>> "))

            if choice == 0: break
            elif choice == 1: challenge(1)
            elif choice == 2: challenge(2)
    except:
        print("Please check your inputs.")
