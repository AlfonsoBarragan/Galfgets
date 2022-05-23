#!/bin/bash

owlvault_folder=$1  
owlcopy_folder=$2  

let total_files_updated=0

git_regex=".git"
obsidian_regex=".obsidian"

while read -r line; do
    if [[ ! $line =~ $git_regex ]] && [[ ! $line =~ $obsidian_regex ]]; then
        aux="${line//$owlvault_folder/$owlcopy_folder}" 
        line_date=$(date -r "$line" "+%Y%m%d%H%M")
        aux_date=$(date -r "$aux" "+%Y%m%d%H%M")

        if [[ $line_date -gt $aux_date ]]; then
            echo "Updating file $line..."
            cp "$line" "$aux"
            let total_files_updated++
        fi
    fi
done < <(find $1 -type f  -name '*.*')
echo "Total files updated: $total_files_updated"

