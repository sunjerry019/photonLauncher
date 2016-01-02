from mpi4py import MPI


comm =  MPI.COMM_WORLD
rank =  comm.Get_rank()
name = MPI.Get_processor_name()
print rank

if rank == 0:
	data = {1: 2, 3:4}
#	print data
	comm.send(data, dest = 1, tag = 0)
#	print data
if rank == 1:
	data = comm.recv(source = 0, tag = 0)
	print data
