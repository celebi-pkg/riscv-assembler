addi s0 x0 10
addi s1 x0 10

loop:
	addi s1 x0 -1
	beq s1 x0 out
	beq x0 x0 loop

out:
	addi s1 s0 -32