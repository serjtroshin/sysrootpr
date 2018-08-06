import numpy as np
with open("out.txt", "r") as f:
    vectors = list(map(lambda x: np.array(list(map(int, x.split(',')))), f.readlines()))
f.close()
unique_vectors = np.unique(vectors, axis=0)
print(len(vectors), len(unique_vectors))
with open("f4_characteristic_set.txt", "w") as f:
    for i in unique_vectors:
        f.write(",".join(map(str, list(i))) + '\n')
f.close()

