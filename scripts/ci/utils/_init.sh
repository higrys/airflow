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

# Assume all the scripts are sourcing the file from the scripts/ci directory
# and MY_DIR variable is set to this directory. It can be overridden however

#
# Sets verbosity of shell in case VERBOSE is true
# Input: VERBOSE
#
function _set_verbosity() {
    if [[ ${VERBOSE:=} == "true" ]]; then
        set -x
    else
        set +x
    fi
}

#
# Sets up airflow sources variable and creates necessary (gitignored) source directories if needed
#
# Input: AIRFLOW_SOURCES
# Output: AIRFLOW_SOURCES
function _setup_airflow_sources() {
    AIRFLOW_SOURCES=${AIRFLOW_SOURCES:=$(cd "${MY_DIR}/../../" && pwd)}
    export AIRFLOW_SOURCES
}

# Creates temp directories
function _create_ignored_directories() {
    mkdir -p "${AIRFLOW_SOURCES}/.mypy_cache"
    mkdir -p "${AIRFLOW_SOURCES}/logs"
    mkdir -p "${AIRFLOW_SOURCES}/tmp"
}

function _set_python_version_for_default_image() {
   PYTHON_VERSION_FOR_DEFAULT_IMAGE="${PYTHON_VERSION_FOR_DEFAULT_IMAGE:="3.6"}"
   export PYTHON_VERSION_FOR_DEFAULT_IMAGE
}
#
# Creates cache directory where we will keep temporary files needed for the build
#
# This directory will be automatically deleted when the script is killed or exists (via trap)
# Unless SKIP_CACHE_DELETION variable is set. You can set this variable and then see
# the output/files generated by the scripts in this directory.
#
# Most useful is out.log file in this directory - storing verbose output of the scripts.
#
# Output: CACHE_TMP_FILE_DIR, OUTPUT_LOG
function _create_temp_cache_directory() {
    CACHE_TMP_FILE_DIR=$(mktemp -d)
    export CACHE_TMP_FILE_DIR

    if [[ ${SKIP_CACHE_DELETION:=} != "true" ]]; then
        trap 'rm -rf -- "${CACHE_TMP_FILE_DIR}"' INT TERM HUP
    fi

    OUTPUT_LOG="${CACHE_TMP_FILE_DIR}/out.log"
    export OUTPUT_LOG
}

#
# Removes temporary cache directory
#
function _remove_temp_cache_directory() {
    if [[ -z "${CACHE_TMP_FILE_DIR}" ]]; then
        rm -rf -- "${CACHE_TMP_FILE_DIR}"
    fi
}

#
# Sets up cache variable and creates the cache directory if needed
#
# Input: AIRFLOW_SOURCES
# Output: BUILD_CACHE_DIR
function _setup_cache_directory() {
    BUILD_CACHE_DIR="${AIRFLOW_SOURCES}/.build"
    export BUILD_CACHE_DIR
    mkdir -p "${BUILD_CACHE_DIR}"
}

#
# Sets up locally built images as array
#
# Output: LOCALLY_BUILT_IMAGES (array)
function _setup_locally_build_images() {
    LOCALLY_BUILT_IMAGES=("CI" "CHECKLICENCE")
    export LOCALLY_BUILT_IMAGES
}

#
# Sets up files that should be checked for rebuilding
# Output: FILES_FOR_REBUILD_CHECK (array)
function _setup_files_for_rebuild(){
    FILES_FOR_REBUILD_CHECK=(
         "setup.py"
         "setup.cfg"
         "Dockerfile"
         "Dockerfile-checklicence"
         ".dockerignore"
         "airflow/version.py"
         "airflow/www/package.json"
         "airflow/www/package-lock.json"
    )
    export FILES_FOR_REBUILD_CHECK
}

#
# Sets up ports forwarded when entering the container
# Output: WEBSERVER_HOST_PORT, POSTGRES_HOST_PORT, MYSQL_HOST_PORT
#
function _setup_forwarded_ports() {
    export WEBSERVER_HOST_PORT=${WEBSERVER_HOST_PORT:="28080"}
    export POSTGRES_HOST_PORT=${POSTGRES_HOST_PORT:="25433"}
    export MYSQL_HOST_PORT=${MYSQL_HOST_PORT:="23306"}
}

#
# Checks if cache is going to be used
function _check_if_cache_used() {
    # You can set AIRFLOW_CONTAINER_USE_CACHE to false if you do not want to use standard Docker
    # cache during build. This way you can test building everything from the scratch
    AIRFLOW_CONTAINER_USE_CACHE=${AIRFLOW_CONTAINER_USE_CACHE:="true"}

    # You can set AIRFLOW_CONTAINER_USE_LOCAL_DOCKER_CACHE to true if you do not want to use
    # pulled images at all but you rely on local cache
    AIRFLOW_CONTAINER_USE_LOCAL_DOCKER_CACHE=${AIRFLOW_CONTAINER_USE_LOCAL_DOCKER_CACHE:="false"}
}

