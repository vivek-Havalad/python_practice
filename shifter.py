class getMaxLen(object):
    def __init__(self):
        self.__n =  100005
        self.__n_max = 1000002
        self.__prime_map = [0 for i in range(self.__n_max + 1)] 
        self.__n_container = [[] for i in range(self.__n)]     
        self.__prime_values = [-1 for i in range(self.__n_max + 1)]
        self.ThePrimeEngine()

    def ThePrimeEngine(self):
        self.__prime_map[0], self.__prime_map[1] = 1, 1
  
        for i in range(2, self.__n_max + 1): 
            if (self.__prime_map[i] == 0): 
                for j in range(i * 2, self.__n_max, i): 
                    if (self.__prime_map[j] == 0): 
                        self.__prime_map[j] = i 
    
    
        for i in range(2, self.__n_max): 
            if (self.__prime_map[i] == 0): 
                self.__prime_map[i] = i
    
    def TheSubArray(self, arr, n):
        for i in range(n): 
            self.__prime_values[i] = -1
  
        for i in range(n): 
            while (arr[i] > 1): 
                p = self.__prime_map[arr[i]] 
                arr[i] //= p 
                self.__n_container[i].append(p) 
        l, r, ans = 0, 1, -1
        for i in self.__n_container[0]: 
            self.__prime_values[i] = 0
    
        while (l <= r and r < n): 
            flag = 0
            for i in range(len(self.__n_container[r])): 
                if (self.__prime_values[self.__n_container[r][i]] == -1 or self.__prime_values[self.__n_container[r][i]] == r): 
                    self.__prime_values[self.__n_container[r][i]] = r 
                else: 
                    flag = 1
                    break
            if (flag):
                for i in self.__n_container[l]: 
                    self.__prime_values[i] = -1
                l += 1
            else : 
                ans = max(ans, r - l + 1) 
                r += 1
        if (ans == 1): 
            ans = -1
    
        return ans

if __name__ == "__main__":
    max_val = 0
    obj = getMaxLen()
    arr = [[7, 2], [2,2,3,4], [2,2,4]]
    for x in range(len(arr)): 
        x_arr = arr[x]
        n = len(x_arr)
        res = obj.TheSubArray(x_arr, n)
        print(res)
        if max_val < res:
            max_val = res
    print(max_val) 