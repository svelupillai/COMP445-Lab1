import socket
import argparse
from urllib.parse import urlparse


def get(url,v):
   # Step 1: initialize socket
   listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   # extract hostname from the url using urlparse
   url = urlparse(url)
   # Step 2: Connect to port 80
   listener_socket.connect((url.hostname, 80))
   # Step 3: request from the server using GET
   request = "GET " + url.path + "?" + url.query + " HTTP/1.1\r\nHost: " + url.hostname + "\r\n\r\n"
   # Step 4: send the request
   listener_socket.sendall(request.encode("utf-8"))
   response = listener_socket.recv(4096).decode("utf-8")
   # Step 5: At post 1024, response received

   # Include first 9 lines of header if verbose
   if not v:
       response = response.split("\n")
       for i in range(9,len(response)):
           print(response[i])

   else:
       print(response)
   listener_socket.close()

def post(url, header, data, v):
    # Step 1: initialize socket
   listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # extract hostname from the url using urlparse
   url = urlparse(url)
   listener_socket.connect((url.hostname, 80))
   request = "POST " + url.path + " HTTP/1.1" + "\r\n" + "Host: " + url.hostname + "\r\n" + "Content-Length: " + str(len(data)) + "\r\n" + header + "\r\n\r\n" + data + "\r\n\r\n"
    # Step 4: send the request
   listener_socket.sendall(request.encode("utf-8"))
   response = listener_socket.recv(4096).decode("utf-8")
    # Step 5: At post 1024, response received

    # Include first 9 lines of header if verbose
   if not v:
       response = response.split("\n")
       for i in range(9, len(response)):
           print(response[i])

   else:
       print(response)
   listener_socket.close()


# argument parsing
parser = argparse.ArgumentParser()
verbose_post = parser.add_mutually_exclusive_group()
verbose_post.add_argument('-g', '--get', help= 'get with URL argument', type=str)
verbose_post.add_argument('-p', '--post', help= 'post with URL argument', type=str)
parser.add_argument('--h', '--header', help='header for HTTP post', type=str)
dataVsFile = parser.add_mutually_exclusive_group()
dataVsFile.add_argument('-d', '--data', help='data string for HTTP post', type=str)
dataVsFile.add_argument('-f', '--file', help='file for HTTP post', type=str)
verbose = parser.add_argument('-v', '--verbose', help='show verbose output',
       action='store_true')

args = parser.parse_args()
if args.get is not None:
   get(args.get, args.verbose)
elif args.post is not None and args.h is not None:
   if args.data is not None:
       post(args.post, args.h, args.data, args.verbose)
   elif args.file is not None:
       f = open(args.file, 'r')
       data = f.read()
       f.close()
       post(args.post, args.header, data, args.verbose)
   else:
       print("error: expected either a data string (-d) or file (-f) for post request.")
       parser.print_help()
elif args.post is not None and args.header is None:
   print("error: expected a header (--header) for post request.")
   parser.print_help()
else:
   parser.print_help()