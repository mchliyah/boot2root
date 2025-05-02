# boot2root

## Summary
This project is a computer security exercise designed to teach exploitation techniques and privilege escalation by becoming the root user on a target server.

## 📌 Objectives
- Become root (UID 0) on the server using **2 different methods**.
- Use real exploits, scripts, or techniques to escalate privileges.
- we must be in a real shell as root (e.g., able to run `whoami`, `id`).

## 🧾 General Instructions
- we use the **provided ISO** in a 64-bit virtual machine.
- we'r **not** allowd to modify or exploit the ISO, GRUB, or boot process.
- No brute-forcing allowed.

## ✅ Mandatory Part
- **Two distinct root access methods** are required.
- Each method must be documented in separate write-ups:
  - Step-by-step details.
  - Explain tools/scripts used.
- **Do not include binaries** in submission.
- scripts are placed in a `/scripts` folder.

### Example Folder Structure
```
/project-root
│
├── writeup1.md
├── writeup2.md
├── writeupx.md
└── scripts/
    ├── exploit1.sh
    ├── exploit2.py
    └── ...
```
### 🔗 Writeups

- [Writeup 1](./writeups/writeup1.md)
- [Writeup 2](./writeups/writeup2.md)

## ❗ Rules & Warnings
- **No ISO file or GRUB exploitation allowed.**
- we are **not** allowed to include project-internal files; download them live during defense.

## Bonus Part
- find 3 more ways to become root, that's it .
