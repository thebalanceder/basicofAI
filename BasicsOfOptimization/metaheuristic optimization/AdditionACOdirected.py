import numpy as np

distances=np.array([[0,2,3],
                    [2,0,4],
                    [3,4,0]])

new_size=distances.shape[0]+1
newdistances=np.zeros((new_size,new_size))
newdistances[:distances.shape[0],:distances.shape[1]]=distances
newdistances[-1,:-1]=[2,5,6]
newdistances[:-1,-1]=[6,5,2]

print(newdistances)
