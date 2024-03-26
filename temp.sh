PROJECT_VERSION=0.2.0
current_tag=$(git describe --tags)
git tag -f $PROJECT_VERSION

diff_tags=$(./get_git_tag_diff.sh $current_tag $PROJECT_VERSION)
cd cicd/migrations/taxishop/
for tag in $diff_tags; do
  if [[ "$tag" > "$current_tag" ]]; then
    mode="migrate"
  else
    mode="revert"
  fi
  python -m src.db.migration_handler --version $tag --mode $mode --dbname taxi --print-only

done
