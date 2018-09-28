#!../flask/bin/python3

import requests as req
import argparse

def sendCode(inputCode,questionHash):
	# Open the code file using the path sent.
	
	code = None

	with open(inputCode,"r") as fp:
		if(fp.readable()):
			code = fp.read()

	# Create the data object to be sent to server.
	data = {
		"USN":[],
		"code":code,
		"progLang":"Python3",
		"questionHash":questionHash,
	}

	# Make a post request with the data to be sent.
	res = req.post("http://localhost:5000/submitCode",
			json = data,
			headers={
				"content-type":"application/json"
			}
		)

	print("res")
	if(res.ok):
		return(res.text)
	else:
		return("Error occured : ",res.status_code)


if __name__=="__main__":
	# Parse CLI Arguments
	parser = argparse.ArgumentParser()

	parser.add_argument("-u","--upload",
		dest='inputCode', 
		type=str, 
		required=True, 
		help="/path/to/the/file/having/code.ext")

	parser.add_argument("-q","--question",
		dest='questionHash', 
		type=str, 
		help="Hash value of the question")

	args = parser.parse_args()

	retCode = sendCode(args.inputCode, args.questionHash)
	print(retCode)
