#  coding: utf-8 
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        fileName = self.parseData(self.data)

        # Handling
        if type(fileName) == str:
            try:
                file = open("www" + fileName[:-1], "r")
                print(file)

                contentType = ""

                if file.endswith(".html/"):
                    contentType = "text/html"
                    return contentType
                elif file.endswith(".css/"):
                    contentType = "text/css"
                    return contentType
                else:
                    print("Not applicable content type!")
                    print(contentType)
                
                self.request.sendall(bytearray("HTTP/1.1 200 OK\r\n", "utf-8"))
                self.request.sendall(bytearray("Content Type: " + contentType + "\r\n\n", "utf-8"))
                self.request.sendall(bytearray(file.read(), "utf-8"))
                file.close()
            except: # Error handling (404)
                self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n", "utf-8"))

    
    def parseData(self, data):
        # This function processes and parses the GET request
        data = data.decode()

        # Handing for reponses that default to invalid/incorrect
        if data == "":
            return None
        if not data.startswith("GET"): # We should only handle GET methods
            return self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\n", "utf-8"))

        
        # Decompose to the "Request-URI" we need
        message = data.rsplit(" ")
        fileName = message[1]
        fileName = fileName + "/"
        print(fileName)

        # Assembling/processessing file name
        if fileName[-1] != "/": # Check for 301 
            return self.request.sendall(bytearray("HTTP/1.1 301 Moved Permanently\r\nLocation: http://127.0.0.1:8000" + fileName + "/\r\n\n", "utf-8"))
        if fileName == "/" or (not fileName.endswith("css/") and not fileName.endswith("html/")): 
            return(fileName + "index.html/")
        elif fileName.endswith("css/") and fileName != "/base.css/":
            return(fileName.replace("index.html/", ""))
        else:
            print("xd")
            return fileName

    
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
