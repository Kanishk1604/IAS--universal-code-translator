#!/bin/bash

# ✅ Input parameters: start and end dates
START_DATE="$1"
END_DATE="$2"

# ✅ Safety check
if [ -z "$START_DATE" ] || [ -z "$END_DATE" ]; then
  echo "❌ Please provide start and end dates."
  echo "Usage: ./add-commits.sh YYYY-MM-DD YYYY-MM-DD"
  exit 1
fi

# ✅ Base file to write commits into
FILE="activity_log.txt"

# ✅ Emojis and messages
MESSAGES=("Chatbot improvements" "API optimization" "Enhancing NLP flow" "Refactoring codebase" "Improved UI/UX" "Training model" "Documentation updates" "Bug fixes" "Performance improvements" "Integrating features")
EMOJIS=("🤖" "🚀" "✨" "⚡" "✅" "📦" "💡" "🧩")

# ✅ Current date loop
current_date="$START_DATE"

while [[ "$current_date" < "$END_DATE" ]]; do
  # 🎲 Skip some days naturally (about 30% chance)
  if (( RANDOM % 100 < 30 )); then
    echo "Skipping $current_date 💤"
    current_date=$(date -I -d "$current_date + 1 day")
    continue
  fi

  # 🎲 Random commits for the day
  commits_today=$((RANDOM % 5 + 1)) # 1–5 commits per active day

  echo "$current_date — $commits_today commits 📝"

  for ((i=0; i<commits_today; i++)); do
    # Random time of the day
    random_hour=$((RANDOM % 24))
    random_minute=$((RANDOM % 60))
    random_second=$((RANDOM % 60))

    export GIT_AUTHOR_DATE="$current_date $random_hour:$random_minute:$random_second"
    export GIT_COMMITTER_DATE="$GIT_AUTHOR_DATE"

    # Random commit message
    random_message=${MESSAGES[$RANDOM % ${#MESSAGES[@]}]}
    random_emoji=${EMOJIS[$RANDOM % ${#EMOJIS[@]}]}

    # Append to the file and commit
    echo "$random_message $random_emoji at $GIT_AUTHOR_DATE" >> $FILE
    git add $FILE
    git commit -m "$random_message $random_emoji at $GIT_AUTHOR_DATE"
  done

  # Move to next day
  current_date=$(date -I -d "$current_date + 1 day")
done

# ✅ Push to GitHub
git push --force

echo "🎉 Commits added between $START_DATE and $END_DATE!"
