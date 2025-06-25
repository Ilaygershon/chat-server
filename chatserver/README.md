# Chat Server

A real-time chat application built with Python that allows multiple users to communicate through a client-server architecture. The application features user registration, authentication, real-time messaging, and persistent chat history.

## Features

- **User Authentication**: Secure registration and login system
- **Real-time Messaging**: Live chat between online users
- **Persistent Chat History**: Messages are saved and can be viewed when offline
- **Multiple Conversations**: Support for multiple chat sessions per user
- **Online Status**: See which users are currently online/offline
- **Cross-platform GUI**: Tkinter-based graphical user interface
- **Database Storage**: SQLite database for user data and chat history
- **Network Discovery**: Automatic IP detection for server hosting

## Architecture

The application consists of several key components:

- **Server (`server.py`)**: Central server handling client connections and message routing
- **Client GUI (`client.py`)**: Main client interface for login/registration
- **Chat Interface (`client_home.py`)**: Real-time chat interface and message handling
- **Network Layer (`client_request.py`)**: Socket communication utilities
- **Database Layer (`database.py`)**: SQLite database operations

## Requirements

- Python 3.6+
- Standard library modules:
  - `tkinter` (GUI)
  - `socket` (networking)
  - `sqlite3` (database)
  - `threading` (concurrent operations)
  - `subprocess` (system commands)
  - `re` (regular expressions)

## Installation

1. Clone or download the project files
2. Ensure all Python files are in the same directory:
   - `server.py`
   - `client.py`
   - `client_home.py`
   - `client_request.py`
   - `database.py`

3. No additional package installation required (uses Python standard library)

## Usage

### Starting the Server

1. Run the server on the host machine:
```bash
python server.py
```

2. The server will automatically detect the local IP address and start listening on port 2000
3. Server output will show the IP address it's running on

### Connecting Clients

1. Run the client application:
```bash
python client.py
```

2. Enter the server's IP address when prompted
3. Choose to either register a new account or login with existing credentials

### Using the Chat Application

**Registration:**
- Choose a unique username (cannot contain `:` or `` `#` `` characters)
- Set a secure password
- Click "register" to create your account

**Login:**
- Enter your username and password
- Click "login" to access the chat interface

**Chatting:**
- View your conversation list on the home screen
- Click "start new conversation" to chat with other users
- Messages appear in real-time for online users
- Chat history is preserved for offline viewing
- Use the "back" button to return to conversation list
- Use "logout" to return to the login screen

## Technical Details

### Network Protocol

The application uses a custom protocol over TCP sockets:

**Server Port**: 2000  
**Client Listener Port**: 2001

**Message Format**: `MODE:USERNAME:DATA`

**Supported Modes**:
- `IS_HOST` - Check server availability
- `REGISTER` - User registration
- `LOGIN` - User authentication
- `HOME` - Get conversation list
- `GET_USERS` - Get all registered users
- `ONLINE` - Register client as online
- `OFFLINE` - Register client as offline
- `ONLINE_USERS` - Check if user is online
- `START_CONVERSATION` - Initialize new chat
- `SEND_MESSAGE` - Send real-time message
- `SAVE_MESSAGE` - Save message to database
- `OFFLINE_CHAT` - Retrieve chat history

### Database Schema

**Users Table**:
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
```

**User Chat Tables** (per user):
```sql
CREATE TABLE user{id} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    conversation TEXT
)
```

### File Structure

```
chat-server/
├── server.py           # Main server application
├── client.py           # Client login/registration GUI
├── client_home.py      # Chat interface and client listener
├── client_request.py   # Socket communication utilities
├── database.py         # Database operations
└── Users.db           # SQLite database (created automatically)
```

## Security Considerations

- Passwords are stored in plain text (consider hashing for production use)
- No encryption for network communication (consider TLS for production)
- Input validation prevents some injection attacks but could be enhanced
- Server runs on local network only (192.168.x.x range)

## Limitations

- Windows-specific IP detection using `ipconfig`
- No user profile pictures or file sharing
- No group chat functionality
- No message encryption
- Basic error handling
- Single server instance only

## Troubleshooting

**"There is no run server at this ip address"**
- Ensure the server is running on the specified IP
- Check firewall settings
- Verify both server and client are on the same network

**"There is a run server on this ip and port!"**
- Another client is already running on this machine
- Close other instances or use a different machine

**Database errors**
- Ensure write permissions in the application directory
- Check if `Users.db` file is accessible

**Connection issues**
- Verify network connectivity between server and client machines
- Check if ports 2000 and 2001 are available
- Ensure Windows Firewall allows the application

## Future Enhancements

- Cross-platform IP detection (Linux/macOS support)
- Message encryption and secure authentication
- Group chat functionality
- File sharing capabilities
- User profiles and avatars
- Message timestamps
- Emoji support
- Push notifications
- Web-based client interface

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.