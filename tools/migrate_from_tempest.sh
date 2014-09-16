#!/bin/bash
#
# Use this script to move over a set of files from tempest master into
# tempest-lib with the commit history for the files in the commit message.
# This should only be done for files that haven't been migrated over already.
# To use:
#  1. Create a new branch in the tempest-lib repo so not to destroy your current
#     working branch
#  2. Run the script from the repo dir and specify the file paths relative to
#     the root tempest dir(only code and unit tests):
#
#   tools/migrate_from_tempest.sh tempest/file.py tempest/sub_dir


function usage {
    echo "Usage: $0 [OPTION] file1 file2"
    echo "Migrate files from tempest"
    echo ""
    echo "-o, --output_dir      Specify an directory relative to the repo root to move the migrated files into."
}

set -e

output_dir=""

while [ $# -gt 0 ]; do
    case "$1" in
        -h|--help) usage; exit;;
        -o|--output_dir) output_dir="$2"; shift;;
        *) files="$files $1";;
    esac
    shift
done

TEMPEST_GIT_URL=git://git.openstack.org/openstack/tempest

tmpdir=$(mktemp -d -t tempest-migrate.XXXX)
tempest_lib_dir=$(dirname "$0")

function count_commits {
    echo
    echo "Have $(git log --oneline | wc -l) commits"
}

# Clone tempest and cd into it
git clone $TEMPEST_GIT_URL $tmpdir
cd $tmpdir

# Build the grep pattern for ignoring files that we want to keep
keep_pattern="\($(echo $files | sed -e 's/ /\\|/g')\)"
# Prune all other files in every commit
pruner="git ls-files | grep -v \"$keep_pattern\" | git update-index --force-remove --stdin; git ls-files > /dev/stderr"

# Find all first commits with listed files and find a subset of them that
# predates all others
roots=""
for file in $files; do
    file_root="$(git rev-list --reverse HEAD -- $file | head -n1)"
    fail=0
    for root in $roots; do
         if git merge-base --is-ancestor $root $file_root; then
             fail=1
             break
         elif ! git merge-base --is-ancestor $file_root $root; then
             new_roots="$new_roots $root"
         fi
     done
     if [ $fail -ne 1 ]; then
         roots="$new_roots $file_root"
     fi
done

set_roots="
if [ '' $(for root in $roots; do echo " -o \"\$GIT_COMMIT\" == '$root' "; done) ]; then
    echo ''
else
    cat
fi"

# Enhance git_commit_non_empty_tree to skip merges with:
# a) either two equal parents (commit that was about to land got purged as well
# as all commits on mainline);
# b) or with second parent being an ancestor to the first one (just as with a)
# but when there are some commits on mainline).
# In both cases drop second parent and let git_commit_non_empty_tree to decide
# if commit worth doing (most likely not).

skip_empty=$(cat << \EOF
if [ $# = 5 ] && git merge-base --is-ancestor $5 $3; then
    git_commit_non_empty_tree $1 -p $3
else
    git_commit_non_empty_tree "$@"
fi
EOF
)

# Prune just the commits relevant to what is being migrated
git filter-branch --index-filter "$pruner" --parent-filter "$set_roots" --commit-filter "$skip_empty" HEAD

SHA1_LIST=`git log --oneline`

# Move files and commit
cd -
file_list=''
for file in $files; do
    filename=`basename $file`
    if [ -n "$output_dir" ]; then
        dest_file="$output_dir/$filename"
    else
        dest_file="tempest_lib/$filename"
    fi
    cp -r "$tmpdir/$file" "$dest_file"
    git add "$dest_file"
    if [[ -z "$file_list" ]]; then
        file_list="$filename"
    else
        file_list="$file_list, $filename"
    fi
done
# Cleanup temporary tempest repo
rm -rf $tmpdir

# Generate a migration commit
commit_message="Migrated $file_list from tempest"
pre_list=$"This migrates the above files from tempest. This includes tempest commits:"
post_list=$"to see the commit history for these files refer to the above sha1s in the tempest repository"
git commit -m "$commit_message" -m "$pre_list" -m "$SHA1_LIST" -m "$post_list"
