## 📚🤖 RoboLedger 🤖📚

Bookkeeping is the tedious process of categorizing transactions into their respective accounts.   This project looks to reduce the repetitive nature of bookkeeping by leveraging AI to reduce manual data entry.

### **How does RoboLedger Work?**

RoboLedger uses two models in order to automate bookkeeping. The first one is a baseline model that uses a dictionary of potential accounts depending on vendor memos. As the user adds more and more transactions into the database, these transactions are added into a Naive Bayes Model. The Naive Bayes Model overfit bias was minimized by making $n$ = 100. When the Naive Bayes Model reaches a confidence level $\geq$ 0.08, the Naive Bayes Model overrides the baseline model. This means that RoboLedger learns from User and gets better as time passes on.

### **What features does RoboLedger have?**

RoboLedger is a dynamic program that allows users to allow their own Chart of Accounts that can be categorized by the AI models. RoboLedger accepts QBO, CSV, and XLSX files converting them into an exportable profit & loss. RoboLedger cuts bookkeeping that is estimated to take ~1-1.5 hours into seconds with atonishing accuracy.

### **Who is the target audience for RoboLedger?**

RoboLedger is for everyone. However, businesses that can't afford a bookkeeping service would benefit greatly. Keep in mind, bookkeeping services for businesses with 100-300 transactions cost $300 to $500 per month. That can be unaffordable to businesses that need their financial statements right before tax season. If you are a sole proprietor or small business, you would be able to use this software for $0. 

### **How can I help the project?**

RoboLedger is a beta version of a grand project being developed. Since RoboLedger is made for small businesses, we like to keep the costs of the project as $0. However, we do accept donations. Donations as small as $1 help motivate our team to develop more tools for the general public to use. Your donations help us help you.

### Upcoming features:

1) User-friendly UI 👥
2) Carryover Profit & Loss 🗂️
3) Analytics Page 📈

### Credit Goes to: Andre Grigorian and Aidan Pineda


   

