## @package twitter
import argparse

from control_center.control_center import Control_Center
from control_center.text_generator import test as ola


def main():
	control_center = Control_Center()
	control_center.run()
	control_center.close()


def tests(test_type):
	if test_type == "text_generator":
		ola()


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--test', type=str, default='')
	args = parser.parse_args()

	if args.test:
		tests(args.test)
	else:
		main()
