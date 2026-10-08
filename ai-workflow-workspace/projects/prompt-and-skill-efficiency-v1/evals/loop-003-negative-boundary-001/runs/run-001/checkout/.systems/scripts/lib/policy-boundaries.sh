#!/usr/bin/env bash

# Shared policy-boundary helper. Callers own `fail`.
policy_safe_prohibition_pattern='must not|do not|does not|cannot|never|forbidden|invalid|not allow|no automatic|not final check|not write|no project closure|preserves existing|preserving formal|keep precedence|nie może|nie wolno|nie daje|nie oznacza|nie omija|nie pozwala|nie zastępuje|nie uruchamiaj|nie oznaczaj'

policy_match_requires_rejection() {
  local line="$1"
  local match="$2"
  local prefix
  local scoped_match
  local final_clause

  prefix="${line%%"$match"*}"
  scoped_match="${prefix}${match}"
  final_clause="$(printf '%s\n' "$scoped_match" | perl -pe 's/\b(?:but|however|except|unless|yet|and)\b/\n/ig; s/[;:.]/\n/g' | awk 'NF { clause = $0 } END { print clause }')"

  if ! printf '%s\n' "$final_clause" | rg -qi -- "$policy_safe_prohibition_pattern"; then
    return 0
  fi

  return 1
}

policy_reject_unsafe_pattern() {
  local pattern="$1"
  local message="$2"
  shift 2

  local output
  local status
  local entry
  local local_line
  local remaining_line
  local match
  local rejected=()

  if output="$(rg -n --with-filename -i -- "$pattern" "$@" 2>&1)"; then
    status=0
  else
    status=$?
  fi

  if (( status > 1 )); then
    printf '%s\n' "$output"
    echo "Policy-boundary scan failed: $message"
    fail=1
    return 0
  fi

  if (( status == 0 )); then
    while IFS= read -r entry; do
      [[ -z "$entry" ]] && continue
      local_line="${entry#*:*:}"
      remaining_line="$local_line"
      while IFS= read -r match; do
        [[ -z "$match" ]] && continue
        if policy_match_requires_rejection "$remaining_line" "$match"; then
          rejected+=("$entry")
          break
        fi
        remaining_line="${remaining_line#*"$match"}"
      done < <(printf '%s\n' "$local_line" | rg -o -i -- "$pattern" || true)
    done <<< "$output"
  fi

  if [[ "${#rejected[@]}" -gt 0 ]]; then
    printf '%s\n' "${rejected[@]}"
    echo "$message"
    fail=1
  fi
}
