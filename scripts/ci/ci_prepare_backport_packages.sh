#!/usr/bin/env bash
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
export PYTHON_VERSION=${PYTHON_VERSION:-3.6}

# shellcheck source=scripts/ci/_script_init.sh
. "$( dirname "${BASH_SOURCE[0]}" )/_script_init.sh"

LIST_OF_DIRS_FILE=$(mktemp)

cd "${MY_DIR}/../../airflow/providers" || exit 1

find . -type d | sed 's/.\///' | sed 's/\//\./' | grep -E 'hooks|operators|sensors|secrets' \
    > "${LIST_OF_DIRS_FILE}"

cd "${MY_DIR}/../../backport_packages" || exit 1

rm -rf dist/*
rm -rf -- *.egg-info

if [[ -z "$*" ]]; then
    BACKPORT_PACKAGES=$(python3 setup_backport_packages.py list-backport-packages)

    PACKAGE_ERROR="false"
    # Check if all providers are included
    for PACKAGE in ${BACKPORT_PACKAGES}
    do
        if ! grep -E "^${PACKAGE}" <"${LIST_OF_DIRS_FILE}" >/dev/null; then
            echo "The package ${PACKAGE} is not available in providers dir"
            PACKAGE_ERROR="true"
        fi
        sed -i "/^${PACKAGE}.*/d" "${LIST_OF_DIRS_FILE}"
    done

    if [[ ${PACKAGE_ERROR} == "true" ]]; then
        echo
        echo "ERROR! Some packages from backport_packages/setup_backport_packages.py are missing in providers dir"
        exit 1
    fi

    NUM_LINES=$(wc -l "${LIST_OF_DIRS_FILE}" | awk '{ print $1 }')
    if [[ ${NUM_LINES} != "0" ]]; then
        echo "ERROR! Some folders from providers package are not defined"
        echo "       Please add them to backport_packages/setup_backport_packages.py:"
        echo
        cat "${LIST_OF_DIRS_FILE}"
        echo
        exit 1
    fi
else
    if [[ "$1" == "--help" ]]; then
        echo
        echo "Builds all backport packages."
        echo
        echo "You can provide list of packages to build out of:"
        echo
        python3 setup_backport_packages.py list-backport-packages | tr '\n ' ' ' | fold -w 100 -s
        echo
        echo
        exit
    fi
    BACKPORT_PACKAGES="$*"
fi

echo "==================================================================================="
echo " Copying sources and doing refactor for backporting"
echo "==================================================================================="
python3 setup_backport_packages.py prepare

for BACKPORT_PACKAGE in ${BACKPORT_PACKAGES}
do
    echo "==================================================================================="
    echo " Preparing backporting package ${BACKPORT_PACKAGE}"
    echo "-----------------------------------------------------------------------------------"
    python3 setup_backport_packages.py "${BACKPORT_PACKAGE}" clean --all >/dev/null 2>&1
    python3 setup_backport_packages.py "${BACKPORT_PACKAGE}" sdist bdist_wheel >/dev/null 2>&1
    echo " Prepared backporting package ${BACKPORT_PACKAGE}"
done
echo "==================================================================================="
