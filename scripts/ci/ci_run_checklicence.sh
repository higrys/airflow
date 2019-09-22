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

set -euo pipefail

MY_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export AIRFLOW_CI_SILENT=${AIRFLOW_CI_SILENT:="true"}

# shellcheck source=scripts/ci/utils/_init.sh
. "${MY_DIR}/utils/_init.sh"
# shellcheck source=scripts/ci/utils/_build.sh
. "${MY_DIR}/utils/_build.sh"
# shellcheck source=scripts/ci/utils/_run.sh
. "${MY_DIR}/utils/_run.sh"

script_start

initialize_environment

prepare_build

prepare_run

export FORCE_ANSWER_TO_QUESTIONS="yes"
rebuild_checklicence_image_if_needed

LOCALLY_BUILT_IMAGES=("CHECKLICENCE")
export LOCALLY_BUILT_IMAGES

export FORCE_ANSWER_TO_QUESTIONS="quit"
pre-commit run build
pre-commit run check-apache-license --all-files --show-diff-on-failure

script_end
