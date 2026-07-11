# 🏝️ InstaBay-Agentic-AI-Marketing

An Agentic AI Marketing Assistant built for the **Bright Brains IT Forward-Deployed / Agentic AI Engineer Technical Challenge**.

The application simulates an AI-powered marketing teammate that helps manage Instagram content for **InstaBay Resort & Spa** by generating bilingual posts, reviewing them, publishing (mock), analyzing engagement, and recommending improvements for future content.

---

## 🚀 Features

- 🎯 Brand-aware content generation
- 🌍 Bilingual Instagram posts (English & Arabic)
- 👤 Human approval before publishing
- 📢 Mock Instagram publishing workflow
- 📊 Engagement analytics
- 💡 AI-based optimization recommendations
- 🖥️ Interactive Streamlit interface

---

## 🏗️ Project Architecture

```
User
  │
  ▼
Planner Agent
  │
  ▼
Content Agent
  │
  ▼
Review Agent
  │
  ▼
Publisher Agent
  │
  ▼
Analytics Agent
  │
  ▼
Optimization Agent
```

The system follows an **Agentic AI workflow**, where each agent has a single responsibility.

---

## 🤖 Agents

### 🏷️ Brand Agent

Loads the resort identity from `brand_rules.json` including:

- Brand name
- Tone of voice
- Target audience
- Content pillars
- Hashtags

These rules are used to keep all generated content consistent.

---

### ✍️ Content Agent

Generates Instagram content using the LLM.

The generated content includes:

- English caption
- Arabic caption
- Call-to-action
- Relevant hashtags

---

### ✅ Review Agent

Provides a human approval step before publishing.

The post can be:

- Approved
- Rejected

No content is published without approval.

---

### 📢 Publisher Agent

Simulates publishing the approved post.

(Current implementation is a mock publisher.)

---

### 📊 Analytics Agent

Reads engagement data from:

```
data/engagement.csv
```

Calculates:

- Average Likes
- Average Comments
- Average Reach
- Best Performing Content

---

### 💡 Optimization Agent

Uses analytics insights to recommend improvements such as:

- Increase Reel content
- Continue high-performing content categories
- Improve future content strategy

---

## 🖥️ Streamlit Application

The Streamlit interface allows users to:

- Generate Instagram posts
- Review generated content
- Publish approved posts
- View analytics
- View optimization recommendations

Run the application using:

```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
InstaBay-AI-Marketing-Assistant
│
├── agents/
│   ├── analytics_agent.py
│   ├── brand_agent.py
│   ├── content_agent.py
│   ├── optimization_agent.py
│   ├── planner_agent.py
│   ├── publisher_agent.py
│   └── review_agent.py
│
├── data/
│   ├── brand_rules.json
│   ├── content_calendar.csv
│   └── engagement.csv
│
├── utils/
│   ├── llm.py
│   ├── helpers.py
│   └── prompts.py
│
├── app.py
├── requirements.txt
└── README.md
```

---

## 🛠️ Technologies Used

- Python
- Streamlit
- Hugging Face Inference API
- Requests
- Pandas
- JSON
- CSV

---

## ▶️ Installation

Clone the repository:

```bash
git clone https://github.com/your-username/InstaBay-AI-Marketing-Assistant.git
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it.

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
HF_API_KEY=your_api_key
HF_MODEL=Qwen/Qwen3-32B
```

Run the application:

```bash
streamlit run app.py
```

---

## 📈 Future Improvements

- Meta Graph API integration
- Automatic Instagram publishing
- Image generation for posts
- Content calendar automation
- Real engagement analytics
- Scheduled publishing
- Multi-platform support

---

## 👨‍💻 Author

**Mohamed Mahmoud Emam**

AI & Machine Learning Engineer

Computer Science Graduate

Data Science & Artificial Intelligence

---

## 📄 License

This project was developed as part of the Bright Brains IT Technical Challenge and is intended for educational and evaluation purposes.
