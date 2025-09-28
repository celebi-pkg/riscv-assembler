import pytest
from pathlib import Path
from os.path import exists
from riscv_assembler.convert import AssemblyConverter as AC
from riscv_assembler.instr_arr import *
from riscv_assembler.parse import Parser

num_test_files = 9
num_questions = 15

def SUITE():
	# 0. convert directly from file to array
	# 1. convert directly from file to print (return nothing)
	# 2. convert directly from file to txt file
	# 3. convert directly from file to bin file
	#----
	# 4. convert contents from string to array
	# 5. convert contents from string to print (return nothing)
	# 6. convert contents from string to txt file
	# 7. convert contents from string to bin file
	#----
	# 8. convert contents from string array to array
	# 9. convert contents from string array to print (return nothing)
	# 10. convert contents from string array to txt file
	# 11. convert contents from string array to bin file

	dump_path = str(Path(__file__).parent / "dump")
	paths = [str(Path(__file__).parent / "assembly/test{}.s".format(i)) for i in range(num_test_files)]

	results = {i: [] for i in range(num_questions)}
	for i, path in enumerate(paths):
		# 1.
		cnv = AC(hex_mode = True, output_mode = 'a')
		results[0] += [cnv(path)] #**
		# 2.
		cnv.output_mode = 'p'
		results[1] += [cnv(path)]
		# 3. 
		cnv.output_mode = 'f'
		cnv(path, dump_path + '/file{}.txt'.format(i))
		results[2] += ['file{}.txt'.format(i)] #**
		# 4. 
		cnv(path, dump_path + '/file{}.bin'.format(i))
		results[3] += ['file{}.bin'.format(i)] #**

		with open(path) as f:
			code = [elem for elem in f.readlines() if len(elem.strip()) > 0]
		str_code = ''.join(code)

		# 5.
		cnv.output_mode = 'a'
		results[4] += [cnv(str_code)] #**
		# 6.
		cnv.output_mode = 'p'
		results[5] += [cnv(str_code)]
		# 7. 
		cnv.output_mode = 'f'
		cnv(str_code, dump_path + '/str{}.txt'.format(i))
		results[6] += ['str{}.txt'.format(i)] #**
		# 8.
		cnv(str_code, dump_path + '/str{}.bin'.format(i))
		results[7] += ['str{}.bin'.format(i)] #**

		code = [e.strip() for e in code]
		# 9.
		cnv.output_mode = 'a'
		results[8] += [cnv(code)] #**
		results[9] += [cnv.output_mode]
		# 10.
		cnv.output_mode = 'p'
		results[10] += [cnv(code)]
		results[11] += [cnv.output_mode]
		# 11. 
		cnv.output_mode = 'f'
		cnv(code, dump_path + '/arr{}.txt'.format(i))
		results[12] += ['arr{}.txt'.format(i)] #**
		
		# 12.
		cnv(code, dump_path + '/arr{}.bin'.format(i))
		results[13] += ['arr{}.bin'.format(i)] #**
		results[14] += [cnv.output_mode]

	return results

