# Saarthi AI - Dev Notes

- Tech: Vite + React, Tailwind, react-router, i18next.
- Start: `npm install` then `npm run dev`.
- Build: `npm run build`.
- Deploy: Vercel (Root = project, Build Command `npm run build`, Output `.\dist`).

Data flow summary:
- Home → choose mode
- Studying → MarksForm → Quiz (subjectQuestions based on goal)
- Completed → Quiz (quizQuestions)
- Result → maps score to recommendations via careerData.json

Tailwind utilities are pre-wired via `index.css`.