import numpy as np

distances=np.array([[0,1,2],
                    [1,0,3],
                    [2,3,0]])
newdistances=np.delete(distances,2,axis=0)
newdistances=np.delete(distances,2,axis=1)

print(newdistances)
