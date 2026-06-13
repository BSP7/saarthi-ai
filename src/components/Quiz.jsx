import React, { useEffect, useMemo, useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import subjectQuestions from '../data/subjectQuestions.json'
import quizQuestions from '../data/quizQuestions.json'

// Simple scoring: sum of selected option weights
export default function Quiz() {
  const { t } = useTranslation()
  const navigate = useNavigate()
  const location = useLocation()
  const [answers, setAnswers] = useState({})

  // try to recover from sessionStorage if user refreshed mid-flow
  const stored = (() => {
    try { return JSON.parse(sessionStorage.getItem('saarthi_state')) } catch (e) { return null }
  })()

  const mode = location.state?.mode || stored?.mode || 'completed'
  const marksPayload = location.state?.payload || stored?.payload

  const questions = useMemo(() => {
    if (mode === 'studying') {
      // Pick subject-based questions relevant to marks and goal
      const goal = marksPayload?.goal || 'engineering'
      const pool = subjectQuestions[goal] || []
      return pool.slice(0, 5)
    }
    return quizQuestions.slice(0, 6)
  }, [mode, marksPayload])

  useEffect(() => {
    if (!questions.length) return
    // Pre-fill answers with null and try to restore saved answers
    const init = {}
    questions.forEach((q, idx) => { init[idx] = null })
    let saved = null
    try { saved = JSON.parse(sessionStorage.getItem('saarthi_answers')) } catch (e) { saved = null }
    if (saved) {
      // only restore keys that exist in current question set
      Object.keys(init).forEach((k) => { if (saved[k] != null) init[k] = saved[k] })
    }
    setAnswers(init)
  }, [questions])

  const allAnswered = Object.values(answers).every((v) => v !== null)

  const handleSelect = (qIndex, weight) => {
    setAnswers((a) => {
      const next = { ...a, [qIndex]: weight }
      try { sessionStorage.setItem('saarthi_answers', JSON.stringify(next)) } catch (e) { }
      return next
    })
  }

  const handleSubmit = () => {
    // Score calculation
    const baseScore = Object.values(answers).reduce((acc, w) => acc + (Number(w) || 0), 0)

    // If studying, also consider marks
    let marksScore = 0
    if (mode === 'studying' && marksPayload?.marks) {
  const { math = 0, science = 0, english = 0 } = marksPayload.marks
  // secondLanguage isn't a numeric mark in marks; check separate field on payload
  const secondLang = marksPayload?.secondLanguage
      // Weighted sum to bias towards STEM for engineering/medicine
      const bias = marksPayload.goal
  if (bias === 'engineering') marksScore = math * 0.5 + science * 0.4 + english * 0.1
  else if (bias === 'medicine') marksScore = science * 0.6 + english * 0.3 + (math * 0.1)
  else if (bias === 'commerce') marksScore = math * 0.4 + english * 0.3 + (secondLang ? 10 : 0)
  else marksScore = english * 0.4 + (secondLang ? 10 : 0) + math * 0.2
      marksScore = marksScore / 10 // scale down
    }

    const total = baseScore + marksScore

  // persist final computed score and clear answers (keep state for result page)
  try { sessionStorage.setItem('saarthi_last_result', JSON.stringify({ mode, total, goal: marksPayload?.goal })) } catch (e) { }
  try { sessionStorage.removeItem('saarthi_answers') } catch (e) { }
  navigate('/result', { state: { mode, total, goal: marksPayload?.goal } })
  }

  return (
    <div className="card space-y-4">
      <h2 className="text-xl font-semibold">{mode === 'studying' ? t('subject_quiz') : t('interest_quiz')}</h2>
      {questions.map((q, idx) => (
        <div key={idx} className="space-y-2">
          <div className="font-medium">{q.question}</div>
          <div className="grid gap-2 sm:grid-cols-2">
            {q.options.map((opt, i) => (
              <label key={i} className={`border rounded p-2 cursor-pointer ${answers[idx] === opt.weight ? 'border-blue-600' : 'border-gray-200'}`}>
                <input
                  type="radio"
                  name={`q-${idx}`}
                  className="mr-2"
                  onChange={() => handleSelect(idx, opt.weight)}
                />
                {opt.label}
              </label>
            ))}
          </div>
        </div>
      ))}

      <button className="btn" disabled={!allAnswered} onClick={handleSubmit}>{t('see_results')}</button>
    </div>
  )
}