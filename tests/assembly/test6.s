addi x1 x0 10
addi x2 x0 -20

beq x0 x0 loop

out:
	sd x1, 0(x4)
	ld x1, 0(x4)

loop:
	addi x1 x0 -1
	sd x1, 0(x4)
	ld x1, 0(x4)
	blt x5 x0 out
