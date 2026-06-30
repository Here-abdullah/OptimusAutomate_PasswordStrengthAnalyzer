
import tkinter as tk
from tkinter import ttk,messagebox
import re, math, secrets, string

COMMON={"password","123456","qwerty","admin","welcome","letmein","password123"}

def entropy(p):
    pool=0
    if re.search(r"[a-z]",p): pool+=26
    if re.search(r"[A-Z]",p): pool+=26
    if re.search(r"\d",p): pool+=10
    if re.search(r"[^A-Za-z0-9]",p): pool+=32
    return round(len(p)*math.log2(max(pool,1)),1)

def analyze(p):
    score=0
    tips=[]
    if len(p)>=12: score+=25
    else: tips.append("Use at least 12 characters.")
    if re.search(r"[a-z]",p): score+=10
    else: tips.append("Add lowercase letters.")
    if re.search(r"[A-Z]",p): score+=10
    else: tips.append("Add uppercase letters.")
    if re.search(r"\d",p): score+=10
    else: tips.append("Add numbers.")
    if re.search(r"[^A-Za-z0-9]",p): score+=15
    else: tips.append("Add symbols.")
    if p.lower() in COMMON:
        score=5
        tips.append("Password is commonly used.")
    if re.search(r"(.)\1\1",p):
        score-=10
        tips.append("Avoid repeated characters.")
    if any(x in p.lower() for x in ["1234","abcd","qwer"]):
        score-=10
        tips.append("Avoid sequential patterns.")
    score=max(0,min(score+20,100))
    if score<40: lvl="Weak"
    elif score<70: lvl="Medium"
    else: lvl="Strong"
    return score,lvl,entropy(p),tips

def gen():
    chars = string.ascii_letters + string.digits + string.punctuation
    pw = ''.join(secrets.choice(chars) for _ in range(16))

    entry.config(show="")      # <-- This is the fix

    entry.delete(0, tk.END)
    entry.insert(0, pw)

    check() 
   

def check():
    pw=entry.get()
    s,l,e,t=analyze(pw)
    bar["value"]=s
    result["text"]=f"{l} ({s}/100)\nEntropy: {e} bits"
    tips.delete("1.0",tk.END)
    if t:
        tips.insert(tk.END,"\n".join("• "+i for i in t))
    else:
        tips.insert(tk.END,"Excellent password!")

root=tk.Tk()
root.title("Advanced Password Strength Analyzer")
root.geometry("520x420")
tk.Label(root,text="Password",font=("Arial",13,"bold")).pack()
entry=tk.Entry(root,show="*",width=40,font=("Consolas",12))
entry.pack(pady=5)
ttk.Button(root,text="Analyze",command=check).pack()
ttk.Button(root,text="Generate Strong Password",command=gen).pack(pady=5)
bar=ttk.Progressbar(root,length=350,maximum=100)
bar.pack(pady=8)
result=tk.Label(root,font=("Arial",12))
result.pack()
tips=tk.Text(root,height=10,width=58)
tips.pack(pady=10)
root.mainloop()
