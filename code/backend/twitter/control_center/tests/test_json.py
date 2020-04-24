import control_center.PDP as cc


def test_json():
	control = cc.PDP()
	print(control.get_first_time_list())
	control.close()
