
## 🧠 My Reflection: Week 3 CTF Challenge – *Hacker’s Diary*

---

### 👨‍💻 Challenge Summary:

This week’s CTF challenge placed me in the shoes of a cybersecurity analyst. My mission was to investigate a suspicious access log file, detect signs of brute-force attacks, and retrieve a hidden flag left behind by an intruder. The process involved identifying abnormal login behavior, recognizing repeated login attempts, and using pattern-based log parsing techniques to extract a digital fingerprint of the attacker.

---

### 🛠️ Tools I Used: Custom Log Analysis Tool in Jupyter Notebook

To approach this challenge efficiently and align with the course’s hands-on methodology, I built a **log analysis tool using Python in Jupyter Notebook**. This decision allowed me to:

* **Follow the instructions** from the official Week 3 resources and videos
* Keep my log parsing clean, modular, and interactive
* Easily test, filter, and analyze log entries using Python libraries like `re` and `pandas`

The notebook was designed to:

* Analyze system access logs for **suspicious login behavior**
* Detect **brute-force patterns**
* Recover **leaked credentials**
* Automatically **extract flags** using pattern matching (`FLAG{...}`)

By building my own parser, I wasn’t just solving the problem—I was reinforcing my understanding of **log data structures**, **event categorization**, and **cyber threat detection workflows**.

---

### 🔍 My Thought Process & Strategy

#### **1. Understanding the Mission**

I carefully read the scenario: the attacker used a brute-force campaign, and somewhere among the logs, a flag was hidden. My first mental checklist:

* Watch out for repeated login failures
* Suspect usernames like `hackerX`, `hackerY`, or `unknown`
* Look for anything out of place in the password field

#### **2. Setting Up My Investigation**

Using my custom Jupyter Notebook:

* I loaded the `.txt` access logs into memory
* I separated entries into **successful** and **failed** logins
* Then, I filtered for **users with high-frequency activity** (a known brute-force sign)

#### **3. Recognizing Patterns**

Within the parsed results, I noticed several users—especially `hackerX`—trying multiple passwords across different IPs and time intervals. Many of the attempts were common passwords (`letmein`, `admin123`, etc.), which pointed to automated brute-forcing.

I wrote additional filters to track:

* Users with a mix of failures *then* a success
* IPs associated with repeated login behavior
* Passwords that didn’t look like passwords

#### **4. Finding the Flag**

Using my notebook’s regex pattern (`FLAG{.*}`), I caught the following anomaly:

```
2025-02-14 10:05:00 - Successful login from 192.168.1.133 - User: hackerX - Password: FLAG{}
```

💥 There it was. A successful login from `hackerX`—with the **flag embedded as a password**. A digital taunt left in plain sight.

---

### ✅ Final Output:

**CTF Flag Retrieved:** `FLAG{}`
**Method Used:** Custom Python log analyzer in Jupyter Notebook
**Detection Techniques:** Pattern recognition, brute-force tracking, regex-based flag extraction

---

### 🧠 What I Learned

* How to **apply theoretical cybersecurity principles** using practical log analysis tools
* How to detect **brute-force behavior** through login repetition and failure sequences
* How to use **Python + regex** to filter high-signal logs from noisy data
* The importance of building **reusable and flexible tools** like a Jupyter Notebook for scalable investigations

---

### 💭 Final Thoughts

This challenge went beyond just "finding a flag." It taught me how to think like an analyst. I built a custom log analysis notebook to stay aligned with the course's best practices, and in doing so, I gained firsthand experience in building incident response logic.

Seeing the flag appear from a well-built filter I coded myself felt empowering. I wasn't just solving a puzzle—I was simulating a real-world cyber forensic workflow. This was one of the most engaging challenges so far.


