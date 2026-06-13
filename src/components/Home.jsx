import React from 'react'
import { useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'

export default function Home({ setMode }) {
  const navigate = useNavigate()
  const { t } = useTranslation()
  const [hasSaved, setHasSaved] = React.useState(false)

  React.useEffect(() => {
    try {
      const s = sessionStorage.getItem('saarthi_state') || sessionStorage.getItem('saarthi_last_result')
      setHasSaved(!!s)
    } catch (e) { setHasSaved(false) }
  }, [])

  return (
    <div className="card">
      <h1 className="text-2xl font-semibold mb-4">{t('title')}</h1>
      <p className="mb-6 text-gray-600">{t('subtitle')}</p>

      <div className="grid sm:grid-cols-2 gap-4">
        <button
          className="btn"
          onClick={() => { setMode('studying'); navigate('/marks') }}
        >
          {t('im_studying')}
        </button>
        <button
          className="btn-secondary"
          onClick={() => { setMode('completed'); navigate('/quiz', { state: { mode: 'completed' } }) }}
        >
          {t('ive_completed')}
        </button>
      </div>
      {hasSaved && (
        <div className="mt-4 bg-yellow-50 border border-yellow-200 p-3 rounded">
          <div className="flex items-center justify-between">
            <div className="text-sm text-yellow-800">{t('resume_available')}</div>
            <div className="flex items-center gap-2">
              <button className="btn" onClick={() => {
                // prefer last result if present, otherwise resume quiz state
                const last = sessionStorage.getItem('saarthi_last_result')
                if (last) { const parsed = JSON.parse(last); navigate('/result', { state: parsed }) }
                else { const s = JSON.parse(sessionStorage.getItem('saarthi_state')); navigate('/quiz', { state: s }) }
              }}>{t('resume')}</button>
              <button className="btn-secondary" onClick={() => { try { sessionStorage.removeItem('saarthi_state'); sessionStorage.removeItem('saarthi_answers'); sessionStorage.removeItem('saarthi_last_result') } catch (e) {} setHasSaved(false) }}>{t('clear_progress')}</button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}