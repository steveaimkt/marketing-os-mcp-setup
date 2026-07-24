#!/usr/bin/env bash
# 클론한 저장소의 설치 스킬을 Claude Code 가 인식하는 위치(.claude/skills/)에 등록한다.
# 사용법:  bash setup-skills.sh          (이 저장소 안에서만 쓰는 프로젝트 스킬)
#          bash setup-skills.sh --user   (어느 폴더에서든 쓰는 개인 스킬)

set -euo pipefail
cd "$(dirname "$0")"

if [ "${1:-}" = "--user" ]; then
  DEST="$HOME/.claude/skills"
  SCOPE="개인 스킬 (모든 프로젝트에서 사용 가능)"
else
  DEST="$(pwd)/.claude/skills"
  SCOPE="프로젝트 스킬 (이 폴더에서 claude 실행 시 사용 가능)"
fi

mkdir -p "$DEST"

count=0
# mcp설치-* / bot-build / discord-channels-setup 등 SKILL.md 를 가진 폴더 전부
while IFS= read -r skill; do
  name="$(basename "$skill")"
  rm -rf "${DEST:?}/$name"
  cp -R "$skill" "$DEST/$name"
  echo "  ✓ /$name"
  count=$((count + 1))
done < <(find . -name SKILL.md -not -path "./.claude/*" -exec dirname {} \; | sort)

echo
echo "완료 · $count 개 스킬 등록"
echo "위치 : $DEST"
echo "범위 : $SCOPE"
echo
echo "다음 단계"
echo "  1) claude 실행"
echo "  2) /  입력 → 목록에서 mcp설치-전체 선택"
echo "     또는 그냥 \"MCP 전체 설치하자\" 라고 입력"
