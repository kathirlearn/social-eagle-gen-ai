# 🚀 How to Run the Project

Follow the steps below to run the RAG-based chatbot locally.

---

## 1️⃣ Clone the Repository

```bash
git clone <your-repository-url>
cd rag-chatbot

-- 
## 2️⃣ Create Virtual Environment

python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows


## 3️⃣ Install Dependencies
pip install -r requirements.txt


## 4️⃣ Configure Environment Variables
cp .env.example .env

## update your api keys
OPENAI_API_KEY=your_openai_api_key
SERPAPI_API_KEY=your_serpapi_api_key

## 5️⃣ Run the Application
streamlit run app.py

