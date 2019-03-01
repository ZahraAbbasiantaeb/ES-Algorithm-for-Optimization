import numpy as np
import matplotlib.pyplot as plt
from question1.mutation2.ES_Algorithm import ES

child = [50,100,200,300,400,500,600]

for i in range(0,7):
    test = ES (100, 100, np.repeat(-2,100), np.repeat(2,100), 100, child[i], 800)
    result = test.run()
    string = "child: "+ str(child[i])
    plt.plot(result, label=string)

plt.xlabel("iteration")
plt.ylabel("Error")
plt.legend(loc='upper left')
plt.show()
