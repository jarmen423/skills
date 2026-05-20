#!/usr/bin/env bash
# Converts Unix-style symlinks in ~/.claude/skills/ to Windows junctions
# so Claude Desktop (native Windows app) can read them.

SKILLS_DIR="/c/Users/jfrie/.claude/skills"
AGENTS_DIR="C:\\Users\\jfrie\\.agents\\skills"

cd "$SKILLS_DIR" || exit 1

converted=0
skipped=0
failed=0

for link in */; do
  name="${link%/}"

  # Only process if it's a symlink
  if [ -L "$name" ]; then
    target_win="${AGENTS_DIR}\\${name}"

    # Check the real target exists
    if [ -d "/c/Users/jfrie/.agents/skills/${name}" ]; then
      # Remove the Unix symlink
      rm "$name"
      # Create Windows junction via cmd
      cmd.exe /c "mklink /J \"${SKILLS_DIR//\//\\\\}\\\\${name}\" \"${target_win}\"" > /dev/null 2>&1
      if [ $? -eq 0 ]; then
        echo "✓ $name"
        ((converted++))
      else
        echo "✗ FAILED: $name"
        ((failed++))
      fi
    else
      echo "~ SKIPPED (target missing): $name"
      ((skipped++))
    fi
  fi
done

echo ""
echo "Done: $converted converted, $skipped skipped (missing target), $failed failed"
