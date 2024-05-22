def max_subarray_sum_circular(nums):
    def kadane(array):
        current_sum = max_sum = array[0]
        for num in array[1:]:
            current_sum = max(num, current_sum + num)
            max_sum = max(max_sum, current_sum)
        return max_sum

    max_kadane = kadane(nums)
    if max_kadane < 0:
        return 0

    total_sum = sum(nums)
    min_kadane = kadane([-num for num in nums])
    max_wrap = total_sum + min_kadane

    return max(max_kadane, max_wrap)


if __name__ == '__main__':
    n_cases = int(input().strip())

    for case in range(n_cases):
        values = list(map(int, input().strip().split(' ')))[1:]

        # print(values)
        # find_max_gain(values)
        max_gain = max_subarray_sum_circular(values)
        print(max_gain)

