#Euclidean
#Saayoan Navaneethan 

#%%
def A5Q1(a,start=None,stop=None,step=1):
    return a[start:stop:step]
#%% 
def A5Q2 (a,b):
    set_a = set(a)
    set_b = set(b)
    
    common = set_a.intersection(set_b)  
    difference_1 = set_a.difference(set_b) 
    difference_2 = set_b.difference(set_a)
    both_difference = difference_2.union(difference_1)
    return (common,both_difference)
#%%
def A5Q3(a, b=1, c=5):
    ans1 = (-b + (b ** 2 - 4 * a * c) ** 0.5) / (2 * a) 
    ans2 = (-b - (b ** 2 - 4 * a * c) ** 0.5) / (2 * a)  
    return ans1, ans2

    
#%%
def A5Q4(a,b):
    try: 
        result = a * b 
        return result 
    except: 
        result = TypeError
        return None 
#%%

def A5Q5(*args):
    if (1<len(args)<4):
        result = 1 
        for number in args: 
            result *= number
            
    return result 
#%%
def A5Q6(a, b, c=0):
    """
    Calculates the Euclidean distance from the origin to the point (a, b, c) in 2D or 3D space.

    Parameters:
    a (float): The x-coordinate.
    b (float): The y-coordinate.
    c (float, optional): The z-coordinate. Default is 0, making it a 2D calculation if omitted.

    Returns:
    float: The Euclidean distance from the origin to the point (a, b, c).
    """
    hypt = (a**2 + b**2 + c**2) ** 0.5
    return hypt

#%%