ans = ['0xfe810113','0x00812023','0x00912223','0x01212423','0x01312623','0x01412823','0x01512a23','0x00100f13','0x01e64863','0x01e6ca63','0x01e74863','0x0140006f','0x00500593','0xfcdff06f','0x00600593','0xfc5ff06f','0x00000413','0x00000293','0x00000313','0x00000393','0x00400e13','0x03c68a33','0x03c70ab3','0x0040006f','0x02c28263','0x00052483','0x0005a903','0x01450533','0x015585b3','0x032489b3','0x01340433','0x00128293','0xfe1ff06f','0x00040513','0x00012403','0x00412483','0x00812903','0x00c12983','0x01012a03','0x01412a83','0x01810113']
ANSWERS = {
	0: [['0x000000b3'], None, 'file0.txt', 'file0.bin', ['0x000000b3'], None, 'str0.txt', 'str0.bin', ['0x000000b3'], 'a', None, 'p', 'arr0.txt', 'arr0.bin', 'f'],
	1: [['0x02040293'], None, 'file1.txt', 'file1.bin',['0x02040293'], None, 'str1.txt', 'str1.bin',['0x02040293'], 'a', None, 'p', 'arr1.txt', 'arr1.bin', 'f'],
	2: [['0x00a00413', '0x00a00493', '0x00848263', '0xfe040493'], None, 'file2.txt', 'file2.bin', ['0x00a00413', '0x00a00493', '0x00848263', '0xfe040493'], None, 'str2.txt', 'str2.bin', ['0x00a00413', '0x00a00493', '0x00848263', '0xfe040493'], 'a', None, 'p', 'arr2.txt', 'arr2.bin', 'f'],
	3: [['0x00812023', '0x06532223', '0xec532a23','0xfe532fa3','0x7e532fa3','0x004302e7','0x00430293'], None, 'file3.txt', 'file3.bin', ['0x00812023', '0x06532223', '0xec532a23','0xfe532fa3','0x7e532fa3','0x004302e7','0x00430293'], None, 'str3.txt', 'str3.bin', ['0x00812023', '0x06532223', '0xec532a23','0xfe532fa3', '0x7e532fa3','0x004302e7','0x00430293'], 'a', None, 'p', 'arr3.txt', 'arr3.bin', 'f'],
	4: [['0x000000b3', '0x02040293', '0x02040293','0x00812023'], None, 'file4.txt', 'file4.bin',['0x000000b3', '0x02040293', '0x02040293','0x00812023'], None, 'str4.txt', 'str4.bin',['0x000000b3', '0x02040293', '0x02040293','0x00812023'], 'a', None, 'p', 'arr4.txt', 'arr4.bin', 'f'],
	5: [['0x00a00413','0x00a00493','0xfff00493','0x00048463','0xfe000ce3','0xfe040493'], None, 'file5.txt', 'file5.bin', ['0x00a00413','0x00a00493','0xfff00493','0x00048463','0xfe000ce3','0xfe040493'], None, 'str5.txt', 'str5.bin', ['0x00a00413','0x00a00493','0xfff00493','0x00048463','0xfe000ce3','0xfe040493'], 'a', None, 'p', 'arr5.txt', 'arr5.bin', 'f'],
	6: [['0x00a00093','0xfec00113','0x00000663','0x00123023','0x00023083','0xfff00093','0x00123023','0x00023083','0xfe02c6e3'], None, 'file6.txt', 'file6.bin', ['0x00a00093','0xfec00113','0x00000663','0x00123023','0x00023083','0xfff00093','0x00123023','0x00023083','0xfe02c6e3'], None, 'str6.txt', 'str6.bin', ['0x00a00093','0xfec00113','0x00000663','0x00123023','0x00023083','0xfff00093','0x00123023','0x00023083','0xfe02c6e3'], 'a', None, 'p', 'arr6.txt', 'arr6.bin', 'f'],
	7: [['0x00318233','0x002080b3','0x00708093','0x00123023','0x00023083'], None, 'file7.txt', 'file7.bin', ['0x00318233','0x002080b3','0x00708093','0x00123023','0x00023083'], None, 'str7.txt', 'str7.bin', ['0x00318233','0x002080b3','0x00708093','0x00123023','0x00023083'], 'a', None, 'p', 'arr7.txt', 'arr7.bin', 'f'],
	8: [ans, None, 'file8.txt', 'file8.bin', ans, None, 'str8.txt', 'str8.bin', ans, 'a', None, 'p', 'arr8.txt', 'arr8.bin', 'f']}

RESULTS = SUITE()

def error_label(q, test):
	return "Question {q} Failed for Test {test}".format(q = q, test = test)
test_data = []
for q in range(num_questions):
	for t in range(num_test_files):
		test_data += [(q, t)]
@pytest.mark.parametrize("q, test", test_data)
def test_compute(q: int, test: int):
	assert RESULTS[q][test] == ANSWERS[test][q], error_label(q, test)