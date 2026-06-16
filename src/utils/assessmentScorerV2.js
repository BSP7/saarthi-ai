/**
 * Assessment V2 Scoring Utility
 * 
 * Aggregates user answers from the 66-question V2 assessment 
 * and outputs the 30-feature vector expected by the backend.
 */

/**
 * Calculates the final 30-feature profile from raw assessment answers.
 * 
 * @param {Array} questions - The array of question objects from assessment_v2_questions.json
 * @param {Object} answers - A dictionary mapping question `id` to the Likert score (1-5)
 * @returns {Object} featureProfile - A dictionary of 30 features scaled to 1-10
 */
export function calculateV2Profile(questions, answers) {
  // 1. Group scores by feature
  const featureScores = {};
  const featureCounts = {};

  questions.forEach(q => {
    const featureName = q.feature;
    const score = answers[q.id];

    // Skip unanswered questions (or handle default)
    if (score === undefined) return;

    if (!featureScores[featureName]) {
      featureScores[featureName] = 0;
      featureCounts[featureName] = 0;
    }

    featureScores[featureName] += score;
    featureCounts[featureName] += 1;
  });

  // 2. Average the scores for each feature and scale to 1-10
  // (Likert is 1-5, so we can multiply by 2 to get a 2-10 scale, 
  // or use the formula: ((Average - 1) / 4) * 9 + 1 to properly scale 1-5 to 1-10)
  
  const finalProfile = {};
  
  for (const feature in featureScores) {
    const avgScore = featureScores[feature] / featureCounts[feature];
    
    // Scale 1-5 to 1-10 range
    // Formula: Scaled = ((Original - Min) / (Max - Min)) * (NewMax - NewMin) + NewMin
    // Scaled = ((avgScore - 1) / 4) * 9 + 1
    const scaledScore = ((avgScore - 1) / 4) * 9 + 1;
    
    // Round to 1 decimal place
    finalProfile[feature] = Math.round(scaledScore * 10) / 10;
  }

  // 3. Ensure all 30 features exist (default to 5.0 if completely missing)
  const EXPECTED_FEATURES = [
    "Realistic", "Investigative", "Artistic", "Social", "Enterprising", "Conventional",
    "Critical Thinking", "Programming", "Active Listening", "Reading Comprehension", "Speaking", "Writing", "Complex Problem Solving", "Decision Making",
    "Deductive Reasoning", "Inductive Reasoning", "Problem Sensitivity", "Oral Comprehension", "Mathematical Reasoning", "Information Ordering", "Visualization", "Selective Attention",
    "Computers and Electronics", "Mathematics", "Engineering and Technology", "Business", "Psychology", "Education and Training", "Medicine and Health", "Communications"
  ];

  EXPECTED_FEATURES.forEach(feat => {
    if (finalProfile[feat] === undefined) {
      finalProfile[feat] = 5.0; // Neutral default
    }
  });

  return finalProfile;
}
