This is an Anti-Piracy system to see if it can Fool the crackers<br/>
The encryption is not the encryption in standard terms but acutal randomization of blocks of the execution file<br/>
As a result the crackers will have an extremely hard time to make sense of the code if we add code obfuscation too<br/>

* The system works by encrypting the working exe file by randomizing its blocks based on a Product Key
* Tested OS: Linux

-- To encrypt

````python3 main.py main.exe -S scrambled.exe -K HE12-43NK-AIDD-N986````

+ main.py has the actual logic
+ main.exe is used to read total lines, total words, total characters, most frequent word and average words per line from sample.txt
+ -S stands for Scramble
+ scrambled.exe is the encrypted result
+ -K stands for Key
+ HE12-43NK-AIDD-N986 is the used key and using different keys will result in different variations

-- To decrypt

````python3 main.py scrambled.exe -R restore.exe -K HE12-43NK-AIDD-N986````

+ scrambled.exe is the encrypted exe file
+ -R stands for Restore
+ restore.exe is the decrypted result
+ -K is for key and HE12-43NK-AIDD-N986 is used as the decryption key

