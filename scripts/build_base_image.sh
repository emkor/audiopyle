#!/usr/bin/env bash

# check commit hash of current ./base directory
base_image_commit_hash=$(git log -n 1 --format="%H" -- ./base)

# try pulling image, save if image was found (status 0) or not (status 1)
pull_by_commit_hash_status=$(docker pull endlessdrones/audiopyle-base:${base_image_commit_hash})

# build the image only when pull failed
if [ "$pull_by_commit_hash_status" = 1 ]; then
    echo "Could not download image for commit hash ${base_image_commit_hash}, building..."
    docker build -t endlessdrones/audiopyle-base:latest -t endlessdrones/audiopyle-base:${base_image_commit_hash} ./base
else
    echo "Downloaded image with commit hash ${base_image_commit_hash}, omitting build"
fi