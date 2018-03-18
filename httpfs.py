import socket
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('-v', help ='Prints debugging messages.', type = str)
parser.add_argument('-p', '--port', help = 'Specifies the port number that the server will listen and serve at. Default is 8080', type = int)
parser.add_argument('-d', '--directory', '-PATH-TO-DIR', help = 'Specifies the directory that the server will use to read/write requested files. Default is the current directory when launching the application.', type = str)
args = parser.parse_args()

print(args);

host = ''

port = 8080

if args.port is not None:
    port = args.port

localPath = os.path.dirname(os.path.realpath(__file__))
if args.directory is not None:
    localPath = args.directory

# set up list of valid files, remove httpfs.py from said list if using default dir
fileList = os.listdir(localPath)
if localPath == os.path.dirname(os.path.realpath(__file__)):
    fileList.remove("httpfs.py")

# set up socket
listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listener.bind((host, port))
listener.listen(1)
print("serving HTTP on port", port)
while True:
    connection, address = listener.accept()
    request = connection.recv(1024).decode("utf-8")
    # split request into its useful parts (get VS post, path, data)
    request = request.split('\r\n')
    getVsPostLine = request[0].split()
    getVsPost = getVsPostLine[0]
    path = getVsPostLine[1]
    separatorLine = request.index('')
    data = ""
    for line in request[separatorLine + 1:]:
        data += line + "\n"
    response = ""

    if getVsPost == 'GET':
        if path == "/":
            # display fileList
            for file in fileList:
                response += file + "\n"
        else:
            # display contents of file (only if it's in the fileList, else 404)
            if path[1:] in fileList:
                fileSpecific = open(localPath + path, 'r')
                response = fileSpecific.read()
                fileSpecific.close()
            else:
                response = "404"
    elif getVsPost == 'POST':
        # write to file (only if it's in the fileList, else 403)
        if path[1:] in fileList:
            fileSpecific = open(localPath + path, 'w')
            fileSpecific.write(data)
            fileSpecific.close()
        else:
            response = "403"

    # send response
    connection.sendall(bytes(response, "utf-8"))
    connection.close()
