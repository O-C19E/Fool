+ This is an Anti-Piracy system to see if it can Fool the crackers<br/>
+ The encryption is not the encryption in standard terms but acutal randomization of blocks of the execution file<br/>
+ As a result the crackers will have an extremely hard time to make sense of the code if we add code obfuscation too<br/>

Tested Operating System: Linux

File uses: 

- auto_gen.py

Could create the database if not existed <br/>
Simply select the original executable which you want to scramble then its relative license key with its activation key will be saved in the database<br/>
For convience the licence key can seen in the output executable's file name in /build/*.exe<br/>

- db_check.py

Check the license database by selecting [1] and activation logs by selecting [2]<br/>
license table consists of license key, executable hash, activation key, user fingerprint hash<br/>
activation logs table consists of id, license key, fingerprint hash, timestamp in date format<br/>

- server.py

The server extracts and compares the data in database with user request

- launcher.py

By entering the license key<br/>
By selecting the correct scrambled executable<br/>
When all license key, executable hash, device fingerprint hash matches the server will validate the user and send the activation key<br/>

[Note]

- The activation key after entering in memory gets immediately deleted after its use
- Anti-debugger system are used to try to prevent memory dumping to a certain extent
