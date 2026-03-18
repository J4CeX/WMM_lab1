import sys
import ex1


def main(excercise_number):
    if excercise_number == 0:
        print(0)
    elif excercise_number == 1:
        ex1.excercise_one()
    else:
        print("none")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        main(sys.argv[0])
    elif len(sys.argv) == 0:
        main()
