// AI Recommendation Engine
function generateRecommendations(level, ageRange) {
  const recommendations = {
    beginner: {
      todaysDrills: [
        { name: 'Wall Warm-up', description: 'Hit ball against wall for 5 min, focus on grip' },
        { name: 'Shadow Practice', description: '10 min shadow swings, focus on footwork' },
        { name: 'Short Rally Drill', description: 'Rally with partner in front court only' }
      ],
      tips: [
        { category: 'Grip', message: 'Use a firm but relaxed grip. Thumb under the handle for control.' },
        { category: 'Footwork', message: 'Small steps between shots. Always return to the T position.' },
        { category: 'Serve', message: 'Focus on consistency over power. Aim for center court.' }
      ],
      allDrillsByCategory: {
        'Warm-up Drills': [
          { name: 'Wall Hits', description: 'Hit ball against wall, build rhythm' },
          { name: 'Shadow Swings', description: 'Practice swing motion without ball' },
          { name: 'Dynamic Stretching', description: 'Arm circles, leg swings, mobility' }
        ],
        'Footwork Drills': [
          { name: 'T-Position Drill', description: 'Practice returning to center court T' },
          { name: 'Split Step Practice', description: 'Explosive step as opponent strikes' },
          { name: 'Court Movement', description: 'Lateral and diagonal movement patterns' }
        ],
        'Basic Shots': [
          { name: 'Straight Drive', description: 'Hit ball straight down the wall' },
          { name: 'Cross Court', description: 'Diagonal shots across the court' },
          { name: 'Lob Practice', description: 'Gentle high shots for defensive play' }
        ],
        'Serve Practice': [
          { name: 'Serve Accuracy', description: '20 serves focusing on consistency' },
          { name: 'Serve Placement', description: 'Alternate serving corners' },
          { name: 'Second Serve', description: 'Practice safe, soft serves' }
        ]
      }
    },
    intermediate: {
      todaysDrills: [
        { name: 'Boast & Drive', description: '10 min alternating boasts and drives from mid-court' },
        { name: 'Rally Conditioning', description: '5 rallies focusing on court control' },
        { name: 'Volley Practice', description: 'Front court volley exchanges with partner' }
      ],
      tips: [
        { category: 'Court Control', message: 'Push opponent to back, move forward to attack.' },
        { category: 'Shot Selection', description: 'Mix up pace and angles to keep opponent guessing.' },
        { category: 'Fitness', message: 'Work on explosive movements. Conditioning is key at this level.' }
      ],
      allDrillsByCategory: {
        'Advanced Footwork': [
          { name: 'Ghosting Drill', description: 'Movement without ball, all court areas' },
          { name: 'Lunge Practice', description: 'Low lunges to front corners' },
          { name: 'Recovery Drills', description: 'Fast movement back to center' }
        ],
        'Shot Accuracy': [
          { name: 'Boast Drill', description: 'Consistent boasts from mid-court' },
          { name: 'Drop Shot', description: 'Soft shots with control' },
          { name: 'Hard Drive', description: 'Fast balls down the wall' }
        ],
        'Game Tactics': [
          { name: 'Court Positioning', description: 'Hold center court during rallies' },
          { name: 'Serve & Volley', description: 'Attack mode after serves' },
          { name: 'Pressure Points', description: 'Identify and exploit opponent weaknesses' }
        ],
        'Fitness': [
          { name: 'Interval Training', description: '20 sec intense, 10 sec rest x10' },
          { name: 'Core Strength', description: 'Planks, Russian twists, bridges' },
          { name: 'Explosive Power', description: 'Jump squats, lateral bounds' }
        ]
      }
    },
    advanced: {
      todaysDrills: [
        { name: 'Advanced Court Movement', description: 'Game-pace footwork across all court areas' },
        { name: 'Aggressive Rally Drill', description: '10 min intense rallies, focus on attacking' },
        { name: 'Serve & Pressure', description: 'Aggressive serves followed by net domination' }
      ],
      tips: [
        { category: 'Tactics', message: 'Use serve placement to set up your attacking shots.' },
        { category: 'Mental Game', message: 'Stay focused on your game plan. Adapt mid-match.' },
        { category: 'Technique', message: 'Refine your timing on power shots. Consistency under pressure.' }
      ],
      allDrillsByCategory: {
        'Match Preparation': [
          { name: 'Match Simulation', description: 'Competitive rallies at game speed' },
          { name: 'Pressure Situations', description: 'Practice clutch moments (tie-breaks)' },
          { name: 'Mental Conditioning', description: 'Develop resilience and focus' }
        ],
        'Advanced Techniques': [
          { name: 'Backhand Power', description: 'Develop strong backhand attacks' },
          { name: 'Deception', description: 'Disguise shots, wrong-foot opponents' },
          { name: 'Volley Finishing', description: 'Kill shots at the net' }
        ],
        'Competitive Play': [
          { name: 'Serve Strategy', description: 'Mix serve speeds and placements' },
          { name: 'Rally Patterns', description: 'Execute patterns from instruction' },
          { name: 'Opponent Analysis', description: 'Identify and attack weaknesses' }
        ],
        'Peak Performance': [
          { name: 'Recovery Training', description: 'Active recovery and stretching' },
          { name: 'Nutrition Timing', description: 'Fuel before, during, after sessions' },
          { name: 'Mental Toughness', description: 'Build confidence and composure' }
        ]
      }
    },
    professional: {
      todaysDrills: [
        { name: 'Pro-Level Conditioning', description: 'Game-intensity intervals, 45 min sessions' },
        { name: 'Tactical Match Play', description: 'Head-to-head competitive matches' },
        { name: 'Tournament Simulation', description: 'Best-of-5 or best-of-3 sets' }
      ],
      tips: [
        { category: 'Tournament Prep', message: 'Scout opponents. Develop detailed game plans.' },
        { category: 'Physical Peak', message: 'Monitor recovery. Avoid overtraining before big events.' },
        { category: 'Elite Mindset', message: 'Visualize success. Build mental resilience for high pressure.' }
      ],
      allDrillsByCategory: {
        'Elite Training': [
          { name: 'High-Intensity Intervals', description: '90% effort intervals with controlled rest' },
          { name: 'Sport-Specific Power', description: 'Explosive movements mirroring match play' },
          { name: 'Technical Refinement', description: 'Micro-adjustments to technique' }
        ],
        'Tournament Strategy': [
          { name: 'Opponent Research', description: 'Video analysis and scouting' },
          { name: 'Serve Patterns', description: 'Strategic serve placement under pressure' },
          { name: 'Match Psychology', description: 'Mental toughness in critical moments' }
        ],
        'Recovery & Prevention': [
          { name: 'Sport Massage', description: 'Regular massage for muscle recovery' },
          { name: 'Sleep Optimization', description: 'Consistency in sleep schedules' },
          { name: 'Injury Prevention', description: 'Targeted prehab and mobility work' }
        ],
        'Advanced Analytics': [
          { name: 'Performance Tracking', description: 'Monitor stats and shot selection' },
          { name: 'Biomechanics Analysis', description: 'Frame-by-frame technique review' },
          { name: 'Data-Driven Training', description: 'Adjust based on performance metrics' }
        ]
      }
    }
  };

  const ageMessages = {
    '5-10': "Great job starting young! Focus on having fun and building love for the game.",
    '11-15': "You're at the perfect age to develop solid fundamentals. Consistency is key!",
    '16-20': "Peak learning years! Now's the time to build advanced skills and competitive drive.",
    '21-30': "Great time to reach your peak. Combine experience with modern techniques.",
    '31-40': "Stay competitive! Your experience beats younger players' physical advantages.",
    '40+': "Age is just a number. Smart play and consistency win matches!"
  };

  return {
    ...recommendations[level],
    welcomeMessage: ageMessages[ageRange] || "Let's improve your squash game!"
  };
}

