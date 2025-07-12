# Almanack

A full-stack web application built with Next.js frontend and FastAPI backend.

## 🏗️ Project Structure

```
almanack/
├── frontend/          # Next.js application
│   ├── src/
│   ├── public/
│   └── package.json
├── backend/           # FastAPI server
│   ├── main.py
│   ├── requirements.txt
│   └── README.md
└── package.json       # Root package.json for development scripts
```

## 🚀 Quick Start

### Prerequisites
- Node.js (v18 or higher)
- Python (v3.8 or higher)
- npm or yarn

### Installation

1. **Install all dependencies:**
```bash
npm run install:all
```

2. **Start both servers (frontend + backend):**
```bash
npm run dev
```

This will start:
- **Frontend**: http://localhost:3000 (Next.js)
- **Backend**: http://localhost:8000 (FastAPI)

### Individual Server Commands

**Frontend only:**
```bash
npm run dev:frontend
```

**Backend only:**
```bash
npm run dev:backend
```

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔧 Development

### Frontend (Next.js)
- Located in `frontend/`
- Built with TypeScript and Tailwind CSS
- Hot reloading enabled

### Backend (FastAPI)
- Located in `backend/`
- Python-based REST API
- Automatic API documentation
- CORS configured for frontend

## 📝 Available Scripts

- `npm run dev` - Start both frontend and backend in development mode
- `npm run dev:frontend` - Start only the frontend
- `npm run dev:backend` - Start only the backend
- `npm run build` - Build the frontend for production
- `npm run start` - Start the frontend in production mode
- `npm run install:all` - Install all dependencies for both frontend and backend

## 🌐 Ports

- **Frontend**: 3000 (Next.js development server)
- **Backend**: 8000 (FastAPI server)

## 📄 License

MIT
