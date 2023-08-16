# import filecmp
# import os
# from pathlib import Path
#
# DEV_OUT_DIR = 'scratch'
#
#
# verified_dir = Path().absolute() / Path('FILES') / Path('verified_results')
# verified = os.listdir(verified_dir)
#
#
# def check_results(check_dir):
# 	all_match = True
#
# 	for name in verified:
# 		v = Path(verified_dir) / Path(name)
# 		c = Path(check_dir) / Path(name)
# 		match = filecmp.cmp(v, c)
# 		if not match:
# 			all_match = False
# 			print('Mismatch between final results files: ', v, ' ', c)
#
# 	if all_match:
# 		print('All analyzed annotations and logs match verified output')
#
# # -----------------------------------------------------------------------------
# #
#
# #if __name__ == '__main__':
# #	check_results('2022_05_10_14-01-20')