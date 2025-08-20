# Interactive Q&A System

A modern, AI-powered startup business guidance system with Matrix-themed UI and free LLM integration.

## 🚀 Project Overview

A complete full-stack application that provides intelligent answers to startup business questions using Groq's free LLM API. The system features a beautiful Matrix-inspired chat interface and comprehensive business guidance.

## ✨ Features

### 🎨 Frontend (Next.js + Matrix Theme)
- **Matrix-Inspired UI**: Green-on-black terminal aesthetic with glowing effects
- **Real-time Chat**: Responsive chat interface with typing indicators
- **Connection Monitoring**: Live backend connectivity status
- **TypeScript**: Full type safety and developer experience
- **Responsive Design**: Works perfectly on desktop and mobile
- **Fast Performance**: Next.js 15 with Turbopack for instant reloads

### 🤖 Backend (FastAPI + Groq LLM)
- **Free AI Integration**: Uses Groq's free API with llama-3.1-8b-instant
- **Startup Business Focus**: Specialized prompts for entrepreneurship guidance
- **FastAPI Framework**: High-performance async API with automatic docs
- **Health Monitoring**: Real-time system status and LLM connectivity
- **Swagger Documentation**: Interactive API documentation at `/docs`
- **Comprehensive Error Handling**: Robust error management and validation

## 🏗️ Project Structure

```
interactive_QA/
├── client/                          # Frontend (Next.js + TypeScript)
│   ├── src/
│   │   ├── app/                    # Next.js app router
│   │   │   ├── page.tsx           # Main application page
│   │   │   └── globals.css        # Matrix theme styles
│   │   ├── components/            # React components
│   │   │   └── QAInterface.tsx    # Main chat interface
│   │   ├── services/              # API communication
│   │   │   └── qa.ts             # Backend service integration
│   │   └── types/                 # TypeScript definitions
│   │       └── qa.ts             # Type definitions
│   ├── public/                    # Static assets
│   └── package.json              # Frontend dependencies
├── server/                         # Backend (FastAPI + Python)
│   ├── config/                    # Configuration management
│   │   └── settings.py           # Environment settings
│   ├── models/                    # Pydantic models
│   │   ├── requests.py           # Request validation
│   │   └── responses.py          # Response structures
│   ├── services/                  # Business logic
│   │   └── llm_service.py        # Groq LLM integration
│   ├── main.py                   # FastAPI application entry
│   ├── requirements.txt          # Python dependencies
│   └── test_api.py              # API testing script
├── .env.example                  # Environment variables template
├── PROMPTS.md                    # LLM prompts documentation
├── start.sh                       # Single-command startup script
├── requirements.txt               # Combined dependencies
├── .gitignore                    # Git ignore patterns
└── README.md                     # This documentation
```

## 🚀 Quick Start

