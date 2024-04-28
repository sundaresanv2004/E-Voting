# E-Voting

E-Voting v-6.01 is an election application designed for desktop and laptop computers. Built on the `flet` library in the Python programming language, it allows users to conduct elections quickly and easily. The application is primarily designed for use in schools and colleges, but it can also be used in other fields that require elections.


### Installation

To install E-Voting, follow these simple steps:

Note: You need python-3.10 or later version installed in your system.
This app only runs on Mac and Windows-10/(later)

1. Clone the repository to your local machine.
2. Install the libraries from requirements.txt file.
3. Run the main.py file.

### Connect Firebase

We're utilizing Firebase as our data storage solution. To establish the connection to Firebase, simply follow these steps:

__Database and storage management will be seamlessly handled by our program. Users only need to set up access to the database, storage, and authentication to access full functionality.__


1. Set Up a Firebase Account and Log In 
   - Create an Account: Visit the [Firebase website](https://firebase.google.com) and sign up for an account if you haven't already.
   - Log In: Access your Firebase account by logging in with your credentials.


2. Create a New Project 
   - Access the Console: Once logged in, navigate to the Firebase console.
   - Create Project: Click on 'Add project', then enter a custom name for your project that reflects your application's identity.


3. Set Up Authentication
   - Navigate to Authentication: In the Firebase console, select the 'Authentication' tab and then click on the 'Get started' button.
   - Enable Email/Password: Under the 'Sign-in method' tab, find the 'Email/Password' sign-in provider and enable it. This will allow your users to register and authenticate using their email addresses and passwords.


4. Initialize Firestore Database
   - Create Firestore Database: Go to the 'Database' section in the Firebase console and click on 'Create database'.
   - Set Security Rules: Choose 'Start in production mode' to set up Firestore with initial security rules that restrict data access to authorized users.
   - Complete Initialization: Follow the prompts to select your database's location and finalize its setup.


5. Set Up Firebase Storage
   - Initialize Storage: Navigate to the 'Storage' section in the Firebase console and click on 'Get started'.
   - Create Storage Instance: Click on 'Create storage' to provision cloud storage for your application, which is essential for handling file uploads securely.


6. Generate a New Private Key
   - Access Project Settings: Go back to the main dashboard of the Firebase console and select the 'Project settings'.
   - Service Account Tab: Click on the 'Service accounts' tab.
   - Download Private Key: Click on 'Generate new private key', then confirm the action to download the key, which will be stored in your default download folder.


7. Run Your E-Voting Application 
   - Launch Application: Start your e-voting application. It should prompt you to upload the private key you downloaded.
   - Upload Key: Locate and select the key file from your download folder to authenticate and connect your application to Firebase.


Note: Each Firebase project serves as a dedicated repository for a single election dataset. Begin the process of creating a new election by initiating a new project in Firebase. Then, ensure seamless connectivity to additional databases by navigating to the settings menu and following the above steps once more to create a project.
### Features

- Simple and easy setup: E-Voting offers a user-friendly interface for easy setup and operation.
- Secure data storage: Data is stored in JSON and CSV formats with encryption for added security.
- Efficient data analysis: E-Voting provides accurate and timely analysis of election results.
- Two-Step Verification: To ensure that only authorized voters participate in the election, E-Voting uses a two-step verification process.
- Candidate management: The application allows users to manage candidate data easily.
- Multi-field usage: E-Voting can be used in various fields requiring secure and efficient elections.

### Requirements

To use E-Voting, you will need a desktop or laptop with the following specifications:

- A Windows, macOS operating system
- Python 3.10 or later installed on your system
- The `flet`, `pandas`, `cryptography`, `firebase-admin` librarys installed on your system
- An active internet connection

### Usage

Using E-Voting is simple and straightforward. Once the application is launched, follow the on-screen instructions to set up an election. You can manage candidates, set up a two-step verification process, and analyze results. E-Voting makes it easy to conduct an election in just a few clicks.

### Contributing

If you are interested in contributing to E-Voting, please fork the repository and submit a pull request. We welcome any suggestions, feedback, or bug reports.

### License
E-Voting is licensed under the **MIT License**.
