from mpi4py import MPI


comm =  MPI.COMM_WORLD
rank =  comm.Get_rank()

print rank

if rank == 0:
	comm.send("dfdfdfdfdfdfdfdfdfdfdfa", dest = 1, tag = 0)
if rank == 1:
	print comm.recv(source = 0, tag = 0)

