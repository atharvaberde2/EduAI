# EduAI - Interactive Educational AI Platform

An innovative web-based educational platform that combines AI-powered tutoring with interactive learning games to provide personalized education experiences.

## 🌟 Features

### AI Tutors
- **Sam** - Homework Helper: Provides hints and step-by-step guidance for homework problems
- **Joe** - Concept Explainer: Breaks down complex ideas into simple, understandable pieces
- **Russell** - Inclusive Tutor: Specialized for learners with disabilities, using visual metaphors and patient explanations

### Interactive Learning Games
- **Charades** - AI-powered word guessing game with educational themes
- **Detective** - Topic-based mystery solving game that teaches through quiz questions


### Personalized Learning
- Adaptive tutoring based on individual learning styles
- Visual learning support for students with different needs
- Patient and encouraging AI interactions

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)
- Google Generative AI API key
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd hackathon
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   Open your browser and go to `http://localhost:5000`

## 📁 Project Structure

```
hackathon/
├── app.py                  # Main Flask application
├── eduai_users.db         # SQLite database
├── templates/             # HTML templates
│   ├── index (2).html     # Main homepage
│   ├── sam.html          # Sam tutor interface
│   ├── joe.html          # Joe tutor interface
│   ├── russell.html      # Russell tutor interface
│   ├── charades.html     # Charades game
│   ├── detective.html    # Detective game
│   └── ...               # Other templates
├── venv/                 # Virtual environment
└── README.md            # This file
```

## 🎮 How to Use

### AI Tutors
1. Navigate to the desired tutor (Sam, Joe, or Russell)
2. Click "Start Chat" to begin your tutoring session
3. Ask questions or request help with any subject
4. Each tutor has a unique teaching style:
   - **Sam**: Gives hints first, then guides step-by-step
   - **Joe**: Explains concepts in simple 100-word chunks
   - **Russell**: Uses visual metaphors and patient explanations

### Games
1. **Charades**: Choose a topic and play word-guessing with AI
2. **Detective**: Solve mysteries by answering topic-based questions
3. **Quiz Shows**: Test your knowledge in various subjects

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **AI Models**: 
  - Google Generative AI (Gemini 2.0 Flash)
  - OpenAI GPT-4
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite
- **Other**: Flask-CORS, python-dotenv

## 🔧 Configuration

### API Keys
The application requires two API keys:
1. **Google Generative AI API**: Used for most AI interactions
2. **OpenAI API**: Used for specific features like the charades game

### Database
The application uses SQLite with `eduai_users.db` for user data storage.

## 🎯 Game Rules

### Charades
- Choose a topic at the start
- AI or user takes turns giving hints
- 3 attempts to guess each word
- First to reach 5 points wins

### Detective
- Choose a subject area
- Solve mystery by answering quiz questions correctly
- Minimum 5 clues provided
- Progress story by answering correctly

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google Generative AI for providing the Gemini API
- OpenAI for GPT-4 API access
- Flask community for the excellent web framework
- All contributors and testers

## 🐛 Known Issues

- API keys are currently hardcoded in some places (should be moved to environment variables)
- Error handling could be improved for API failures
- Some template files have versioned names that could be cleaned up

## 📞 Support

For support, please open an issue in the repository or contact the development team.

---

Made with ❤️ for educational innovation 
