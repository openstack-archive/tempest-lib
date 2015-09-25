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
    echo "-o, --output_dir      Specify a directory relative to the repo root to move the migrated files into."
    echo "-u, --tempest_git_url Specify the repo to clone tempest from for the migration."
}

set -e

output_dir=""
service_client=0

while [ $# -gt 0 ]; do
    case "$1" in
        -h|--help) usage; exit;;
        -o|--output_dir) output_dir="$2"; shift;;
        -u|--tempest_git_url) tempest_git_url="$2"; shift;;
        -s|--service_client) service_client=1;;
        *) files="$files $1";;
    esac
    shift
done

TEMPEST_GIT_URL=${tempest_git_url:-git://git.openstack.org/openstack/tempest}

tmpdir=$(mktemp -d -t tempest-migrate.XXXX)
tempest_lib_dir=$(dirname "$0")

function count_commits {
    echo
    echo "Have $(git log --oneline | wc -l) commits"
}

# Clone tempest and cd into it
git clone $TEMPEST_GIT_URL $tmpdir
cd $tmpdir

for file in $files; do
    # Get the latest change-id for each file
    change_id=`git log -n1 --grep "Change-Id: " -- $file | grep "Change-Id: " | awk '{print $2}'`
    filename=`basename $file`
    CHANGE_LIST=`echo -e "$CHANGE_LIST\n * $filename: $change_id"`
done

# Move files and commit
cd -
file_list=''
for file in $files; do
    filename=`basename $file`
    dirname=`dirname $file`
    if [ -n "$output_dir" ]; then
        dirname="$output_dir"
    else
        dirname=`echo $dirname | sed s@tempest\/@tempest_lib/\@`
        if [ $service_client -eq 1 ]; then
            # Remove /json path because tempest-lib supports JSON only without XML
            dirname=`echo $dirname | sed s@\/json@@`
        fi
    fi
    dest_file="$dirname/$filename"
    cp -r "$tmpdir/$file" "$dest_file"

    if [ $service_client -eq 1 ]; then
        # service_client module is not necessary in tempest-lib because rest_client can be used instead
        sed -i='' s/"from tempest.common import service_client"/"from tempest_lib.common import rest_client"/ $dest_file
        sed -i='' s/"service_client.ServiceClient"/"rest_client.RestClient"/  $dest_file
        sed -i='' s/"service_client.ResponseBody"/"rest_client.ResponseBody"/ $dest_file
        sed -i='' s/"from tempest\."/"from tempest_lib\."/ $dest_file

        # Replace mocked path in unit tests
        sed -i='' s/"tempest.common.rest_client"/"tempest_lib.common.rest_client"/ $dest_file

        # Remove ".json" from import line
        sed -i='' -e "s/^\(from tempest_lib\.services\..*\)\.json\(.*\)/\1\2/" $dest_file
    fi

    git add "$dest_file"
    if [[ -z "$file_list" ]]; then
        file_list="$filename"
    else
        tmp_file_list="$file_list, $filename"
        char_size=`echo $tmp_file_list | wc -c`
        if [ "$char_size" -lt 27 ]; then
            file_list="$file_list, $filename"
        fi
    fi
done
# Cleanup temporary tempest repo
rm -rf $tmpdir

# Generate a migration commit
commit_message="Migrated $file_list from tempest"
pre_list=$"This migrates the above files from tempest.\nThis includes tempest commits:"
pre_list=`echo -e $pre_list`
post_list=$"to see the commit history for these files refer to the above Change-Ids \nin the tempest repository."
post_list=`echo -e $post_list`
if [ $service_client -eq 1 ]; then
    bp_msg="Partially implements blueprint migrate-service-clients-to-tempest-lib"
else
    bp_msg=""
fi
git commit -m "$commit_message" -m "$pre_list" -m "$CHANGE_LIST" -m "$post_list" -m "$bp_msg"
