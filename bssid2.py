from access_points import get_scanner

wifi_scanner = get_scanner()
wifiInfo = wifi_scanner.get_access_points()
print wifiInfo
print wifiInfo[1]["bssid"]
