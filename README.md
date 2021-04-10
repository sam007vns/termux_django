# termux_django

Its a Django application developed to run on Turmux, using this application you can remotely control all the features, functions of your android phone.<br>
Note - If you try to run this on your PC, you will get lots of invalid syntex, errors ... thats not error's. This application is designed only for Turmux and will
run very smoothly in it.

How to install?

1. You should be having Turmux and Turmux API application installed on your Android Device, you can download both of them from playstore.

2.Install Python - pkg install python

3.Install Django - pip insatll Django

4.Clone the Repo - https://github.com/sam007vns/termux_django

5.Move to termux_django - cd termux_django

6.Run Migrations- python3 manage.py makemigrations 

7.Migrate- python3 manage.py migrate

8.Create Super User- python3 manage.py createsuperuser

9.Run server- python3 manage.py runserver 0.0.0.0:8000 --noreload

You can control your android phone functions and features  using this appliction in the network and over the network.

Controlling Over The Network?

1. Install ngrok(Used for Port Forwarding)
    Steps to install ngrok:- 
      1. pkg install zip wget -y
      2. Now type the below command as it is to download Ngrok in your Termux.
      3. wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip
      4. unzip ngrok-stable-linux-arm.zip
      5. chmod +x ngrok
      6. create an account on ngrok.io and get the AUTH_TOKEN
      7. set auth token in turmux-    ./ngrok authtoken YOUR_AUTH_TOKEN_HERE
2. After setting up ngrok, start the termux_django server on one window of turmux, run the command as described on 9 to start server
3. Open another turmux window and navigate to home or where ngrok binary lives then run-  ./ngrok http 8000
4. This will start a tunnel which points to your local django server remember you need to start ngrok on the port where django server is running in order to access 
   your android phone over the internet, here we are running django on port 8000 and ngrok is also started at 8000
   Make sure your android phone wifi hotspot is tuened on, without that ngrok will not start.
5. Now you will see some web addresses displayed on the page where ngrok is running it will be like https://someString.ngrok.io
6. Access the webaddress which you have got from ngrok page, from any PC, MOBILE or anything which has a browser.

** THIS PROJECT IS ONLY MADE FOR EDUCATIONAL PURPOSES **

I will be adding some more features like :- 1.sms messaging system 2. notification system, 3.Remote command execution, 4. File System Traversal and more...
