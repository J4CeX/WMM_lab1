import sys
import ex1a
import ex1b


def main(excercise_number):
    if excercise_number == 0:
        print(0)
    elif excercise_number == 1:
        ex1a.excercise_one_a()
    elif excercise_number == 2:
        ex1b.excercise_two_b()
    else:
        print("none")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(int(sys.argv[1]))
    elif len(sys.argv) == 0:
        main()
