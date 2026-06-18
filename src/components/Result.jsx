import React, { useEffect, useState } from 'react'
import { useLocation, Link, useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'

export default function Result() {
  const { t } = useTranslation()
  const { state } = useLocation()
  const navigate = useNavigate()
  
  const [loading, setLoading] = useState(true)
  const [loadingText, setLoadingText] = useState('Analyzing Your Profile...')
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    // Try to load payload from state or fallback to localStorage if refreshed
    let payload = state?.payload
    if (!payload) {
      try {
        const cached = localStorage.getItem('saarthi_v2_dashboard')
        if (cached) {
          setResults(JSON.parse(cached))
          setLoading(false)
          return
        }
      } catch (e) {}
    }

    if (!payload && !results) {
      navigate('/')
      return
    }

    if (payload) {
      generateRecommendations(payload)
    }
  }, [state, navigate])

  const generateRecommendations = async (featurePayload) => {
    try {
      // Rotate loading text to simulate complex processing
      setTimeout(() => setLoadingText('Matching Careers...'), 1500)
      setTimeout(() => setLoadingText('Generating Recommendations...'), 3000)

      const response = await fetch('/api/v2/recommendation/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          user_id: "user-" + Math.random().toString(36).substring(7),
          features: featurePayload
        })
      })

      if (!response.ok) {
        throw new Error('Failed to generate recommendations')
      }

      const data = await response.json()
      
      if (data.status === 'error') {
        throw new Error(data.results?.error || 'Unknown error occurred')
      }

      setResults(data.results)
      
      // Persist for dashboard
      try {
        localStorage.setItem('saarthi_v2_dashboard', JSON.stringify(data.results))
      } catch (e) {}
      
    } catch (err) {
      console.error(err)
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    try {
      localStorage.removeItem('saarthi_v2_dashboard')
      sessionStorage.removeItem('saarthi_v2_answers')
      sessionStorage.removeItem('saarthi_v2_step')
    } catch (e) {}
    window.location.href = '/'
  }

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-20 space-y-6">
        <div className="w-16 h-16 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
        <div className="text-xl font-medium text-gray-700 animate-pulse">{loadingText}</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="card max-w-2xl mx-auto space-y-4 text-center">
        <div className="text-red-500 text-5xl mb-4">⚠️</div>
        <h2 className="text-2xl font-bold text-gray-800">Something went wrong</h2>
        <p className="text-gray-600">{error}</p>
        <button className="btn mt-4" onClick={handleReset}>Try Again</button>
      </div>
    )
  }

  if (!results) return null

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Header section */}
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-bold text-gray-900">Your AI Career Recommendations</h1>
        <p className="text-gray-600">Based on our advanced 30-feature O*NET analysis</p>
      </div>

      {/* Strengths Section */}
      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
        <h2 className="text-lg font-semibold mb-4 text-gray-800">Your Key Strengths</h2>
        <div className="flex flex-wrap gap-2">
          {results.strengths?.map((strength, idx) => (
            <span key={idx} className="bg-green-100 text-green-800 px-4 py-2 rounded-lg font-medium text-sm">
              ✨ {strength}
            </span>
          ))}
        </div>
      </div>

      {/* Domains Section */}
      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
        <h2 className="text-lg font-semibold mb-4 text-gray-800">Top 3 Career Domains</h2>
        <div className="grid gap-3 sm:grid-cols-3">
          {results.top_domains?.map((domain, idx) => (
            <div key={idx} className="bg-blue-50 border border-blue-100 rounded-lg p-4 text-center">
              <div className="text-blue-800 font-medium">{domain}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Careers Section */}
      <div className="space-y-4">
        <h2 className="text-xl font-bold text-gray-800 border-b pb-2">Top 5 Specific Occupations</h2>
        <div className="space-y-4">
          {results.careers?.map((career, idx) => (
            <div key={idx} className="bg-white border rounded-xl p-5 shadow-sm hover:shadow-md transition-shadow relative overflow-hidden">
              <div className="absolute top-0 left-0 w-1 h-full bg-blue-600"></div>
              <div className="flex justify-between items-start mb-2">
                <div>
                  <h3 className="text-xl font-bold text-gray-900">{career.title}</h3>
                  <div className="text-sm text-blue-600 font-medium">{career.domain}</div>
                </div>
                <div className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-bold flex items-center gap-1">
                  <span>🎯</span> {career.match_score}% Match
                </div>
              </div>
              <p className="text-gray-600 text-sm mt-3 leading-relaxed">{career.description}</p>
            </div>
          ))}
        </div>
      </div>

      <div className="flex justify-center gap-4 pt-6">
        <button className="px-6 py-2 rounded-lg font-medium text-blue-600 bg-blue-50 hover:bg-blue-100" onClick={() => navigate('/')}>
          Go to Dashboard
        </button>
        <button className="px-6 py-2 rounded-lg font-medium text-gray-600 bg-gray-100 hover:bg-gray-200" onClick={handleReset}>
          Retake Assessment
        </button>
      </div>
    </div>
  )
}