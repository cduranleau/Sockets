# Christian Duranleau Tech Demo - WebSockets

## Requirements
* Python 3.x
* Pip3
* Terminal interface to a computer



## Instructions
Install dependencies 

```pip3 install -r requirements.txt```

Run the Server

```python3 main.py server```

In a new terminal, run the client.

```python3 main.py client```

In the terminal for the client, enter some text. Inputs from the user will be denoted with the `*` symbol. Responses from the server will be denoted with the `+` symbol.

```
$ python3 main.py client
* Hello World!
+ Hello World!
*
```


In the terminal for the server, view the echoed text.
```
python3 main.py server
+ Hello World!
```


Exit the Client by pressing `ctrl+c`. Exit the server by pressing `ctrl+c`

### Additional Verification Method using curl
``` 
# This creates a 24 byte key that is used to ensure unique websocket connections
x=`echo "24 byte strings" | base64`

curl --include \
     --no-buffer \
     --header "Connection: Upgrade" \
     --header "Upgrade: websocket" \
     --header "Host: localhost:1234" \
     --header "Origin: http://localhost:1234" \
     --header "Sec-WebSocket-Key: $x" \
     --header "Sec-WebSocket-Version: 13" \
     http://localhost:1234/

```




