#!/usr/bin/env bash
for ubuntu in 16.04 18.04; do
    image=pdfparser:${ubuntu}
    docker build --build-arg UBUNTU_VERSION=$ubuntu -t pdfparser:${ubuntu} .
    # get the built artifacts out
    artifact_dir=artifacts/${ubuntu}
    mkdir -p $artifact_dir
    docker run --rm -v $(pwd)/${artifact_dir}:/artifacts --user $(id -u):$(id -g) $image sh -c 'cp -r dist/* /artifacts'
    if [ "$ubuntu" = "18.04" ]; then
      scripts/add_ubuntu_suffix.py -s bionic ${artifact_dir}/*.whl
    fi
done
