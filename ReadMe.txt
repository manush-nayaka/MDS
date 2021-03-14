The Rest API is written in "FLask" framework and to store data the application uses "SQLITE3" 

Files and folder structure:
    MDS.py --> contains the entire code of the application
    database/MDS.db --> sqlite db file
    database/create_db.sql --> DDL file
    unit_test.py --> unit tests to APIs 
    log/MDS.log --> to log the application errors/info
    requirement.txt --> contains python dependencies for the application
    key_certificate/key.pem --> private key for https
    key_certificate/cert.pem --> self signed certificate
    openapi-yaml --> folder which contains openapi yaml file

Dependencies:
    System packages: python 2.7
    Application packages: Flask==1.0.3, pyOpenSSL==19.0.0

To install depencies:
    From the command line "./run_install.sh install"

To run unit tests:
    From the command line "./run_install.sh test"
 
To run the application:
    from the command line "./run_install.sh run"

API doc:
    API is documented in OAP 3.0 which can be found in the folder openapi-yaml and also exists in "https://app.swaggerhub.com/apis/manushmn/MDS/0.1"

