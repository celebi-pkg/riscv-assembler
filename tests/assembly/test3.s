sw s0, 0(sp)
sw x5, 100(x6)
sw x5, -300(x6)
sw x5, -1(x6)
sw x5, 2047(x6)
jalr x5, x6, 4
addi x5, x6, 4