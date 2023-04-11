import pytest
from pathlib import Path
from riscv_assembler.convert import AssemblyConverter as AC
from riscv_assembler.instr_arr import *
from riscv_assembler.parse import Parser
#TESTS


def SUITE(path):
	# 1. convert directly from file to array
	# 2. convert directly from file to print (return nothing)
	# 3. convert directly from file to txt file
	# 4. convert directly from file to bin file
	#----
	# 5. convert contents from string to array
	# 6. convert contents from string to print (return nothing)
	# 7. convert contents from string to txt file
	# 8. convert contents from string to bin file
	#----
	# 5. convert contents from string array to array
	# 6. convert contents from string array to print (return nothing)
	# 7. convert contents from string array to txt file
	# 8. convert contents from string array to bin file

	dump_path = str(Path(__file__).parent / "dump/")
	paths = [str(Path(__file__).parent / "assembly/test{}.s".format(i)) for i in range(7)]

	results = []
	for i, path in enumerate(paths):
		cnv = AC(hex_mode = True, output_mode = 'a')
		results += [cnv(path)]
		cnv.output_mode = 'p'
		cnv(path)
		cnv.output_mode = 'f'
		cnv(path, dump_path + 'file{i}.txt'.format(i))
		results += ['file{i}.txt'.format(i)]
		cnv(path, dump_path + 'file{i}.bin'.format(i))
		results += ['file{i}.bin'.format(i)]

		with open(path) as f:
			code = f.readlines()


#test simple.s file, writes to txt and bin
def func0():
	#test convert, should return array
	cnv = AC()

	path = str(Path(__file__).parent / "assembly/test0.s")
	return cnv(path)

def func1():
	#test convert
	cnv = AC()

	path = str(Path(__file__).parent / "assembly/test1.s")
	return cnv(path)

def func2():
	#test get/set OutpuType
	outarr = []
	cnv = AC()

	outarr += [cnv.output_mode]
	cnv.output_mode = 'p'
	cnv.output_mode = 'f'
	outarr += [cnv.output_mode]

	return outarr

def func4():
	#test nibble form for convert
	cnv = AC(nibble_mode = True)

	path = str(Path(__file__).parent / "assembly/test0.s")
	return cnv(path)

def func5():
	#test nibbleForm for convert
	cnv = AC(nibble_mode = True)

	path = str(Path(__file__).parent / "assembly/test1.s")
	return cnv(path)

def func6():
	# test clone

	cnv = AC(output_mode = 'p', nibble_mode = True, hex_mode = True)

	cnv2 = cnv.clone()

	return [cnv2.output_mode, cnv2.nibble_mode, cnv2.hex_mode]

def func7():
	#test calcJump()
	path = str(Path(__file__).parent / "assembly/test2.s")

	code = Parser.read_file(path)
	return Ip.JUMP('loop', 2, code)

def func8():
	#test hex
	out_arr = []
	cnv = AC(hex_mode = True)

	path = str(Path(__file__).parent / "assembly/test0.s")
	out_arr += cnv(path)

	path = str(Path(__file__).parent / "assembly/test1.s")
	out_arr += cnv(path)

	return out_arr

def func9():
	# test tokenizer
	line = "add x0 x0 x1"

	result = Parser.tokenize(line)

	return result

def func10():
	line = "add x0 x0 x1"
	tokens = Parser.tokenize(line)

	return str(Parser.determine_type(tokens[0]))

def func11():
	line = ""
	tokens = Parser.tokenize(line)

	return tokens

def func12():
	cnv = AC(hex_mode = True, output_mode='a')

	path = str(Path(__file__).parent / "assembly/test2.s")

	return cnv(path)

def func13():
	cnv = AC(hex_mode = True, output_mode='a')

	path = str(Path(__file__).parent / "assembly/test3.s")

	return cnv(path)

def func14():
	cnv = AC(hex_mode = True, output_mode='a')

	instr = 'add x1 x0 x0\naddi t0 s0 32\naddi t0 s0 32\nsw s0, 0(sp)'

	return cnv(instr)

def func15():
	cnv = AC(hex_mode = True, output_mode = 'a')

	instr = "add x4, x3, x3\nadd x1, x1, x2\naddi x1, x1, 7\nsd x1, 0(x4)\nld x1, 0(x4)"

	return cnv(instr)

def func16():
	cnv = AC(hex_mode = True, output_mode = 'a')

	path = str(Path(__file__).parent / "assembly/test5.s")

	return cnv(path)

#-----------------------------------------------------------------------------------------		
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------


def test_0():
	assert func0() == ['00000000000000000000000010110011'], "Test 0 Failed"

def test_1():
	assert func1() == ['00000010000001000000001010010011'], "Test 1 Failed"

def test_2():
	assert func2() == ["a", "f"], "Test 2 Failed"

def test_4():
	assert func4() == ['0000\t0000\t0000\t0000\t0000\t0000\t1011\t0011'], "Test 4 Failed"

def test_5():
	assert func5() == ['0000\t0010\t0000\t0100\t0000\t0010\t1001\t0011'], "Test 5 Failed"

def test_6():
	assert func6() == ['p', True, True], "Test 6 Failed"

def test_7():
	assert func7() == 4

def test_8():
	assert func8() == ['0x000000b3', '0x02040293'], "Test 8 Failed"

def test_9():
	assert func9() == ['add', 'x0', 'x0', 'x1'], "Test 9 Failed"

def test_10():
	assert func10() == 'R Parser', "Test 10 Failed"

def test_11():
	assert func11() == []

# Test file test2.s, need to implement JUMP
def test_12():
	assert func12() == ['0x00a00413', '0x00a00493', '0x00848263', '0xfe040493']

def test_13():
	assert func13() == ['0x00812023']

def test_14():
	assert func14() == ['0x000000b3', '0x02040293', '0x02040293','0x00812023']

def test_15():
	assert func15() == ['0x00318233', '0x002080b3','0x00708093','0x00123023', '0x00023083']

def test_16():
	assert func16() == ['0x00a00413','0x00a00493','0xfff00493', 
	'0x00048463', '0xfe000ce3', '0xfe040493']