# Explain Firewall

## What is a Firewall?

A **firewall** is a network security component that monitors and filters network traffic based on a set of rules.

Think of it as a **security guard**:

```
Internet
    |
    v
+----------------+
|    Firewall    |
+----------------+
 Allow | Deny
    |       |
    v       X
 Application
```

Its job is to inspect packets and decide whether to:

* ✅ Allow the traffic
* ❌ Drop the packet silently
* 🚫 Reject the connection (send an error)

---

## How a Linux Firewall Works

Every network packet entering or leaving the Linux kernel passes through the **Netfilter** framework.

```
Incoming Packet
       |
       v
+------------------+
| Linux Kernel     |
| Netfilter        |
+------------------+
       |
       v
Firewall Rules
       |
  Allow / Drop
       |
       v
Application
```

The kernel checks firewall rules before delivering packets to applications.

---

## Linux Firewall Stack

```
Application
      ▲
      │
TCP/IP Stack
      ▲
      │
Netfilter (Kernel)
      ▲
      │
iptables / nftables
      ▲
      │
User
```

* **Netfilter** → packet filtering framework inside the kernel
* **iptables** → older userspace tool to configure Netfilter
* **nftables** → modern replacement for iptables
* **ufw** → beginner-friendly wrapper around iptables/nftables

---

# Netfilter Hooks

Packets travel through hooks inside the kernel.

```
                Incoming
                    |
             PREROUTING
                    |
        +-----------+----------+
        |                      |
     Forward               Local Machine
        |                      |
    FORWARD                 INPUT
        |                      |
        v                      v
   Other machine        Local Process

Local Process
      |
   OUTPUT
      |
 POSTROUTING
      |
    Network
```

---

# Firewall Chains

| Chain   | Purpose                                      |
| ------- | -------------------------------------------- |
| INPUT   | Incoming packets to this machine             |
| OUTPUT  | Outgoing packets                             |
| FORWARD | Packets passing through the machine (router) |

---

# Install Firewall

Ubuntu:

```bash
sudo apt update
sudo apt install ufw
```

Enable it:

```bash
sudo ufw enable
```

Status:

```bash
sudo ufw status
```

---

# Allow SSH

```bash
sudo ufw allow 22/tcp
```

Equivalent iptables:

```bash
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
```

Meaning

```
-A INPUT     -> append to INPUT chain
-p tcp       -> TCP packets
--dport 22   -> destination port 22
-j ACCEPT    -> allow
```

---

# Block Port 80

```bash
sudo iptables -A INPUT -p tcp --dport 80 -j DROP
```

or

```bash
sudo ufw deny 80
```

---

# Allow Only One IP

```bash
sudo iptables -A INPUT \
    -p tcp \
    -s 192.168.1.10 \
    --dport 22 \
    -j ACCEPT
```

Block everyone else:

```bash
sudo iptables -A INPUT \
    -p tcp \
    --dport 22 \
    -j DROP
```

---

# Rate Limiting SSH

```bash
sudo iptables -A INPUT \
    -p tcp \
    --dport 22 \
    -m limit \
    --limit 5/minute \
    -j ACCEPT
```

---

# Default Policy

Allow nothing:

```bash
sudo iptables -P INPUT DROP
sudo iptables -P OUTPUT ACCEPT
sudo iptables -P FORWARD DROP
```

---

# Viewing Rules

```bash
sudo iptables -L -v
```

Example:

```
Chain INPUT

ACCEPT tcp -- anywhere anywhere tcp dpt:ssh
DROP   tcp -- anywhere anywhere tcp dpt:http
```

---

# nftables (Modern Linux Firewall)

Create a table:

```bash
sudo nft add table inet filter
```

Create INPUT chain:

```bash
sudo nft add chain inet filter input \
'{ type filter hook input priority 0 ; }'
```

Allow SSH:

```bash
sudo nft add rule inet filter input tcp dport 22 accept
```

Block HTTP:

```bash
sudo nft add rule inet filter input tcp dport 80 drop
```

Show rules:

```bash
sudo nft list ruleset
```

---

# Example: Simple Home Server Firewall

```text
Default:
    DROP everything

Allow:
    SSH (22)
    HTTPS (443)

Block:
    HTTP (80)
    Telnet (23)
```

Commands:

```bash
sudo iptables -P INPUT DROP

sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT

sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT

sudo iptables -A INPUT -p tcp --dport 80 -j DROP

sudo iptables -A INPUT -p tcp --dport 23 -j DROP
```

---

# How the Kernel Processes a Packet

Suppose a packet arrives at port 22:

```
Packet Arrives
      |
      v
Netfilter INPUT chain
      |
      v
Rule 1: Allow SSH? ------ Yes ----> ACCEPT
      |
      No
      |
Rule 2: Block HTTP?
      |
      No
      |
Default Policy
      |
     DROP
```

The firewall evaluates rules **from top to bottom**. The **first matching rule** determines the action, so rule order is important.

---

## Summary

* A firewall filters network traffic according to configured rules.
* Linux uses the **Netfilter** framework in the kernel to inspect packets.
* **iptables** is the traditional interface; **nftables** is the modern replacement.
* Rules are organized into chains such as **INPUT**, **OUTPUT**, and **FORWARD**.
* Common actions include **ACCEPT**, **DROP**, and **REJECT**.
* Always place more specific rules before broader ones, since packets are processed sequentially until the first match.

