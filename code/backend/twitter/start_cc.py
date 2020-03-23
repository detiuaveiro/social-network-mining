## @package twitter

from control_center.dbwriter import DBWriter

if __name__ == "__main__":
	control_center = DBWriter()
	control_center.run()
	control_center.close()