#
# Checks if core utils required in the host system are installed and explain what needs to be done if not
# exits if it's not
function _check_if_coreutils_installed() {
    set +e
    getopt -T >/dev/null
    local GETOPT_RETVAL=$?

    if [[ $(uname -s) == 'Darwin' ]] ; then
        command -v gstat >/dev/null
        local STAT_PRESENT=$?
    else
        command -v stat >/dev/null
        local STAT_PRESENT=$?
    fi

    command -v md5sum >/dev/null
    local MD5SUM_PRESENT=$?

    set -e

    local CMDNAME
    CMDNAME="$(basename -- "$0")"

    ####################  Parsing options/arguments
    if [[ ${GETOPT_RETVAL} != 4 || "${STAT_PRESENT}" != "0" || "${MD5SUM_PRESENT}" != "0" ]]; then
        echo
        if [[ $(uname -s) == 'Darwin' ]] ; then
            echo >&2 "You are running ${CMDNAME} in OSX environment"
            echo >&2 "And you need to install gnu commands"
            echo >&2
            echo >&2 "Run 'brew install gnu-getopt coreutils'"
            echo >&2
            echo >&2 "Then link the gnu-getopt to become default as suggested by brew."
            echo >&2
            echo >&2 "If you use bash, you should run this command:"
            echo >&2
            echo >&2 "echo 'export PATH=\"/usr/local/opt/gnu-getopt/bin:\$PATH\"' >> ~/.bash_profile"
            echo >&2 ". ~/.bash_profile"
            echo >&2
            echo >&2 "If you use zsh, you should run this command:"
            echo >&2
            echo >&2 "echo 'export PATH=\"/usr/local/opt/gnu-getopt/bin:\$PATH\"' >> ~/.zprofile"
            echo >&2 ". ~/.zprofile"
            echo >&2
            echo >&2 "Login and logout afterwards !!"
            echo >&2
            echo >&2 "After re-login, your PATH variable should start with \"/usr/local/opt/gnu-getopt/bin\""
            echo >&2 "Your current path is ${PATH}"
            echo >&2
        else
            echo >&2 "You do not have necessary tools in your path (getopt, stat, md5sum)."
            echo >&2 "Please install latest/GNU version of getopt and coreutils."
            echo >&2 "This can usually be done with 'apt install util-linux coreutils'"
        fi
        echo
        exit 1
    fi
}

#
# Asserts that we are not inside of the container
#
function _assert_not_in_container() {
    if [[ -f /.dockerenv && ! ${SKIP_DOCKER_CONTAINER_CHECK:="false"} == "true" ]]; then
        echo >&2
        echo >&2 "You are inside the Airflow docker container!"
        echo >&2 "You should only run this script from the host."
        echo >&2 "Learn more about how we develop and test airflow in:"
        echo >&2 "https://github.com/apache/airflow/blob/master/CONTRIBUTING.md"
        echo >&2
        exit 1
    fi
}

#
# Prints message on the stdout if VERBOSE == True  AIRFLOW_CI_SILENT != true
# Input: VERBOSE, AIRFLOW_CI_SILENT
function print_info() {
    if [[ ${VERBOSE:="false"} == "true" || ${AIRFLOW_CI_SILENT:="false"} != "true" ]]; then
        echo "$@"
    fi
}

#
# Starts the script/ If VERBOSE variable is set to true, it enables verbose output of commands executed
# Also prints some useful diagnostics information at start of the script
#
function script_start {
    print_info
    print_info "Running $(basename "$0")"
    print_info
    print_info
    if [[ ${VERBOSE:=} == "true" ]]; then
        print_info
        print_info "Variable VERBOSE Set to \"true\""
        print_info "You will see a lot of output"
        print_info
        set -x
    else
        print_info "You can increase verbosity by running 'export VERBOSE=\"true\""
        if [[ ${SKIP_CACHE_DELETION:=} != "true" ]]; then
            print_info "And skip deleting the output file with 'export SKIP_CACHE_DELETION=\"true\""
        fi
        print_info
        set +x
    fi
    START_SCRIPT_TIME=$(date +%s)
}

#
#
# Disables verbosity in the script
#
function script_end {
    if [[ ${VERBOSE:=} == "true" ]]; then
        set +x
    fi
    END_SCRIPT_TIME=$(date +%s)
    RUN_SCRIPT_TIME=$((END_SCRIPT_TIME-START_SCRIPT_TIME))
    print_info
    print_info "Finished the script $(basename "$0")"
    print_info "It took ${RUN_SCRIPT_TIME} seconds"
    print_info
    _remove_temp_cache_directory
}

function verbose_docker() {
    echo "docker" "${@}"
    docker "${@}"
}

function spin() {
    local FILE_TO_MONITOR=${1}
    local SPIN=("-" "\\" "|" "/")
    echo -n " Build log: ${FILE_TO_MONITOR} ${SPIN[0]}" > "${DETECTED_TERMINAL}"

    while "true"
    do
      for i in "${SPIN[@]}"
      do
            echo -ne "\b$i" > "${DETECTED_TERMINAL}"
            local LAST_FILE_SIZE
            local FILE_SIZE
            LAST_FILE_SIZE=$(set +e; wc -c "${FILE_TO_MONITOR}" 2>/dev/null | awk '{print $1}' || true)
            FILE_SIZE=${LAST_FILE_SIZE}
            while [[ "${LAST_FILE_SIZE}" == "${FILE_SIZE}" ]];
            do
                FILE_SIZE=$(set +e; wc -c "${FILE_TO_MONITOR}" 2>/dev/null | awk '{print $1}' || true)
                sleep 0.2
            done
            LAST_FILE_SIZE=FILE_SIZE
            sleep 0.2
            if [[ ! -f "${FILE_TO_MONITOR}" ]]; then
                exit
            fi
      done
    done
}

_assert_not_in_container
_setup_airflow_sources

# shellcheck source=scripts/ci/utils/_autodetect_variables.sh
. "${AIRFLOW_SOURCES}/scripts/ci/utils/_autodetect_variables.sh"

#
# Performs basic sanity checks common for most of the scripts in this directory
#
function initialize_environment() {
    _set_verbosity
    _set_python_version_for_default_image
    _create_ignored_directories
    _create_temp_cache_directory
    autodetect_variables
    _setup_cache_directory
    _setup_locally_build_images
    _setup_files_for_rebuild
    _setup_forwarded_ports
    _check_if_cache_used
    _check_if_coreutils_installed
}
