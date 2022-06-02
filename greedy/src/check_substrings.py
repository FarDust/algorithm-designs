# si la suma de substrings es divisible en 3 -> el substring es divisible en 3

# Basandose en https://www.geeksforgeeks.org/count-sub-arrays-sum-divisible-k/


def calc_substrings(string):

    k = 3
    result = 0
    cumulative_sum = 0
    frequency_count = [0] * (k + 1)

    for number in string:
        cumulative_sum += int(number)
        frequency_count[cumulative_sum % k] += 1

    for count in frequency_count:

        if count > 1:
            result += (count * (count - 1)) // 2

    result += frequency_count[0]

    return result


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "-t":
        from random import randint

        input_string = "".join([str(randint(0, 9)) for i in range(int(1e5))])
    else:
        input_string = input()
    print(calc_substrings(input_string))
