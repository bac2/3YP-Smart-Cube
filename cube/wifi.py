import urllib2
import urllib

def is_wifi_on():
	try:
		urllib2.urlopen('http://google.com', timeout=1)
		return True
 	except urllib2.URLError:
		return False

def send_post_data(hashdata):
	post_data = { 'data':'value' }
	post_encode = urllib.urlencode(hashdata)
	request = urllib2.Request("http://webpage.com", post_encode)
	response = urllib2.urlopen(request)
	print response.read();


if __name__ == '__main__':
	print is_wifi_on()
