# E-Voting

E-Voting v-6.01 is an election application designed for desktop and laptop computers. Built on the `flet` library in the Python programming language, it allows users to conduct elections quickly and easily. The application is primarily designed for use in schools and colleges, but it can also be used in other fields that require elections.

### Installation
To install E-Voting version-6.08, follow these simple steps:

Note: You need Python 3.10 or later version installed on your system. This app is compatible only with Mac and Windows 10 (or later).

1. Clone the repository to your local machine.
2. Install the required libraries from the requirements.txt file.
3. Run the main.py file.

Alternatively, you can download the complete app from the "Version" section. Click on "Install" to automatically installer.py the app. Once installed, simply run vote.py to start using the application without any further manual steps.

This streamlined process ensures a hassle-free installation experience for users.


### Version

Version(5.01): [Get Here](https://drive.google.com/file/d/1TXIkfS3dKSFbkvoECO2Utr039laP7BvW/view?usp=drive_link) __This version doesn't required a firebase connection it runs on local system.__
Version(5.08): [Get Here]()

## Firebase Project Setup Guide

This guide will help you set up a Firebase project, enable email authentication, configure Firestore and Real-time Database with specific security rules, and enable storage. Finally, you'll create a Web App and integrate the Firebase configuration.

### Step 1: Create a Firebase Project

1. **Go to the Firebase Website**
   - Open your web browser and go to the [Firebase Console](https://console.firebase.google.com/).


2. **Log In**
   - Log in with your Google account email.


3. **Create a New Project**
   - Click on "Add project" or "Create a project".
   - Enter a name for your project (e.g., "MyFirebaseProject").
   - Click "Continue".
   - (Optional) Configure Google Analytics for your project, then click "Create project".


4. **Wait for the project to be created**
   - Once your project is ready, click "Continue".

### Step 2: Enable Email/Password Authentication

1. **Navigate to Authentication**
   - In the Firebase Console, click on the menu icon (three horizontal lines) in the top left corner to open the navigation bar.
   - Select "Authentication" from the menu.


2. **Enable Email/Password Sign-In**
   - Click on the "Sign-in method" tab.
   - Find "Email/Password" in the list and click on it.
   - Enable the switch to turn on Email/Password authentication.
   - Click "Save".

### Step 3: Set Up Firestore

1. **Navigate to Firestore Database**
   - In the Firebase Console, open the navigation bar and select "Firestore Database".


2. **Create a Database**
   - Click "Create database".
   - In the setup prompt, choose "Start in production mode".
   - Select a location that is comfortable for you and click "Enable".


3. **Configure Firestore Security Rules**
   - Click on the "Rules" tab.
   - Delete the default rules and replace them with the following:

   ```plaintext
   rules_version = '2';

   service cloud.firestore {
     match /databases/{database}/documents {
       match /{document=**} {
         allow read, write: if true;
       }
     }
   }
   ```
   
   
4. **Publish Rules**
   - Click "Publish" to apply the new rules.`

## Step 4: Set Up Real-time Database

1. **Navigate to Real-time Database**
   - In the Firebase Console, open the navigation bar and select "Realtime Database".


2. **Create a Database**
   - Click "Create Database".
   - In the setup prompt, choose "Start in production mode".
   - Select a location that is comfortable for you and click "Enable".


3. **Configure Real-time Database Security Rules**
   - Click on the "Rules" tab.
   - Delete the default rules and replace them with the following:

   ```json
   {
     "rules": {
       ".read": "auth != null",  
       ".write": "auth != null"
     }
   }
   ```

4. **Publish Rules**
   - Click "Publish" to apply the new rules.


## Step 5: Set Up Storage

1. **Navigate to Storage**
   - In the Firebase Console, open the navigation bar and select "Storage".

2. **Enable Storage**
   - Click "Get Started".
   - Select a location that is comfortable for you and click "Done".

3. **Configure Storage Security Rules**
   - Click on the "Rules" tab.
   - Delete the default rules and replace them with the following:

   ```plaintext
   service firebase.storage {
     match /b/{bucket}/o {
       match /{allPaths=**} {
         allow read, write: if true;
       }
     }
   }
   ```


4. **Publish Rules**
   - Click "Publish" to apply the new rules.

## Step 6: Create a Web App

1. **Add a Web App**
   - In the Firebase Console, open the navigation bar and select "Project Overview".
   - Click the gear icon next to "Project settings" and select "Project settings".
   - Click on the "General" tab, then scroll down to "Your apps".
   - Click on the web icon (</>) to add a web app.
   - Enter a name for your web app (e.g., "MyWebApp").
   - Click "Register app".

2. **Copy the Configuration Code**
   - After registering the app, Firebase will provide you with configuration code. Copy this code.

3. **Integrate Firebase Configuration**
   - Paste the copied configuration code into your web app's initialization script.

## Step 7: Set Up Privacy and Security

1. **Download Privacy and Security Settings**
   - In the Firebase Console, navigate to "Security & Privacy".
   - Download the required settings.

2. **Upload Settings**
   - Upload the downloaded settings to your web app to ensure it adheres to the best security practices.


Note: Each Firebase project serves as a dedicated repository for a single election dataset. Begin the process of creating a new election by initiating a new project in Firebase. Then, ensure seamless connectivity to additional databases by navigating to the settings menu and following the above steps once more to create a project.
### Features

- Simple and easy setup: E-Voting offers a user-friendly interface for easy setup and operation.
- Secure data storage: Data is stored in JSON and CSV formats with encryption for added security.
- Efficient data analysis: E-Voting provides accurate and timely analysis of election results.
- Two-Step Verification: To ensure that only authorized voters participate in the election, E-Voting uses a two-step verification process.
- Candidate management: The application allows users to manage candidate data easily.
- Multi-field usage: E-Voting can be used in various fields requiring secure and efficient elections.

### Usage

Using E-Voting is simple and straightforward. Once the application is launched, follow the on-screen instructions to set up an election. You can manage candidates, set up a two-step verification process, and analyze results. E-Voting makes it easy to conduct an election in just a few clicks.
 

### License
E-Voting is licensed under the **MIT License**.
