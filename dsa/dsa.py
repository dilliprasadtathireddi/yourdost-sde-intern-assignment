def second_largest_element(arr):
    max_val = arr[0]
    second_largest = -1
    for i in range(1, len(arr)):
        if arr[i] > max_val:
            second_largest = max_val
            max_val = arr[i]
        if arr[i] > second_largest and arr[i] < max_val:
            second_largest = arr[i]
    return second_largest

arr = list(map(int, input().split()))
result = second_largest_element(arr)
print(result)