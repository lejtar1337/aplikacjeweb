#!/usr/bin/env bash
set -u

BASE="${1:-http://127.0.0.1:8000}"
RUN="$$"
PASSED=0
FAILED=0

check() {
  local expected="$1"
  local method="$2"
  local path="$3"
  local body="${4:-}"
  local args=(-s -o /dev/null -w "%{http_code}" -X "$method" "$BASE$path")
  if [ -n "$body" ]; then
    args+=(-H "Content-Type: application/json" -d "$body")
  fi
  local actual
  actual=$(curl "${args[@]}")
  if [ "$actual" = "$expected" ]; then
    PASSED=$((PASSED + 1))
    echo "OK    $expected  $method $path"
  else
    FAILED=$((FAILED + 1))
    echo "BLAD  oczekiwano $expected, otrzymano $actual  $method $path $body"
  fi
}

created_id() {
  curl -s -D - -o /dev/null -X POST "$BASE$1" -H "Content-Type: application/json" -d "$2" \
    | tr -d '\r' | awk -F/ 'tolower($0) ~ /^location:/ {print $NF}'
}

PROJECT=$(created_id /projects "{\"name\": \"Kontrola $RUN\"}")
TASK=$(created_id /tasks "{\"project_id\": $PROJECT, \"title\": \"Zadanie kontrolne\"}")

echo "Projekt testowy: $PROJECT, zadanie testowe: $TASK"
echo

check 200 GET /users
check 200 GET /users/1
check 404 GET /users/999

check 200 GET /projects
check 201 POST /projects "{\"name\": \"Drugi $RUN\"}"
check 409 POST /projects "{\"name\": \"Kontrola $RUN\"}"
check 422 POST /projects '{"name": "   "}'
check 200 GET "/projects/$PROJECT"
check 404 GET /projects/999
check 200 PATCH "/projects/$PROJECT" '{"description": "Projekt utworzony przez check-api.sh"}'
check 409 PATCH "/projects/$PROJECT" "{\"name\": \"Drugi $RUN\"}"
check 409 DELETE "/projects/$PROJECT"

check 200 GET /tasks
check 200 GET "/tasks?project_id=$PROJECT&status=open"
check 422 GET "/tasks?status=unknown"
check 422 GET "/tasks?limit=0"
check 201 POST /tasks "{\"project_id\": $PROJECT, \"title\": \"Drugie zadanie\"}"
check 400 POST /tasks '{"title": '
check 409 POST /tasks "{\"project_id\": $PROJECT, \"title\": \"Zadanie kontrolne\"}"
check 422 POST /tasks '{"title": "Bez projektu"}'
check 422 POST /tasks '{"project_id": 999, "title": "Nieistniejacy projekt"}'
check 422 POST /tasks "{\"project_id\": $PROJECT, \"title\": \"   \"}"
check 422 POST /tasks "{\"project_id\": $PROJECT, \"title\": \"Pole id\", \"id\": 1}"
check 422 POST /tasks "{\"project_id\": $PROJECT, \"title\": \"Zly status\", \"status\": \"closed\"}"
check 422 POST /tasks "{\"project_id\": $PROJECT, \"title\": \"Zly uzytkownik\", \"assignee_id\": 999}"
check 200 GET "/tasks/$TASK"
check 404 GET /tasks/999
check 200 PATCH "/tasks/$TASK" '{"status": "in_progress", "assignee_id": 1}'
check 200 PATCH "/tasks/$TASK" '{"assignee_id": null}'
check 409 PATCH "/tasks/$TASK" '{"title": "Drugie zadanie"}'
check 422 PATCH "/tasks/$TASK" '{"title": null}'
check 404 PATCH /tasks/999 '{"status": "done"}'
check 204 DELETE "/tasks/$TASK"
check 404 DELETE "/tasks/$TASK"

echo
echo "Zgodnych: $PASSED, niezgodnych: $FAILED"
[ "$FAILED" -eq 0 ]
