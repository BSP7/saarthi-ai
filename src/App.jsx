import React, { useState } from 'react'
import { Routes, Route, Link, useNavigate, useLocation } from 'react-router-dom'
import Home from './components/Home.jsx'
import MarksForm from './components/MarksForm.jsx'
import Quiz from './components/Quiz.jsx'
import Result from './components/Result.jsx'
import { useTranslation } from 'react-i18next'

export default function App() {
  const { i18n, t } = useTranslation()
  const navigate = useNavigate()
  const location = useLocation()
  const [mode, setMode] = useState('') // 'studying' | 'completed'

  const changeLanguage = (lng) => {
    i18n.changeLanguage(lng)
  }

  return (
    <div className="min-h-screen">
      <header className="bg-white border-b">
        <div className="container flex items-center justify-between py-4">
          <Link to="/" className="text-xl font-semibold">Saarthi AI</Link>
          <div className="flex items-center gap-3">
            <select
              aria-label="language"
              className="select"
              value={i18n.language}
              onChange={(e) => changeLanguage(e.target.value)}
            >
              <option value="en">English</option>
              <option value="hi">हिंदी</option>
              <option value="kn">ಕನ್ನಡ</option>
            </select>
          </div>
        </div>
      </header>

      <main className="container py-6">
        <Routes>
          <Route path="/" element={<Home setMode={setMode} />} />
          <Route path="/marks" element={<MarksForm onContinue={(payload) => navigate('/quiz', { state: { mode: 'studying', payload } })} />} />
          <Route path="/quiz" element={<Quiz />} />
          <Route path="/result" element={<Result />} />
        </Routes>
      </main>

      <footer className="container py-8 text-center text-sm text-gray-500">
        {t('footer')} • {t('hackathon_ready')}
      </footer>
    </div>
  )
}