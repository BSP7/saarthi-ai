import React, { useState } from 'react'
import { useTranslation } from 'react-i18next'

export default function MarksForm({ onContinue }) {
  const { t } = useTranslation()

  const [marks, setMarks] = useState({ math: '', science: '', english: '', secondLanguage: '' })
  const [goal, setGoal] = useState('engineering')
  const [secondLanguage, setSecondLanguage] = useState('kannada')

  const handleChange = (e) => {
    const { name, value } = e.target
    setMarks((m) => ({ ...m, [name]: value }))
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    const normalizedMarks = Object.fromEntries(Object.entries(marks).map(([k,v]) => [k, Number(v) || 0]))
    // attach second-language separately (marks.secondLanguage may be empty string)
    const payload = { marks: normalizedMarks, goal, secondLanguage }
  // persist the chosen mode + payload so refresh won't lose progress
  try { sessionStorage.setItem('saarthi_state', JSON.stringify({ mode: 'studying', payload })) } catch (e) { /* ignore */ }
  onContinue(payload)
  }

  return (
    <form onSubmit={handleSubmit} className="card space-y-4">
      <h2 className="text-xl font-semibold">{t('enter_marks')}</h2>
      <div>
        <label className="label" htmlFor="math">{t('math')}</label>
        <input id="math" name="math" type="number" min="0" max="100" className="input" value={marks.math} onChange={handleChange} required />
      </div>
      <div>
        <label className="label" htmlFor="science">{t('science')}</label>
        <input id="science" name="science" type="number" min="0" max="100" className="input" value={marks.science} onChange={handleChange} required />
      </div>
      <div>
        <label className="label" htmlFor="english">{t('english')}</label>
        <input id="english" name="english" type="number" min="0" max="100" className="input" value={marks.english} onChange={handleChange} required />
      </div>
      <div>
        <label className="label" htmlFor="secondLanguage">{t('second_language')}</label>
        <select id="secondLanguage" className="select" value={secondLanguage} onChange={(e) => setSecondLanguage(e.target.value)}>
          <option value="kannada">{t('kannada')}</option>
          <option value="hindi">{t('hindi')}</option>
          <option value="telugu">{t('telugu')}</option>
        </select>
      </div>
      <div>
        <label className="label" htmlFor="goal">{t('desired_goal')}</label>
        <select id="goal" className="select" value={goal} onChange={(e) => setGoal(e.target.value)}>
          <option value="engineering">{t('engineering')}</option>
          <option value="medicine">{t('medicine')}</option>
          <option value="commerce">{t('commerce')}</option>
          <option value="arts">{t('arts')}</option>
        </select>
      </div>
      <button className="btn" type="submit">{t('start_quiz')}</button>
    </form>
  )
}