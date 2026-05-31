#!/bin/sh

set -eu

usage() {
  printf 'Usage: %s <model_name> <harness_name> [task|--all]\n' "$0" >&2
  exit 1
}

[ "$#" -eq 2 ] || [ "$#" -eq 3 ] || usage

model_name=$1
harness_name=$2
task=${3:---all}

move_task_answers() {
  task_name=$1
  source_dir="./tasks/$task_name/answer"
  destination_dir="./answers/$task_name/$model_name/$harness_name"

  if [ ! -d "$source_dir" ]; then
    printf 'Skipping task without answer directory: %s\n' "$task_name" >&2
    return 0
  fi

  mkdir -p "$destination_dir"

  found_files=false
  for file in "$source_dir"/*; do
    [ -e "$file" ] || continue
    found_files=true
    mv "$file" "$destination_dir/"
  done

  if [ "$found_files" = false ]; then
    printf 'No files found in: %s\n' "$source_dir" >&2
    return 0
  fi

  printf 'Moved answer files from %s to %s\n' "$source_dir" "$destination_dir"
}

if [ "$task" = "--all" ]; then
  for task_dir in ./tasks/*; do
    [ -d "$task_dir" ] || continue
    move_task_answers "${task_dir##*/}"
  done
else
  if [ ! -d "./tasks/$task" ]; then
    printf 'Task directory does not exist: ./tasks/%s\n' "$task" >&2
    exit 1
  fi

  move_task_answers "$task"
fi
