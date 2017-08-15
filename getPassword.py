import base64
import getpass

print("Your password must contain at least 7 characters, at least one uppercase and one lowercase and one digit!")
current_user_passwd=getpass.getpass(prompt="Please enter your password: "); 
#print(current_user_passwd)
b=current_user_passwd.encode('ascii')
encrypted_passwd=base64.b64encode(b)
print(encrypted_passwd)

f=open("tmpPasswd.txt",'wb')
f.write(encrypted_passwd)
f.close()

