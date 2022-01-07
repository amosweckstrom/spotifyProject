import requests
import webbrowser
import base64
import json

#client id from spotify application
CLIENT_ID = "clientID"
#client secret from spotify application
CLIENT_SECRET = "clientSecret"

#dont have a server running now so i am using a website that returns information sent to it
REDIRECT_URI = "https://httpbin.org/anything"

#Base spotify api url
BASE_URL = 'https://api.spotify.com/v1/'

#initialize USER_ID
USER_ID = None



#encode client id and client secret to base64
client_ids_string = CLIENT_ID + ":" + CLIENT_SECRET
client_ids_byte = client_ids_string.encode("ascii")
base64bytes = base64.b64encode(client_ids_byte)
base64string = str(base64bytes, 'ascii')

#initialize acces token
access_token = None

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
	return url

#funtction to exchnage code for accestoken
def exchange_code_for_acces_token(code):
	params1 = {
		"grant_type": "authorization_code",
		"code": code,
		"redirect_uri": REDIRECT_URI
	}

	headers = {
		"Authorization": "Basic %s" % base64string,
		"Content-type": "application/x-www-form-urlencoded"
	}
	endpoint = "https://accounts.spotify.com/api/token"
	response = requests.post(endpoint, params=params1, headers=headers)
	response = response.json()
	##print(response)
	access_token = response['access_token']
	return response['access_token']

#function for refresh token
def request_refresh_token():
	pass

#function that returns users playlists
def get_user_playlist(user_id, token):
	
	user_playlist_endpoint = BASE_URL + "users/" + user_id + "/playlists"
	print(user_playlist_endpoint)
	headers = {
	'Authorization': 'Bearer {}'.format(token)
	}

	params = {
	"user_id": user_id
	}
	response = requests.get(user_playlist_endpoint, headers=headers, params=params)
	print(response.status_code)
	response = response.json()
	return response

def create_new_file(playlists):
	file = open("user_playlists", "wb")
	json_object = json.dumps(playlists, indent = 4)
	with open("user_playlists.json", "w") as outfile:
		outfile.write(json_object)



def main():
	#opens link created by function
	webbrowser.open(create_oauth_link())
	
	code = input("Code please")
	
	#saves acces token in variable
	access_token = exchange_code_for_acces_token(code)
	#asks user for their spotify id ex. "smedjan"
	USER_ID = input("enter your user id please")
	#saves information about the users playlists in user_playlists
	user_playlists = get_user_playlist(USER_ID, access_token)

	print(user_playlists)

	create_new_file(user_playlists)




if __name__ == '__main__':
	main()
