import requests
import webbrowser
import base64

#client id from spotify application
CLIENT_ID = "db459c6c7af046da9f7ed812c73a8f69"
#client secret from spotify application
CLIENT_SECRET = "5dab7ec1e0ae4fc0a1787d716a58d8ec"

REDIRECT_URI = "https://httpbin.org/anything"
#encode client id and client secret to base64
client_ids_string = CLIENT_ID + ":" + CLIENT_SECRET
client_ids_byte = client_ids_string.encode("ascii")
base64string = base64.b64encode(client_ids_byte)
base64_test_string = "ZGI0NTljNmM3YWYwNDZkYTlmN2VkODEyYzczYThmNjk6NWRhYjdlYzFlMGFlNGZjMGExNzg3ZDcxNmE1OGQ4ZWM="

#function to create authentication link for user
def create_oauth_link():
	params = {
	"client_id": CLIENT_ID,
	"response_type": "code",
	"redirect_uri": REDIRECT_URI,
	"scope":"user-read-email playlist-read-private user-top-read"
	}

	endpoint = "https://accounts.spotify.com/authorize?"

	response = requests.get(endpoint, params=params)
	url = response.url
	print(response.status_code)
	return url

#funtction to exchnage code for accestoken
def exchange_code_for_acces_token(code):
	params ={
		"grant-type": "authorization-code",
		"code": code,
		"redirect-uri": REDIRECT_URI
	}

	headers = {
		"Authorization": "Basic %s" % base64string,
		"Content-type": "application/x-www-form-urlencoded"
	}
	print(headers["Authorization"])
	endpoint = "https://accounts.spotify.com/api/token"
	response = requests.post(endpoint, params=params, headers=headers)
	print(response.status_code)
	response = response.json()
	return response['access_token']

def main():
	#opens link created by function
	webbrowser.open(create_oauth_link())
	code = input("Code please")
	print(exchange_code_for_acces_token(code))



if __name__ == '__main__':
	main()