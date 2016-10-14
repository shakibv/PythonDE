### PythonDE
Differential evolution optimization (DE)
<br/><br/>
**Table of Contents**
* [To Use](#to-use)  
* [Example Usage](#example-usages-normal-mode)
  * [Normal Mode](#example-usages-normal-mode)  
  * [Coroutine Mode](#coroutine-mode)
  * [Generator Mode](#generator-mode)
* [References](#references)  

To Use
------

To clone and run this repository you'll need [Git](https://git-scm.com) installed on your computer. From your command line:

```bash
# Clone this repository
git clone https://github.com/shakibv/PythonDE
# Go into the repository
cd PythonDE
# Install the package
python setup.py install --user
```
Example Usages: Normal Mode
---------------------------

A simple example showing how **PythonDE** can be utilized to minimze the **Goldstein-Price** function. The true global minimum is at `(x,y) = (0, -1)` where `f(x,y) = 3`:
```python
from pythonde import DEvolution

def GoldsteinPrice(x):
    return (1+(x[0]+x[1]+1)**2*(19-14*x[0]+3*x[0]**2-14*x[1]+6*x[0]*x[1]+3*x[1]**2))* \
           (30+(2*x[0]-3*x[1])**2*(18-32*x[0]+12*x[0]**2+48*x[1]-36*x[0]*x[1]+27*x[1]**2))

maxGen, nPopulation, bounds = 100, 50, [[-2,2],[-2,2]]
DE = DEvolution(GoldsteinPrice, bounds, nPopulation)
MinPoint, MinValue = DE.Optimize(maxGen)

print(MinPoint, MinValue)
#[  1.24805183e-09  -1.00000000e+00] 3.0
```
Now let's walk through each section of the code. We start off with importing the class from the package:
```python
from pythonde import DEvolution
```
Then we define the objective function to be minimized. In this case the **Goldstein-Price** function:
```python
def GoldsteinPrice(x):
    return (1+(x[0]+x[1]+1)**2*(19-14*x[0]+3*x[0]**2-14*x[1]+6*x[0]*x[1]+3*x[1]**2))* \
           (30+(2*x[0]-3*x[1])**2*(18-32*x[0]+12*x[0]**2+48*x[1]-36*x[0]*x[1]+27*x[1]**2))
```
Next we have to specify the limits of the input parameters that the optimizer is allowed to search within (`bounds`), the size of population (`nPopulation`) and the maximum number of generations allowed (`maxGen`). For the sake of clarity, we have defined them prior to calling the optimizer. In this example the bounds on the input parameters are `-2 ≤ x,y ≤ 2` and are passed using the `bounds = [[-2,2],[-2,2]]` variable:
```python
maxGen, nPopulation, bounds = 100, 50, [[-2,2],[-2,2]]
```
Now we can create a `DEvolution` instance and run the optimizer for `maxGen` generations:
```python
DE = DEvolution(GoldsteinPrice, bounds, nPopulation)
MinPoint, MinValue = DE.Optimize(maxGen)

print(MinPoint, MinValue)
```
Finaly, to access the best-fit solution found by the algorithm we can simply access the two variables `MinPoint` and `MinValue`.

Coroutine Mode
--------------

This mode is used in the case that the **Fitness Function** is provided from an external source to the **Differential Evolution** algorithm. For example, from an experimental setup or an external function. A simple example showing how **PythonDE** can be used as a **coroutine** to minimze an **external fitness function** is provided here. The true global minimum is at `(x,y) = (1, 1)` where `f(x,y) = 0`:
```python
from pythonde import DEvolution

def fitness_func(x):
    error = (1 - x[0]) ** 2 + 100 * (x[1] - x[0] ** 2) ** 2
    return error

maxGen, nPopulation, bounds = 100, 50, [[-5,6],[-5,6]]
DE = DEvolution(None, bounds, nPopulation)
coDE = DE();

param = next(coDE)
for i in range(maxGen * nPopulation):
    param = coDE.send(fitness_func(param))
coDE.close()

print(DE.MinimumPoint, DE.MinimumValue)
#[ 1.00000113  1.00000246] 5.57046840346e-12
```
Now let's walk through each section of the code. To start using `PythonDE` as a **coroutine** we start off with importing the class from the package:
```python
from pythonde import DEvolution
```
Then we define the **external fitness function**. It takes a parameter set and returns the corresponding fitness value:
```python
def fitness_func(x):
    error = (1 - x[0]) ** 2 + 100 * (x[1] - x[0] ** 2) ** 2
    return error
```
Next we have to specify the limits of the input parameters that the optimizer is allowed to search within (`bounds`), the size of population (`nPopulation`) and the maximum number of generations allowed (`maxGen`). In this example the bounds on the input parameters are `-5 ≤ x,y ≤ 6` and are passed using the `bounds = [[-5,6],[-5,6]]` variable:
```python
maxGen, nPopulation, bounds = 100, 50, [[-5,6],[-5,6]]
```
Now we can create a `DEvolution` instance and run the optimizer as a coroutine for arbitrary number of generations. In this example the fitness function is not directly passed to the algorithm. So, the value `None` will be placed instead:
```python
DE = DEvolution(None, bounds, nPopulation)
coDE = DE();

param = next(coDE)
for i in range(maxGen * nPopulation):
    param = coDE.send(fitness_func(param))
coDE.close()

print(DE.MinimumPoint, DE.MinimumValue)
#[ 1.00000113  1.00000246] 5.57046840346e-12
```
Finaly, to access the best-fit solution found by the algorithm we can simply access the two properties `DE.MinimumPoint` and `DE.MinimumValue`.

Generator Mode
--------------

References
----------
Storn, R., Price, K., Journal of Global Optimization 11: 341--359, 1997
