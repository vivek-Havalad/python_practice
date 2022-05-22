def FindGcd(a, b): 
    if (b == 0): 
        return a
    return FindGcd(b, a % b) 

def TheSubArray(arr, n): 
    subArrayLen = -1
    for i in range(n - 1): 
        for j in range(n): 
            lcm = 1 * arr[i] 
            res = 1 * arr[i] 
            for x in range(i + 1, j + 1): 
                lcm = ((arr[x] * lcm) / FindGcd(arr[x], lcm)) 
                res = res * arr[x] 
            if (lcm == res):
                subArrayLen = max(subArrayLen, j - i + 1) 
    return subArrayLen

if __name__ == "__main__":
    max_val = 0
    arr = [[7, 2], [2,2,3,4], [2,2,4]]
    for x in range(len(arr)): 
        x_arr = arr[x]
        n = len(x_arr)
        res = TheSubArray(x_arr, n)
        print(res)
        if max_val < res:
            max_val = res
    print(max_val) 