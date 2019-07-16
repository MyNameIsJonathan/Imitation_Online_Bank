# My SynapseFi Coding Challenge
My submission for the back-end engineering coding challenge, using the SynapseFi API and Python wrapper

Began: Monday July 8, 2019

Completed: Monday July 15, 2019

# To run flask app
1 - Fork/download project folder

2 - Navigate to folder locally

3 - Inside the folder, run the following bash command (with Docker Daemon running):

    ```
    docker-compose up -d
    ```
    
4 - Go to the following address in your browser: http://localhost:5000/


# Project Structure:

  This is a Flask-Python-Docker program that runs on two separate Docker containers
  
    (1) - Flask container running Python 3.7
    
    (2) - MongoDB container running MongoDB 4.1.13
    
    
  This project mimics an online-only, neo banking system that allows users to:
  
    Register
    
    Login
    
    Logout
    
    View and update user information
    
    Create DEPOSIT-US accounts
    
    View DEPOSIT-US accounts
    
    Send money between DEPOSIT-US accounts (functionality not complete due to non-production account); returns successful API response.
    
    Delete DEPOSIT-US accounts
    
    View current Bitcoin and Ethereum prices
    
    Open cryptocurrency accounts
    
    View crypto accounts
    
    Purchase Bitcoin and Ethereum cryptocurrencies (functionality not complete due to non-production account); returns successful API            response.
    
    Close cryptocurrency accounts


# Ideas for future work on this project:


  Functionality


    Server: A production-grade server would be used in lieu of the provided Flask server, which cannot handle production-level loads. I            would use NginX and Gunicorn to serve the webpages and handle corollary Python code 
    
    Docker: 
    
       A docker swarm could be implemented to allow multiple containers to handle the server loads between serving files and                      executing MongoDB queries
    
       Instead of mounting a docker volume to persist MongoDB data, as is done currently, a MongoDB persistent storage directory could            be used to allow access from different servers
    
    MongoDB Sync: 
    
      While many user details are currently synchronized between the SynapseFi servers and this project's included MongoDB database,              this functionality could be improved and expanded so as to allow any new user to find currently existing SynapseFi accounts              (currently, there is an ascribed level of trust between the Flask app and SynapseFi's user records, as the Flask app assumes            the users saved in the provided MongoDB database are exactly as they are in SynapseFi's servers)
      
      This would also mean fewer requests would have to be sent to SynapseFi's servers during user navigation of the site, allowing for          potentially faster load times
      
    Format:
    
      The app formatting would be tailored specifically towards mobile users
      
      The app formatting would be improved to further show advanced security measures are in place
      
      
  Security
  
  
    Sensitive Values: 
    
       Sensitive values would be hidden in configuration files to obfuscate
       
       Form values would be encrypted before sending to SynapseFi's servers
       
    Connection: Site would require https connections and have the required https certificate
    
