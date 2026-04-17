def searchInsert(nums: list[int], target: int) -> int:
    left = 0
    right = len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        print(nums[left:right + 1])
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
        
    return left


print(f"res: >>>> {searchInsert([1,3,5,6], 0)}")

