# WhatsApp Unsaved Chat Cleaner

This Python automation script deletes **WhatsApp chats with unsaved contacts** (numbers only) using **Selenium and WhatsApp Web**.  
It automatically scans your chats, detects numbers without names, and deletes their chats safely.

---

## 🚀 Features
- ✅ Detects chats with **unsaved phone numbers** only.
- ✅ Opens the **context menu** and clicks **Delete chat** automatically.
- ✅ Confirms deletion with the **red Delete button**.
- ✅ Skips saved contacts to keep important chats safe.
- ✅ Easily extendable to **log deleted chats into a CSV file**.

---

## 📦 Requirements

Before running the script, ensure you have the following:

1. **Python 3.10+** installed  
2. **Google Chrome** (latest version)  
3. **ChromeDriver** (auto-managed with `webdriver-manager`)  
4. Install required Python packages:

```bash
pip install selenium webdriver-manager
