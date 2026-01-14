# 🧠 AI Resume Analyzer & Interview Prep System

An intelligent full-stack application that analyzes resumes using AI and helps job seekers prepare for interviews with personalized questions and real-time feedback.

## 🌟 Features

- **AI-Powered Resume Analysis**: Get detailed feedback on your resume with scores, strengths, weaknesses, and actionable suggestions
- **Interview Question Generation**: Receive personalized interview questions based on your actual experience and skills
- **Real-Time Answer Evaluation**: Practice answering questions and get instant AI feedback with improvement tips
- **Multi-Format Support**: Upload resumes in PDF, DOCX, or TXT format
- **Beautiful UI**: Modern, responsive interface with smooth animations

## 🛠️ Tech Stack

### Backend
- **Python 3.10+**
- **FastAPI** - Modern web framework for building APIs
- **Groq AI (Llama 3.3)** - AI model for natural language processing
- **PyPDF2** - PDF text extraction
- **python-docx** - DOCX file processing

### Frontend
- **React.js** - UI library
- **Axios** - HTTP client
- **Lucide React** - Icon library
- **CSS3** - Styling with animations

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- Node.js 16 or higher
- npm or yarn
- Groq API key (free at [console.groq.com](https://console.groq.com))

### Backend Setup

1. Clone the repository:
```bash
git clone https://github.com/Devashya/resume-analyzer.git
cd resume-analyzer
```

2. Navigate to backend and create virtual environment:
```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file in `backend/` folder:
```
GROQ_API_KEY=your_groq_api_key_here
```

5. Run the backend server:
```bash
uvicorn main:app --reload
```

Backend will run on `http://127.0.0.1:8000`

### Frontend Setup

1. Open a new terminal and navigate to frontend:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

Frontend will run on `http://localhost:3000`

## 🚀 Usage

1. **Upload Resume**: Click the upload box and select your resume (PDF, DOCX, or TXT)

2. **Analyze Resume**: 
   - Click "Analyze Resume" to get AI feedback
   - View your overall score, strengths, weaknesses, and suggestions
   - See missing keywords and formatting feedback

3. **Practice Interviews**:
   - Click "Generate Interview Questions" to get personalized questions
   - Type your answer in the text area
   - Submit and receive instant AI evaluation with improvement tips
   - Navigate through multiple questions

## 🔑 Getting Groq API Key

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Navigate to "API Keys" section
4. Create a new API key
5. Copy and paste it in your `.env` file

**Note**: Groq offers a generous free tier perfect for development and personal use.

## 🏗️ Project Structure
```
resume-analyzer/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   ├── .env                 # Environment variables (not in repo)
│   └── uploads/             # Temporary upload folder
├── frontend/
│   ├── src/
│   │   ├── App.js          # Main React component
│   │   ├── App.css         # Styling
│   │   └── index.js        # Entry point
│   ├── public/
│   └── package.json        # Node dependencies
├── .gitignore
└── README.md
```

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Devashya Patel**
- Location: Dallas, TX
- Email: devashya.1312@gmail.com
- LinkedIn: https://www.linkedin.com/in/devashya-patel
- GitHub: https://github.com/Devashya

## 🙏 Acknowledgments

- [Groq](https://groq.com) for providing fast and free AI inference
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [React](https://react.dev/) for the UI library

## 📊 Project Status

✅ **Completed Features:**
- Resume analysis with AI
- Interview question generation
- Answer evaluation
- Multi-format file support
- Responsive UI

🚧 **Potential Enhancements:**
- Job description matcher
- Resume template generator
- Save analysis history
- Export reports as PDF
- Multi-language support

---

⭐ If you found this project helpful, please consider giving it a star!
```

---