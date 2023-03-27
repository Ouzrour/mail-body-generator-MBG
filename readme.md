![By.Ouzrour](/logo.png)
# Mail Body Generator
## Why MBG ?
The main idea of this tool is to be used after using 
Mailstyler . 
## How it work ?
1. Export The "html" in a folder named "in" in the same directory as this py project
2. Complete the **.env** file with your personnel API keys
3. Run **"mail_body_generator.py"** for the unencrypted body // **"mail_body_generator_encrypt.py"** for the Encrypted version ( after that choose the method that you want ) 
4. Inject the Copied HTML in the body case of your app .
## Steps to use it ? 
1. You must export your project in MailStyler as "**_name_of_project.html_**" ( The images gonna be on the same folder , on another folder named **"file_" + _name_of_project_** ) and save it on the folder "**MBG/in**"
2. run "**MBG/mail_body_generator.py**" for _**Unencrypted**_ result // "**MBG/mail_body_generator_encrypt**" for _**encrpyted**_ result
3. Paste on the Application that you use .
4. Enjoy ! 
## How to install it ?
1. install all dependencies :
```cmd
pip install -r requirements.txt
```
2. Complete **.env** file
3. run **"mail_body_generator.py"** or **"mail_body_generator_encrypt.py"**
