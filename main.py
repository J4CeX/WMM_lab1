import sys
import ex1


def main(exercise_number):
    if exercise_number == 0:
        print(0)
    elif exercise_number == 1:
        ex1.exercise_one()
    else:
        print("none")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        main(sys.argv[0])
    elif len(sys.argv) == 0:
        main()
