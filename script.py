import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QPushButton, QLabel, QListWidget,
                             QStackedWidget, QMessageBox, QTextEdit)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import mysql.connector
from datetime import datetime
from mysql.connector import Error
import cryptographer as cr
import os
import json

class ChatApp(QWidget):
    def __init__(self):
        super().__init__()
        self.current_user = None
        self.db_conn = self.create_db_connection()
        self.init_db_tables()
        self.setWindowIcon(QIcon("Textit.png"))
        self.initUI()

    def create_db_connection(self):
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',        # Change to your MySQL username
                password='admin',
                database="textit" # Change to your MySQL password
            )
            return conn
        except Error as e:
            QMessageBox.critical(self, "Database Error", f"Failed to connect to MySQL: {e}")
            sys.exit(1)

    def init_db_tables(self):
        try:
            cursor = self.db_conn.cursor()
                        
            # Create users table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            
            # Create messages table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                sender_id INT NOT NULL,
                receiver_id INT NOT NULL,
                message TEXT NOT NULL,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (sender_id) REFERENCES users(id),
                FOREIGN KEY (receiver_id) REFERENCES users(id)
            )
            ''')
            
            self.db_conn.commit()
        except Error as e:
            QMessageBox.critical(self, "Database Error", f"Failed to create tables: {e}")
            sys.exit(1)

    def initUI(self):
        self.setWindowTitle('TextIt Application (Login Window)')
        self.setGeometry(100, 100, 800, 600)
        
        # Stacked widgets for different views
        self.stackedLayout = QStackedWidget()
        
        # Sign In Page
        self.signInPage = QWidget()
        self.setupSignIn()
        self.stackedLayout.addWidget(self.signInPage)
        
        # Sign Up Page
        self.signUpPage = QWidget()
        self.setupSignUp()
        self.stackedLayout.addWidget(self.signUpPage)
        
        # Contacts Page
        self.contactsPage = QWidget()
        self.setupContacts()
        self.stackedLayout.addWidget(self.contactsPage)
        
        # Chat Page
        self.chatPage = QWidget()
        self.setupChat()
        self.stackedLayout.addWidget(self.chatPage)
        
        # Main layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.stackedLayout)
        self.setLayout(mainLayout)

    def setupSignIn(self):
        layout = QVBoxLayout()
        
        header = QLabel("Welcome to TextIt")
        header.setStyleSheet("font-size: 20px; font-weight: bold; font-style: italic;")
        header.setAlignment(Qt.AlignCenter)
        
        self.usernameInput = QLineEdit(self)
        self.usernameInput.resize(50,400)
        self.usernameInput.setPlaceholderText("Username")
        self.usernameInput.setStyleSheet("""
            QLineEdit {
                border: 2px solid #4CAF50; 
                border-radius: 15px; 
                padding: 10px; 
                font-size: 20px; 
            }
            QLineEdit:focus {
                border: 2px solid #FF5722;
            }
        """)
        
        self.passwordInput = QLineEdit(self)
        self.passwordInput.resize(50,400)
        self.passwordInput.setPlaceholderText("Password")
        self.passwordInput.setStyleSheet("""
            QLineEdit {
                border: 2px solid #4CAF50; 
                border-radius: 15px; 
                padding: 10px; 
                font-size: 20px; 
            }
            QLineEdit:focus {
                border: 2px solid #FF5722;
            }
        """)
        self.passwordInput.setEchoMode(QLineEdit.Password)
        
        self.signInButton = QPushButton("Sign In")
        self.signInButton.setFixedSize(150,50)
        self.signInButton.setStyleSheet("""
            QPushButton {
                background-color: #0000FF;  
                color: white;                
                border: none;               
                border-radius: 25px;        
                font-size: 16px;           
            }
            QPushButton:hover {
                background-color: #00008B;   /* Darker green on hover */
            }
        """)
        self.signInButton.clicked.connect(self.handleSignIn)
        
        self.signUpButton = QPushButton("Create Account")
        self.signUpButton.setFixedSize(150,50)
        self.signUpButton.setStyleSheet("""
            QPushButton {
                background-color: #0000FF;  
                color: white;                
                border: none;                
                border-radius: 25px;        
                font-size: 16px;             
            }
            QPushButton:hover {
                background-color: #00008B;   
            }
        """)
        self.signUpButton.clicked.connect(lambda: self.stackedLayout.setCurrentIndex(1))
        
        layout.addWidget(header)
        layout.addSpacing(10)
        layout.addWidget(self.usernameInput)
        layout.addSpacing(10)
        layout.addWidget(self.passwordInput)
        layout.addSpacing(10)
        layout.addWidget(self.signInButton, alignment=Qt.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(self.signUpButton, alignment=Qt.AlignCenter)
        
        self.signInPage.setLayout(layout)

    def setupSignUp(self):
        layout = QVBoxLayout()
        
        header = QLabel("Create New Account")
        header.setStyleSheet("font-size: 20px; font-weight: bold;font-style:Arial")
        header.setAlignment(Qt.AlignCenter)
        
        self.newUsername = QLineEdit(self)
        self.newUsername.setPlaceholderText("Username")
        self.newUsername.setStyleSheet("""
            QLineEdit {
                border: 2px solid #4CAF50; 
                border-radius: 15px; 
                padding: 10px; 
                font-size: 20px; 
            }
            QLineEdit:focus {
                border: 2px solid #FF5722;
            }
        """)
        
        self.newPassword = QLineEdit(self)
        self.newPassword.setPlaceholderText("Password")
        self.newPassword.setStyleSheet("""
            QLineEdit {
                border: 2px solid #4CAF50; 
                border-radius: 15px; 
                padding: 10px; 
                font-size: 20px; 
            }
            QLineEdit:focus {
                border: 2px solid #FF5722;
            }
        """)
        self.newPassword.setEchoMode(QLineEdit.Password)
        
        self.confirmPassword = QLineEdit(self)
        self.confirmPassword.setPlaceholderText("Confirm Password")
        self.confirmPassword.setStyleSheet("""
            QLineEdit {
                border: 2px solid #4CAF50; 
                border-radius: 15px; 
                padding: 10px; 
                font-size: 20px; 
            }
            QLineEdit:focus {
                border: 2px solid #FF5722;
            }
        """)
        self.confirmPassword.setEchoMode(QLineEdit.Password)
    
        
        self.signUpButton = QPushButton("Sign Up")
        self.signUpButton.setFixedSize(150,50)
        self.signUpButton.setStyleSheet("""
            QPushButton {
                background-color: #0000FF;  
                color: white;                
                border: none;              
                border-radius: 25px;       
                font-size: 16px;         
            }
            QPushButton:hover {
                background-color: #00008B;  
            }
        """)
        self.signUpButton.clicked.connect(self.handleSignUp)
        
        self.backButton = QPushButton("Back to Sign In")
        self.backButton.setFixedSize(150,50)
        self.backButton.clicked.connect(lambda: self.stackedLayout.setCurrentIndex(0))
        
        layout.addWidget(header)
        layout.addSpacing(20)
        layout.addWidget(self.newUsername)
        layout.addSpacing(10)
        layout.addWidget(self.newPassword)
        layout.addSpacing(10)
        layout.addWidget(self.confirmPassword)
        layout.addSpacing(10)
        layout.addWidget(self.signUpButton, alignment=Qt.AlignCenter)
        layout.addWidget(self.backButton, alignment=Qt.AlignCenter)
        
        self.signUpPage.setLayout(layout)

    def setupContacts(self):
        layout = QVBoxLayout()
        
        self.contactsList = QListWidget()
        self.contactsList.itemClicked.connect(self.startChat)
        
        self.logoutButton = QPushButton("Logout")
        self.logoutButton.setFixedSize(150,50)
        self.logoutButton.setStyleSheet("""
            QPushButton {
                background-color: #0000FF; 
                color: white;                
                border: none;               
                border-radius: 25px;      
                font-size: 16px;           
            }
            QPushButton:hover {
                background-color: #00008B; 
            }
        """)
        self.logoutButton.clicked.connect(self.logout)
        self.loadContacts()
        self.refreshButton = QPushButton("Refresh Contacts")
        self.refreshButton.setFixedSize(150,50)
        self.refreshButton.setStyleSheet("""
            QPushButton {
                background-color: #0000FF;  
                color: white;              
                border: none;              
                border-radius: 25px;       
                font-size: 16px;           
            }
            QPushButton:hover {
                background-color: #00008B;  
            }
        """)
        self.refreshButton.clicked.connect(self.loadContacts)
        
        layout.addWidget(QLabel("Your Contacts:"))
        layout.addWidget(self.contactsList)
        layout.addWidget(self.refreshButton, alignment=Qt.AlignCenter)
        layout.addWidget(self.logoutButton, alignment=Qt.AlignCenter)
        
        self.contactsPage.setLayout(layout)

    def setupChat(self):
        layout = QVBoxLayout()
        
        self.chatPartnerLabel = QLabel()
        self.chatPartnerLabel.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.chatPartnerLabel.setAlignment(Qt.AlignCenter)
        
        self.chatHistory = QTextEdit()
        self.chatHistory.setReadOnly(True)
        
        self.messageInput = QTextEdit(self)
        self.messageInput.setPlaceholderText("Enter text here")
        self.messageInput.setStyleSheet("""
            QLineEdit {
                border: 2px solid #4CAF50; 
                border-radius: 15px; 
                padding: 10px; 
                font-size: 20px; 
            }
            QLineEdit:focus {
                border: 2px solid #FF5722;
            }
        """)
        
        
        self.sendButton = QPushButton("Send")
        self.sendButton.setFixedSize(150,50)
        self.sendButton.setStyleSheet("""
            QPushButton {
                background-color: #0000FF;  
                color: white;                
                border: none;               
                border-radius: 25px;       
                font-size: 16px;            
            }
            QPushButton:hover {
                background-color: #00008B;  
            }
        """)
        self.sendButton.clicked.connect(self.sendMessage)
        
        self.backButton = QPushButton("Back to Contacts")
        self.backButton.setFixedSize(150,50)
        self.backButton.setStyleSheet("""
            QPushButton {
                background-color: #ADD8E6;  
                color: white;               
                border: none;                
                border-radius: 25px;       
                font-size: 16px;             
            }
            QPushButton:hover {
                background-color: #00008B;   
            }
        """)
        self.backButton.clicked.connect(lambda: self.stackedLayout.setCurrentIndex(2))
        
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.backButton)
        buttonLayout.addWidget(self.sendButton)
        
        layout.addWidget(self.chatPartnerLabel)
        layout.addWidget(self.chatHistory)
        layout.addWidget(QLabel("Your Message:"))
        layout.addWidget(self.messageInput)
        layout.addLayout(buttonLayout)
        
        self.chatPage.setLayout(layout)
    
    def handleSignUp(self):
        username = self.newUsername.text()
        password = self.newPassword.text()
        confirm = self.confirmPassword.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Username and password are required")
            return
        if password != confirm:
            QMessageBox.warning(self, "Error", "Passwords do not match")
            return
        
        flag_file = "flag.txt"
        if not os.path.exists(flag_file):

            cipher = cr.key_generator()
            with open("key.json","w") as f1:
                json.dump(cipher,f1)
            with open(flag_file,"w") as f:
                f.write("Program has run.")
        
        else:
            with open("key.json","r") as f:
                cipher = json.load(f)

                
        try:
            cursor = self.db_conn.cursor()
            enc_password = cr.encrypter(password, cipher)
            
            cursor.execute("USE textit")
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", 
                         (username, enc_password))
            self.db_conn.commit()
            
            self.stackedLayout.setCurrentIndex(2)
            self.newUsername.clear()
            self.newPassword.clear()
            self.confirmPassword.clear()
        except Error as e:
            QMessageBox.warning(self, "Error", f"Failed to create account: {e}")

    def handleSignIn(self):
        username = self.usernameInput.text()
        password = self.passwordInput.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password")
            return
        with open("key.json","r") as f:
            cipher = json.load(f)
        try:
            cursor = self.db_conn.cursor(dictionary=True)
            enc_password = cr.encrypter(password,cipher)
            cursor.execute("USE textit")
            cursor.execute("SELECT id, username FROM users WHERE username = %s AND password = %s", 
                         (username, enc_password))
            user = cursor.fetchone()
            
            if user:
                self.current_user = {'id': user['id'], 'username': user['username']}
                self.stackedLayout.setCurrentIndex(2)
                self.usernameInput.clear()
                self.passwordInput.clear()
            else:
                QMessageBox.warning(self, "Error", "Invalid username or password")
        except Error as e:
            QMessageBox.critical(self, "Database Error", f"Failed to sign in: {e}")

    def loadContacts(self):
        if not self.current_user:
            return
            
        self.contactsList.clear()
        try:
            cursor = self.db_conn.cursor(dictionary=True)
            cursor.execute("USE textit")
            cursor.execute("SELECT id, username FROM users WHERE id != %s", (self.current_user['id'],))
            contacts = cursor.fetchall()
            
            for contact in contacts:
                self.contactsList.addItem(f"{contact['username']} (ID: {contact['id']})")
        except Error as e:
            QMessageBox.critical(self, "Database Error", f"Failed to load contacts: {e}")

    def startChat(self, item):
        if not self.current_user:
            return
            
        contact_text = item.text()
        contact_id = int(contact_text.split("ID: ")[1].strip(")"))
        
        try:
            cursor = self.db_conn.cursor(dictionary=True)
            cursor.execute("USE textit")
            cursor.execute("SELECT username FROM users WHERE id = %s", (contact_id,))
            contact = cursor.fetchone()
            
            if not contact:
                QMessageBox.warning(self, "Error", "Contact not found")
                return
                
            self.current_chat = {
                'id': contact_id,
                'username': contact['username']
            }
            
            self.chatPartnerLabel.setText(f"Chat with {self.current_chat['username']}")
            self.loadChatHistory()
            self.stackedLayout.setCurrentIndex(3)
        except Error as e:
            QMessageBox.critical(self, "Database Error", f"Failed to start chat: {e}")

    def loadChatHistory(self):
        if not self.current_user or not self.current_chat:
            return
            
        self.chatHistory.clear()
        try:
            cursor = self.db_conn.cursor(dictionary=True)
            cursor.execute("USE textit")
            cursor.execute('''
            SELECT 
                u.username as sender, 
                m.message, 
                m.sent_at 
            FROM 
                messages m
            JOIN 
                users u ON u.id = m.sender_id
            WHERE 
                (m.sender_id = %s AND m.receiver_id = %s)
                OR 
                (m.sender_id = %s AND m.receiver_id = %s)
            ORDER BY 
                m.sent_at
            ''', (self.current_user['id'], self.current_chat['id'], 
                  self.current_chat['id'], self.current_user['id']))
            
            messages = cursor.fetchall()

            with open("key.json","r") as f:
                cipher = json.load(f)

            for message in messages:
                timestamp = str(message['sent_at']).split('.')[0]
                dec_message = cr.decrypter(message['message'],cipher)
                self.chatHistory.append(f"[{timestamp}] <{message['sender']}> {dec_message}")
            
            self.chatHistory.verticalScrollBar().setValue(
                self.chatHistory.verticalScrollBar().maximum())
        except Error as e:
            QMessageBox.critical(self, "Database Error", f"Failed to load chat history: {e}")

    def sendMessage(self):
        if not self.current_user or not self.current_chat:
            return
            
        message = self.messageInput.toPlainText().strip()
        if not message:
            return
        
        with open("key.json","r") as f:
            cipher = json.load(f)

        try:
            cursor = self.db_conn.cursor()
            enc_message = cr.encrypter(message,cipher)
            cursor.execute("USE textit")
            cursor.execute('''
            INSERT INTO messages (sender_id, receiver_id, message)
            VALUES (%s, %s, %s)
            ''', (self.current_user['id'], self.current_chat['id'], enc_message))
            self.db_conn.commit()
            
            self.messageInput.clear()
            self.loadChatHistory()
        except Error as e:
            QMessageBox.critical(self, "Database Error", f"Failed to send message: {e}")

    def logout(self):
        self.current_user = None
        self.stackedLayout.setCurrentIndex(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ChatApp()
    window.show()
    sys.exit(app.exec_())
