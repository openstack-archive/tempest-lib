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

# get only commits that touch our files
commits="$(git log --format=format:%h --no-merges --follow -- $files)"
# then their merge commits - which works fina since we merge commits
# individually.
merge_commits="$(git log --format=format:%h --merges --first-parent -- $files)"
pattern="\n$(echo $commits $merge_commits | sed -e 's/ /\\|/g')"

# order them by filtering each one in the order it appears on rev-list
SHA1_LIST=$(git rev-list --oneline HEAD | grep $pattern)

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