// Navigation helpers
function goToAuth() {
  window.location.href = 'signup.html';
}

function scrollToSection(sectionId) {
  const element = document.getElementById(sectionId);
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' });
  }
}

// Progress Tracking
const PROGRESS_KEY = 'squash_progress';
const SESSION_KEY = 'squash_sessions';

function initProgressData() {
  if (!localStorage.getItem(PROGRESS_KEY)) {
    localStorage.setItem(PROGRESS_KEY, JSON.stringify({
      totalSessions: 0,
      totalDrillsLogged: 0,
      skillRating: 3,
      consistencyDays: 0,
      lastSessionDate: null,
      drillsCompleted: {}
    }));
  }
  if (!localStorage.getItem(SESSION_KEY)) {
    localStorage.setItem(SESSION_KEY, JSON.stringify([]));
  }
}

function getProgress() {
  initProgressData();
  return JSON.parse(localStorage.getItem(PROGRESS_KEY));
}

function getSessions() {
  initProgressData();
  return JSON.parse(localStorage.getItem(SESSION_KEY)) || [];
}

function logSession(sessionData) {
  const sessions = getSessions();
  const session = {
    id: Date.now(),
    date: new Date().toISOString(),
    drillsCompleted: sessionData.drillsCompleted || [],
    duration: sessionData.duration || 30, // minutes
    intensity: sessionData.intensity || 'moderate',
    notes: sessionData.notes || '',
    skillRating: sessionData.skillRating || 5
  };
  
  sessions.push(session);
  localStorage.setItem(SESSION_KEY, JSON.stringify(sessions));
  
  // Update progress stats
  const progress = getProgress();
  progress.totalSessions += 1;
  progress.totalDrillsLogged += (session.drillsCompleted.length || 0);
  progress.lastSessionDate = session.date;
  
  // Update consistency (days in a row)
  const lastSessionDate = progress.lastSessionDate ? new Date(progress.lastSessionDate) : new Date();
  const today = new Date();
  const daysDiff = Math.floor((today - lastSessionDate) / (1000 * 60 * 60 * 24));
  if (daysDiff <= 1) {
    progress.consistencyDays += 1;
  } else {
    progress.consistencyDays = 1;
  }
  
  // Update drill counts
  if (session.drillsCompleted) {
    session.drillsCompleted.forEach(drill => {
      if (!progress.drillsCompleted[drill]) {
        progress.drillsCompleted[drill] = 0;
      }
      progress.drillsCompleted[drill] += 1;
    });
  }
  
  localStorage.setItem(PROGRESS_KEY, JSON.stringify(progress));
  return session;
}

