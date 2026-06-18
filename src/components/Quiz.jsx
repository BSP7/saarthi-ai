import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import assessmentData from '../data/assessment_v2_questions.json'
import { calculateV2Profile } from '../utils/assessmentScorerV2'

const SECTIONS = [
  { id: 'interests', title: 'RIASEC Interests', start: 0, end: 18 },
  { id: 'skills', title: 'Essential Skills', start: 18, end: 34 },
  { id: 'abilities', title: 'Abilities', start: 34, end: 50 },
  { id: 'knowledge', title: 'Knowledge Areas', start: 50, end: 66 }
]

export default function Quiz() {
  const { t } = useTranslation()
  const navigate = useNavigate()
  
  const [currentStep, setCurrentStep] = useState(0)
  const [answers, setAnswers] = useState({})

  // Try to recover state
  useEffect(() => {
    try {
      const savedAnswers = JSON.parse(sessionStorage.getItem('saarthi_v2_answers'))
      const savedStep = parseInt(sessionStorage.getItem('saarthi_v2_step'), 10)
      if (savedAnswers) setAnswers(savedAnswers)
      if (!isNaN(savedStep)) setCurrentStep(savedStep)
    } catch (e) {}
  }, [])

  const currentSection = SECTIONS[currentStep]
  const currentQuestions = assessmentData.questions.slice(currentSection.start, currentSection.end)

  const handleSelect = (qId, weight) => {
    setAnswers(prev => {
      const next = { ...prev, [qId]: weight }
      try { sessionStorage.setItem('saarthi_v2_answers', JSON.stringify(next)) } catch (e) {}
      return next
    })
  }

  const allCurrentAnswered = currentQuestions.every(q => answers[q.id] !== undefined)

  const handleNext = () => {
    if (currentStep < SECTIONS.length - 1) {
      const nextStep = currentStep + 1
      setCurrentStep(nextStep)
      try { sessionStorage.setItem('saarthi_v2_step', nextStep.toString()) } catch (e) {}
      window.scrollTo(0, 0)
    } else {
      handleSubmit()
    }
  }

  const handleBack = () => {
    if (currentStep > 0) {
      const prevStep = currentStep - 1
      setCurrentStep(prevStep)
      try { sessionStorage.setItem('saarthi_v2_step', prevStep.toString()) } catch (e) {}
      window.scrollTo(0, 0)
    }
  }

  const handleSubmit = () => {
    // Score calculation via assessmentScorerV2
    const featurePayload = calculateV2Profile(assessmentData.questions, answers)
    
    // Clear session storage since we are done
    try { 
      sessionStorage.removeItem('saarthi_v2_answers')
      sessionStorage.removeItem('saarthi_v2_step')
    } catch (e) {}
    
    navigate('/result', { state: { payload: featurePayload } })
  }

  const options = [
    { label: "Strongly Disagree", weight: 1 },
    { label: "Disagree", weight: 2 },
    { label: "Neutral", weight: 3 },
    { label: "Agree", weight: 4 },
    { label: "Strongly Agree", weight: 5 }
  ]

  return (
    <div className="card space-y-6 max-w-4xl mx-auto">
      <div className="flex justify-between items-center border-b pb-4">
        <h2 className="text-2xl font-bold">{currentSection.title}</h2>
        <span className="text-sm font-medium text-gray-500 bg-gray-100 px-3 py-1 rounded-full">
          Step {currentStep + 1} of {SECTIONS.length}
        </span>
      </div>

      <div className="w-full bg-gray-200 rounded-full h-2.5">
        <div className="bg-blue-600 h-2.5 rounded-full" style={{ width: `${((currentStep + 1) / SECTIONS.length) * 100}%` }}></div>
      </div>

      <div className="space-y-8 mt-6">
        {currentQuestions.map((q) => (
          <div key={q.id} className="space-y-3 p-4 bg-gray-50 rounded-lg">
            <div className="font-medium text-lg text-gray-800">{q.question}</div>
            <div className="grid gap-2 sm:grid-cols-5">
              {options.map((opt, i) => (
                <label 
                  key={i} 
                  className={`border rounded-lg p-3 text-center cursor-pointer transition-all ${
                    answers[q.id] === opt.weight 
                      ? 'border-blue-600 bg-blue-50 shadow-sm' 
                      : 'border-gray-200 hover:border-blue-300 hover:bg-white'
                  }`}
                >
                  <input
                    type="radio"
                    name={`q-${q.id}`}
                    className="hidden"
                    onChange={() => handleSelect(q.id, opt.weight)}
                    checked={answers[q.id] === opt.weight}
                  />
                  <div className="text-sm font-medium">{opt.label}</div>
                </label>
              ))}
            </div>
          </div>
        ))}
      </div>

      <div className="flex justify-between pt-6 border-t">
        <button 
          className={`px-6 py-2 rounded-lg font-medium ${currentStep === 0 ? 'opacity-50 cursor-not-allowed bg-gray-200 text-gray-500' : 'bg-gray-200 text-gray-800 hover:bg-gray-300'}`}
          onClick={handleBack}
          disabled={currentStep === 0}
        >
          Back
        </button>
        <button 
          className={`px-6 py-2 rounded-lg font-medium text-white ${!allCurrentAnswered ? 'opacity-50 cursor-not-allowed bg-blue-400' : 'bg-blue-600 hover:bg-blue-700'}`} 
          disabled={!allCurrentAnswered} 
          onClick={handleNext}
        >
          {currentStep === SECTIONS.length - 1 ? 'Generate Recommendations' : 'Next Section'}
        </button>
      </div>
    </div>
  )
}