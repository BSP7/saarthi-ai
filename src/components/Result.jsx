import React from 'react'
import { useLocation, Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import careerData from '../data/careerData.json'

// Map score and goal to recommendation bucket
function getRecommendations(total, mode, goal) {
  if (mode === 'studying') {
    const tracks = careerData.higherEducation
    if (goal && tracks[goal]) {
      const level = total > 35 ? 'strong' : total > 25 ? 'moderate' : 'starter'
      return tracks[goal][level]
    }
    return tracks.engineering.starter
  }

  // completed mode
  const buckets = careerData.careers
  const level = total > 25 ? 'analytical' : total > 15 ? 'balanced' : 'creative'
  return buckets[level]
}

export default function Result() {
  const { t } = useTranslation()
  const { state } = useLocation()
  // allow restoring result from sessionStorage if user refreshed before reaching this page
  let stored = null
  try { stored = JSON.parse(sessionStorage.getItem('saarthi_last_result')) } catch (e) { stored = null }

  const mode = state?.mode || stored?.mode || 'completed'
  const total = state?.total ?? stored?.total ?? 0
  const goal = state?.goal || stored?.goal

  const recomms = getRecommendations(total, mode, goal)

  return (
    <div className="card space-y-4">
      <h2 className="text-xl font-semibold">{t('your_results')}</h2>
      <p className="text-gray-600">{t('score_label')}: <span className="font-semibold">{Math.round(total)}</span></p>

      <div className="space-y-3">
        {recomms.map((r, idx) => (
          <div key={idx} className="border rounded p-3">
            <div className="font-medium">{r.title}</div>
            <div className="text-sm text-gray-600">{r.description}</div>
            {r.improve && (
              <div className="mt-2 text-sm">
                <span className="font-semibold">{t('improvement')}:</span> {r.improve}
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="flex gap-3">
      <Link to="/" className="btn-secondary" onClick={() => { try { sessionStorage.removeItem('saarthi_state'); sessionStorage.removeItem('saarthi_last_result'); sessionStorage.removeItem('saarthi_answers') } catch (e) {} }}>{t('go_home')}</Link>
      <button className="btn" onClick={() => { try { sessionStorage.removeItem('saarthi_state'); sessionStorage.removeItem('saarthi_last_result'); sessionStorage.removeItem('saarthi_answers') } catch (e) {} window.location.href = '/' }}>{t('reset_progress')}</button>
      </div>
    </div>
  )
}