function getProgressStats() {
  const progress = getProgress();
  const sessions = getSessions();
  
  const lastWeek = sessions.filter(s => {
    const sessionDate = new Date(s.date);
    const weekAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);
    return sessionDate >= weekAgo;
  });
  
  const totalMinutesThisWeek = lastWeek.reduce((sum, s) => sum + (s.duration || 0), 0);
  const avgSkillRating = lastWeek.length > 0 
    ? (lastWeek.reduce((sum, s) => sum + (s.skillRating || 5), 0) / lastWeek.length).toFixed(1)
    : 5;
  
  return {
    totalSessions: progress.totalSessions,
    consistencyStreak: progress.consistencyDays,
    drillsLogged: progress.totalDrillsLogged,
    sessionsThisWeek: lastWeek.length,
    totalMinutesThisWeek: totalMinutesThisWeek,
    averageSkillRating: avgSkillRating,
    topDrill: getTopDrill(progress.drillsCompleted),
    recentSessions: sessions.slice(-5).reverse()
  };
}

function getTopDrill(drillsCompleted) {
  if (!drillsCompleted || Object.keys(drillsCompleted).length === 0) return 'None yet';
  let topDrill = '';
  let maxCount = 0;
  for (const [drill, count] of Object.entries(drillsCompleted)) {
    if (count > maxCount) {
      maxCount = count;
      topDrill = drill;
    }
  }
  return topDrill || 'None yet';
}

function getConsistencyPercentage() {
  const stats = getProgressStats();
  // Max streak is 30 days, so percentage is (streak / 30) * 100
  return Math.min((stats.consistencyStreak / 30) * 100, 100);
}

function getSkillImprovementPercentage() {
  const sessions = getSessions();
  if (sessions.length < 2) return 50;
  
  const firstHalf = sessions.slice(0, Math.floor(sessions.length / 2));
  const secondHalf = sessions.slice(Math.floor(sessions.length / 2));
  
  const avgFirst = firstHalf.reduce((sum, s) => sum + (s.skillRating || 5), 0) / firstHalf.length;
  const avgSecond = secondHalf.reduce((sum, s) => sum + (s.skillRating || 5), 0) / secondHalf.length;
  
  const improvement = ((avgSecond - avgFirst) / 10) * 100 + 50;
  return Math.min(Math.max(improvement, 0), 100);
}