### Prerequisites
- **Python 3.12+**
- **Node.js 18+**
- **Free Groq API Key** (get at [console.groq.com](https://console.groq.com))

### 1. Clone and Setup
```bash
git clone https://github.com/Carey99/interactive_QA --> HTTPS

or

git clone git@github.com:Carey99/interactive_QA.git --> SSH

cd interactive_QA

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
cd client
npm install
cd ..
```

### 2. Configure Environment
```bash
# Copy the environment template
cp .env.example .env

# Get your free Groq API key from https://console.groq.com
# Edit .env and add your API key:
GROQ_API_KEY=your_actual_groq_api_key_here
```

### 3. Start the System
```bash
# Single command to start both frontend and backend
./start.sh
```

### 4. Access the Application
- **Main Interface**: http://localhost:3000 (Matrix-themed Q&A chat)
- **API Documentation**: http://localhost:8001/docs (Swagger UI)
- **API Health**: http://localhost:8001/health

## 🎯 Usage Examples

Ask startup business questions like:

- "What documents do I need to travel from Kenya to Ireland?"
- "How do I register a business in the United States?"
- "What are the visa requirements for attending a conference in Germany?"
- "How do I open a business bank account in Canada?"
- "What are the legal requirements for starting a tech startup?"

## 🛠️ Manual Setup (Alternative)

If you prefer to start services manually:

### Backend
```bash
cd server
source ../.venv/bin/activate
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

### Frontend
```bash
cd client
npm run dev
```

## 🧪 Testing

### Automated Tests
```bash
# Test the API (ensure backend is running)
cd server
python test_api.py
```

### Manual Testing
1. Visit http://localhost:3000
2. Ask a business question
3. Verify you get an AI response
4. Check that the connection status shows as connected

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|---------|-------------|
| `/` | GET | API information and status |
| `/health` | GET | System health and LLM status |
| `/api/ask` | POST | Submit questions for AI responses |
| `/api/stats` | GET | Performance statistics |
| `/docs` | GET | Interactive API documentation |

## 🔧 Configuration

### Backend Settings (server/.env)
```bash
# Groq API (Required)
GROQ_API_KEY=your_api_key_here
GROQ_MODEL=llama-3.1-8b-instant

# Server Configuration
DEBUG=true
HOST=0.0.0.0
PORT=8001

# CORS (Frontend URLs)
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Frontend Settings (client/.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8001
```

## � Troubleshooting

### Common Issues

1. **"LLM service error"**
   - Verify Groq API key in `server/.env`
   - Check internet connection
   - Ensure API key has sufficient credits

2. **"Address already in use"**
   - The startup script automatically handles port conflicts
   - Or manually kill processes: `pkill -f uvicorn`

3. **Connection shows "disconnected"**
   - Wait 30 seconds for health check cycle
   - Verify backend is running on port 8001
   - Check browser console for errors

4. **Module not found errors**
   - Activate virtual environment: `source .venv/bin/activate`
   - Reinstall dependencies: `pip install -r requirements.txt`

### Development Tips

- **Backend Logs**: Check backend.log for detailed error information
- **Frontend Logs**: Check browser console for client-side errors
- **API Testing**: Use http://localhost:8001/docs for interactive testing
- **Health Monitoring**: Monitor http://localhost:8001/health

## 🌟 Key Features Highlight

### Matrix Theme
- Authentic terminal look with green-on-black color scheme
- Glowing text effects and smooth animations
- Courier New monospace font for authentic terminal feel

### AI Integration
- Free, high-quality responses using Groq's llama-3.1-8b-instant
- Specialized business guidance prompts
- Confidence scoring and response time tracking

### Developer Experience
- Single-command startup with `./start.sh`
- Comprehensive error handling and logging
- Interactive API documentation
- TypeScript for type safety

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**Built with ❤️ for entrepreneurs and startup founders**

*Need help? Create an issue or check the troubleshooting section above.*

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Frontend Setup

1. Navigate to the client directory:
```bash
cd client/
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

### Environment Configuration

Create a `.env.local` file in the client directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:3001
NODE_ENV=development
```

## 🛠️ Technology Stack

### Frontend
- **Framework**: Next.js 15 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Build Tool**: Turbopack

### Backend (Planned)
- **Runtime**: Node.js
- **Framework**: Express.js or Fastify
- **Language**: TypeScript
- **AI/ML**: Custom LLM integration
- **Database**: PostgreSQL/SQLite

## 📦 Key Components

### QAInterface Component
The main chat interface that handles:
- Message display and management
- User input and form submission
- Loading states and error handling
- Backend connectivity status
- Real-time chat experience

### QAService
API service layer that manages:
- Question submission to backend
- Health checks and connectivity
- Error handling and fallbacks
- Response processing

## � Assessment Requirements Checklist

✅ **Complete source code** - Full-stack application with frontend and backend  
✅ **Documentation of prompts used with the LLM** - See `PROMPTS.md`  
✅ **Setup instructions in README.md** - Comprehensive setup guide above  
✅ **Environment variable template** - See `.env.example` file  

### Additional Features Included
✅ **Interactive Swagger Documentation** - Available at `/docs`  
✅ **Health Monitoring** - Real-time system status  
✅ **Error Handling** - Comprehensive error management  
✅ **Type Safety** - Full TypeScript implementation  
✅ **Testing Scripts** - Automated API testing  
✅ **Production Ready** - Single-command deployment  

## 🔄 Development Status

### Project Complete ✅
- ✅ Frontend application complete with Matrix theme
- ✅ Modern chat interface implemented  
- ✅ TypeScript configuration
- ✅ Backend API with FastAPI
- ✅ LLM integration with Groq
- ✅ Real-time health monitoring
- ✅ Comprehensive error handling
- ✅ Single-command startup
- ✅ Complete documentation

## 🤝 Contributing

## 📝 Scripts

### Frontend (client/)
```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run ESLint
```

## 🔧 Configuration

- **TypeScript**: Configured with strict mode
- **ESLint**: Next.js recommended rules
- **Tailwind**: Custom configuration with dark mode
- **Next.js**: App router with TypeScript

## 📄 License

This project is for educational purposes.

## 🎯 Goals

Building this system step-by-step to understand:
- Modern frontend development with Next.js
- API design and backend architecture
- LLM integration and AI system design
- Full-stack application development
- Real-time communication patterns
