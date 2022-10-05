import sys,os
sys.path.insert(1, "./build")
import timing_example

import time
import matplotlib.pyplot as plt





def basic_operation(i, j):
    sum = 0;
    for l in range(0,i):
        sum = sum + j
    return sum;



def comparaison(i,j, rank = 0):
	sum = 0
	py_time = 0
	cpp_time = 0
	mpi_time = 0

	if(rank == 0):
		start_time = time.time()
		sum = basic_operation(i, j)
		py_time = time.time() - start_time
		print("result :", sum, "python time",py_time)

	if(rank == 0):
		start_time = time.time()
		sum = timing_example.basic_operation(i, j)
		cpp_time = time.time() - start_time
		print("result :", sum, "c++ time",cpp_time)

	if(1):
		start_time = time.time()
		sum = timing_example.mpi_basic_operation(i, j)
		mpi_time = time.time() - start_time
		print("result :", sum, "mpi time",mpi_time)


	return py_time, cpp_time, mpi_time


timing_example.mpi_init()


rank = timing_example.mpi_rank()

py_times = []
cpp_times = []
mpi_times = []
iterations = [pow(10,i) for i in range(1,8)]
for n in iterations:
	print("_________", n)
	py_time, cpp_time, mpi_time = comparaison(n, 2, rank)

	py_times.append(py_time)
	cpp_times.append(cpp_time)
	mpi_times.append(mpi_time)


plt.plot(iterations, py_times, label = "python")
plt.plot(iterations, cpp_times, label = "cpp")
plt.plot(iterations, mpi_times, label = "mpi")
plt.xlabel("number of operations")
plt.ylabel("time")
plt.legend();
plt.savefig('./test.png')

plt.clf()

plt.plot(iterations, cpp_times, label = "cpp")
plt.plot(iterations, mpi_times, label = "mpi")
plt.xlabel("number of operations")
plt.ylabel("time")
plt.legend();
plt.savefig('./test2.png')


timing_example.mpi_finalize()


