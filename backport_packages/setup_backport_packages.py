#
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
"""Setup.py for the Backport packages of Airflow project."""
import collections
import io
import json
import logging
import os
import pkgutil
import re
import subprocess
import sys
import textwrap
from importlib import util
from inspect import isclass
from os import listdir
from os.path import dirname
from shutil import copyfile, copytree, rmtree
from typing import Any, Dict, List, Optional, Set

from jinja2 import Template
from setuptools import Command, find_packages, setup as setuptools_setup
from tabulate import tabulate

from tests.test_core_to_contrib import HOOK, OPERATOR, PROTOCOLS, SENSOR

# noinspection DuplicatedCode
logger = logging.getLogger(__name__)

# Kept manually in sync with airflow.__version__
# noinspection PyUnresolvedReferences
spec = util.spec_from_file_location("airflow.version", os.path.join('airflow', 'version.py'))
# noinspection PyUnresolvedReferences
mod = util.module_from_spec(spec)
spec.loader.exec_module(mod)  # type: ignore
version = mod.version  # type: ignore

PY3 = sys.version_info[0] == 3

MY_DIR_PATH = os.path.dirname(__file__)
SOURCE_DIR_PATH = os.path.abspath(os.path.join(MY_DIR_PATH, os.pardir))
AIRFLOW_PATH = os.path.join(SOURCE_DIR_PATH, "airflow")
PROVIDERS_PATH = os.path.join(AIRFLOW_PATH, "providers")

# noinspection PyUnboundLocalVariable
try:
    with io.open('README.md', encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = ''


class CleanCommand(Command):
    """
    Command to tidy up the project root.
    Registered as cmd class in setup() so it can be called with ``python setup.py extra_clean``.
    """

    description = "Tidy up the project root"
    user_options = []  # type: List[str]

    def initialize_options(self):
        """Set default values for options."""

    def finalize_options(self):
        """Set final values for options."""

    # noinspection PyMethodMayBeStatic
    def run(self):
        """Run command to remove temporary files and directories."""
        os.chdir(dirname(__file__))
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info')


sys.path.insert(0, SOURCE_DIR_PATH)

import setup  # From AIRFLOW_SOURCES/setup.py # noqa  # isort:skip

PROVIDERS_REQUIREMENTS: Dict[str, List[str]] = {
    "amazon": setup.aws,
    "apache.cassandra": setup.cassandra,
    "apache.druid": setup.druid,
    "apache.hdfs": setup.hdfs,
    "apache.hive": setup.hive,
    "apache.livy": [],
    "apache.pig": [],
    "apache.pinot": setup.pinot,
    "apache.spark": setup.spark,
    "apache.sqoop": [],
    "celery": setup.celery,
    "cloudant": setup.cloudant,
    "cncf.kubernetes": setup.kubernetes,
    "databricks": setup.databricks,
    "datadog": setup.datadog,
    "dingding": [],
    "discord": [],
    "docker": setup.docker,
    "email": [],
    "elasticsearch": [],
    "exasol": setup.exasol,
    "facebook": setup.facebook,
    "ftp": [],
    "google": setup.google,
    "grpc": setup.grpc,
    "hashicorp": setup.hashicorp,
    "http": [],
    "imap": [],
    "jdbc": setup.jdbc,
    "jenkins": setup.jenkins,
    "jira": setup.jira,
    "microsoft.azure": setup.azure,
    "microsoft.mssql": setup.mssql,
    "microsoft.winrm": setup.winrm,
    "mongo": setup.mongo,
    "mysql": setup.mysql,
    "odbc": setup.odbc,
    "openfaas": [],
    "opsgenie": [],
    "oracle": setup.oracle,
    "pagerduty": setup.pagerduty,
    "papermill": setup.papermill,
    "postgres": setup.postgres,
    "presto": setup.presto,
    "qubole": setup.qds,
    "redis": setup.redis,
    "salesforce": setup.salesforce,
    "samba": setup.samba,
    "segment": setup.segment,
    "sftp": setup.ssh,
    "singularity": setup.singularity,
    "slack": setup.slack,
    "snowflake": setup.snowflake,
    "sqlite": [],
    "ssh": setup.ssh,
    "vertica": setup.vertica,
    "yandex": [],
    "zendesk": setup.zendesk,
}

DEPENDENCIES_JSON_FILE = os.path.join(PROVIDERS_PATH, "dependencies.json")

MOVED_OPERATORS_DICT = {value[0]: value[1] for value in OPERATOR}
MOVED_SENSORS_DICT = {value[0]: value[1] for value in SENSOR}
MOVED_HOOKS_DICT = {value[0]: value[1] for value in HOOK}
MOVED_PROTOCOLS_DICT = {value[0]: value[1] for value in PROTOCOLS}


def change_import_paths_to_deprecated():
    from bowler import LN, TOKEN, Capture, Filename, Query
    from fissix.pytree import Leaf
    from fissix.fixer_util import KeywordArg, Name, Comma

    # noinspection PyUnusedLocal
    def remove_tags_modifier(_: LN, capture: Capture, filename: Filename) -> None:
        for node in capture['function_arguments'][0].post_order():
            if isinstance(node, Leaf) and node.value == "tags" and node.type == TOKEN.NAME:
                if node.parent.next_sibling and node.parent.next_sibling.value == ",":
                    node.parent.next_sibling.remove()
                node.parent.remove()

    # noinspection PyUnusedLocal
    def pure_airflow_models_filter(node: LN, capture: Capture, filename: Filename) -> bool:
        """Check if select is exactly [airflow, . , models]"""
        return len([ch for ch in node.children[1].leaves()]) == 3

    # noinspection PyUnusedLocal
    def remove_super_init_call(node: LN, capture: Capture, filename: Filename) -> None:
        for ch in node.post_order():
            if isinstance(ch, Leaf) and ch.value == "super":
                if any(c.value for c in ch.parent.post_order() if isinstance(c, Leaf)):
                    ch.parent.remove()

    # noinspection PyUnusedLocal
    def add_provide_context_to_python_operator(node: LN, capture: Capture, filename: Filename) -> None:
        fn_args = capture['function_arguments'][0]
        fn_args.append_child(Comma())

        provide_context_arg = KeywordArg(Name('provide_context'), Name('True'))
        provide_context_arg.prefix = fn_args.children[0].prefix
        fn_args.append_child(provide_context_arg)

    def remove_class(query, class_name) -> None:
        # noinspection PyUnusedLocal
        def _remover(node: LN, capture: Capture, filename: Filename) -> None:
            if node.type not in (300, 311):  # remove only definition
                node.remove()

        query.select_class(class_name).modify(_remover)

    changes = [
        ("airflow.operators.bash", "airflow.operators.bash_operator"),
        ("airflow.operators.python", "airflow.operators.python_operator"),
        ("airflow.utils.session", "airflow.utils.db"),
        (
            "airflow.providers.cncf.kubernetes.operators.kubernetes_pod",
            "airflow.contrib.operators.kubernetes_pod_operator"
        ),
    ]

    qry = Query()
    for new, old in changes:
        qry.select_module(new).rename(old)

    # Move and refactor imports for DataFlow
    copyfile(
        os.path.join(dirname(__file__), os.pardir, "airflow", "utils", "python_virtualenv.py"),
        os.path.join(
            dirname(__file__), "airflow", "providers", "google", "cloud", "utils", "python_virtualenv.py"
        )
    )
    (
        qry
            .select_module("airflow.utils.python_virtualenv")
            .rename("airflow.providers.google.cloud.utils.python_virtualenv")
    )
    copyfile(
        os.path.join(dirname(__file__), os.pardir, "airflow", "utils", "process_utils.py"),
        os.path.join(
            dirname(__file__), "airflow", "providers", "google", "cloud", "utils", "process_utils.py"
        )
    )
    (
        qry
            .select_module("airflow.utils.process_utils")
            .rename("airflow.providers.google.cloud.utils.process_utils")
    )

    # Remove tags
    qry.select_method("DAG").is_call().modify(remove_tags_modifier)

    # Fix AWS import in Google Cloud Transfer Service
    (
        qry
            .select_module("airflow.providers.amazon.aws.hooks.base_aws")
            .is_filename(include=r"cloud_storage_transfer_service\.py")
            .rename("airflow.contrib.hooks.aws_hook")
    )

    (
        qry
            .select_class("AwsBaseHook")
            .is_filename(include=r"cloud_storage_transfer_service\.py")
            .filter(lambda n, c, f: n.type == 300)  # noqa
            .rename("AwsHook")
    )

    # Fix BaseOperatorLinks imports
    files = r"bigquery\.py|mlengine\.py"  # noqa
    qry.select_module("airflow.models").is_filename(include=files).filter(pure_airflow_models_filter).rename(
        "airflow.models.baseoperator")

    # Fix super().__init__() call in hooks
    qry.select_subclass("BaseHook").modify(remove_super_init_call)

    (
        qry.select_function("PythonOperator")
            .is_call()
            .is_filename(include=r"mlengine_operator_utils.py$")
            .modify(add_provide_context_to_python_operator)
    )

    (
        qry.select_function("BranchPythonOperator")
            .is_call()
            .is_filename(include=r"example_google_api_to_s3_transfer_advanced.py$")
            .modify(add_provide_context_to_python_operator)
    )

    # Remove new class and rename usages of old
    remove_class(qry, "GKEStartPodOperator")
    (
        qry
            .select_class("GKEStartPodOperator")
            .is_filename(include=r"example_kubernetes_engine\.py")
            .rename("GKEPodOperator")
    )

    qry.execute(write=True, silent=False, interactive=False)

    # Add old import to GKE
    gke_path = os.path.join(
        dirname(__file__), "airflow", "providers", "google", "cloud", "operators", "kubernetes_engine.py"
    )
    with open(gke_path, "a") as f:  # noqa
        f.writelines(["", "from airflow.contrib.operators.gcp_container_operator import GKEPodOperator"])


def get_source_providers_folder():
    return os.path.join(dirname(__file__), os.pardir, "airflow", "providers")


def get_providers_folder():
    return os.path.join(dirname(__file__), "airflow", "providers")


def get_providers_package_folder(provider_package_id: str):
    return os.path.join(get_providers_folder(), *provider_package_id.split("."))


def get_provider_package_name(provider_package_id: str):
    return "apache-airflow-backport-providers-" + provider_package_id.replace(".", "-")


def copy_provider_sources():
    rm_build_dir()
    package_providers_dir = get_providers_folder()
    if os.path.isdir(package_providers_dir):
        rmtree(package_providers_dir)
    copytree(get_source_providers_folder(), get_providers_folder())


def rm_build_dir():
    build_dir = os.path.join(dirname(__file__), "build")
    if os.path.isdir(build_dir):
        rmtree(build_dir)


def copy_and_refactor_sources():
    copy_provider_sources()
    change_import_paths_to_deprecated()


def get_readme(package_folder: str, name: str) -> str:
    backport_file_path = os.path.join(package_folder, name)
    if os.path.isfile(backport_file_path):
        with open(backport_file_path, "rt") as backport_readme:
            return backport_readme.read()
    else:
        return ""


def get_long_description(provider_package_id: str) -> str:
    package_folder = get_providers_package_folder(provider_package_id)
    with open(os.path.join(package_folder, "README.md")) as readme_file:
        return readme_file.read()


def do_setup_package_providers(provider_package_id: str,
                               package_dependencies: List[str], extras: Dict[str, List[str]]):
    setup.write_version()
    provider_package_name = get_provider_package_name(provider_package_id)
    package_name = f'{provider_package_name}'
    package_prefix = f'airflow.providers.{provider_package_id}'
    found_packages = find_packages()
    found_packages = [package for package in found_packages if package.startswith(package_prefix)]
    setuptools_setup(
        name=package_name,
        description=f'Back-ported {package_name} package for Airflow 1.10.*',
        long_description=get_long_description(provider_package_id),
        long_description_content_type='text/markdown',
        license='Apache License 2.0',
        version='2020.04.27.rc1',
        packages=found_packages,
        package_data={
            '': ["airflow/providers/cncf/kubernetes/example_dags/*.yaml"],
        },

        include_package_data=True,
        zip_safe=False,
        install_requires=['apache-airflow~=1.10'] + package_dependencies,
        extras_require=extras,
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Topic :: System :: Monitoring',
        ],
        setup_requires=[
            'bowler',
            'docutils',
            'gitpython',
            'setuptools',
            'wheel',
        ],
        python_requires='>=3.6',
    )


def find_package_extras(package: str) -> Dict[str, List[str]]:
    """Finds extras for the packages"""
    if package == 'providers':
        return {}
    with open(DEPENDENCIES_JSON_FILE, "rt") as dependencies_file:
        cross_provider_dependencies: Dict[str, List[str]] = json.load(dependencies_file)
    extras_dict = {module: [get_provider_package_name(module)]
                   for module in cross_provider_dependencies[package]} \
        if cross_provider_dependencies.get(package) else {}
    return extras_dict


def get_provider_packages():
    """Returns all packages available in providers"""
    return list(PROVIDERS_REQUIREMENTS)


def usage():
    print()
    print("You should provide PACKAGE as first of the setup.py arguments")
    packages = get_provider_packages()
    out = ""
    for package in packages:
        out += f"{package} "
    out_array = textwrap.wrap(out, 80)
    print(f"Available packages: ")
    print()
    for text in out_array:
        print(text)
    print()
    print("You can see all packages configured by specifying list-backport-packages as first argument")
    print("You can generate release notes by specifying:"
          " update-package-release-notes YYYY.MM.DD [PACKAGES]")


# return list of tuples (objclass, name) containing all subclasses in package specified
def find_all_subclasses(full_package: str, class_type, expected_in_package_name: str = None,
                        exclude_class_type=None):
    import inspect
    subclasses = set()
    for global_name, global_object in globals().items():
        if global_name.startswith(full_package) and inspect.isclass(global_object):
            mro = inspect.getmro(global_object)
            if global_object is not class_type and \
                class_type in mro and \
                "example_dags" not in global_name and \
                (expected_in_package_name is None or expected_in_package_name in global_name) and \
                (exclude_class_type is None or exclude_class_type not in mro) \
                    and global_object.__module__.startswith(full_package):
                subclasses.add(global_name)
    return subclasses


def get_new_and_moved_objects(objects: Set[str], test_moved_object_dict: Dict[str, str]):
    new_objects = []
    moved_objects = {}
    for obj in objects:
        if obj in test_moved_object_dict:
            moved_objects[obj] = test_moved_object_dict[obj]
            del test_moved_object_dict[obj]
        else:
            new_objects.append(obj)
    new_objects.sort()
    return new_objects, moved_objects


def strip_package(base_package: str, obj_name: str):
    if obj_name.startswith(base_package):
        return obj_name[len(base_package) + 1:]
    else:
        return obj_name


def convert_obj_name_to_url(prefix: str, obj_name):
    return prefix + "/".join(obj_name.split(".")[:-1]) + ".py"


def get_object_code_link(base_package: str, obj_name: str, tag: str):
    url_prefix = f'https://github.com/apache/airflow/blob/{tag}/'
    return f'[{strip_package(base_package, obj_name)}]({convert_obj_name_to_url(url_prefix, obj_name)})'


def convert_new_objects_to_table(obj_list: List[str], full_package_name: str, object_type: str):
    headers = [f"New Airflow 2.0 {object_type}: `{full_package_name}` package"]
    table = [(get_object_code_link(full_package_name, obj, "master"),) for obj in obj_list]
    return tabulate(table, headers=headers, tablefmt="pipe")


def convert_moved_objects_to_table(obj_dict: Dict[str, str], full_package_name: str, object_type: str):
    headers = [f"Airflow 2.0 {object_type}: `{full_package_name}` package",
               f"Airflow 1.10.* previous location (usually `airflow.contrib`)"]
    table = [
        (get_object_code_link(full_package_name, obj, "master"),
         get_object_code_link("airflow.contrib", obj_dict[obj], "v1-10-stable"))
        for obj in sorted(obj_dict.keys())
    ]
    return tabulate(table, headers=headers, tablefmt="pipe")


def get_package_class_summary(full_package_name: str):
    from airflow.sensors.base_sensor_operator import BaseSensorOperator
    from airflow.hooks.base_hook import BaseHook
    from airflow.models.baseoperator import BaseOperator
    from typing_extensions import Protocol
    operators = find_all_subclasses(full_package=full_package_name,
                                    class_type=BaseOperator,
                                    expected_in_package_name=".operators.",
                                    exclude_class_type=BaseSensorOperator)
    sensors = find_all_subclasses(full_package=full_package_name,
                                  class_type=BaseSensorOperator,
                                  expected_in_package_name='.sensors.')
    hooks = find_all_subclasses(full_package=full_package_name,
                                class_type=BaseHook,
                                expected_in_package_name='.hooks.')
    protocols = find_all_subclasses(full_package=full_package_name,
                                    class_type=Protocol)
    new_operators, moved_operators = get_new_and_moved_objects(operators, MOVED_OPERATORS_DICT)
    new_sensors, moved_sensors = get_new_and_moved_objects(sensors, MOVED_SENSORS_DICT)
    new_hooks, moved_hooks = get_new_and_moved_objects(hooks, MOVED_HOOKS_DICT)
    new_protocols, moved_protocols = get_new_and_moved_objects(protocols, MOVED_PROTOCOLS_DICT)
    class_summary = {
        "NEW_OPERATORS": new_operators,
        "MOVED_OPERATORS": moved_operators,
        "NEW_SENSORS": new_sensors,
        "MOVED_SENSORS": moved_sensors,
        "NEW_HOOKS": new_hooks,
        "MOVED_HOOKS": moved_hooks,
        "NEW_PROTOCOLS": new_protocols,
        "MOVED_PROTOCOLS": moved_protocols,
    }
    for from_name, to_name, object_type in [
        ("NEW_OPERATORS", "NEW_OPERATORS_TABLE", "operators"),
        ("NEW_SENSORS", "NEW_SENSORS_TABLE", "sensors"),
        ("NEW_HOOKS", "NEW_HOOKS_TABLE", "hooks"),
        ("NEW_PROTOCOLS", "NEW_PROTOCOLS_TABLE", "protocols"),
    ]:
        class_summary[to_name] = convert_new_objects_to_table(class_summary[from_name],
                                                              full_package_name,
                                                              object_type)
    for from_name, to_name, object_type in [
        ("MOVED_OPERATORS", "MOVED_OPERATORS_TABLE", "operators"),
        ("MOVED_SENSORS", "MOVED_SENSORS_TABLE", "sensors"),
        ("MOVED_HOOKS", "MOVED_HOOKS_TABLE", "hooks"),
        ("MOVED_PROTOCOLS", "MOVED_PROTOCOLS_TABLE", "protocols"),
    ]:
        class_summary[to_name] = convert_moved_objects_to_table(class_summary[from_name],
                                                                full_package_name,
                                                                object_type)
    return class_summary


def prepare_readme_from_template(template_name: str, context: Dict[str, Any]):
    template_file_path = os.path.join(MY_DIR_PATH, f"{template_name}_TEMPLATE.md.jinja2")
    with open(template_file_path, "rt") as template_file:
        # remove comment
        template = Template(template_file.read(), autoescape=True)
    return template.render(**context)


def convert_git_changes_to_table(changes: str, commit_url_prefix: str):
    lines = changes.split("\n")
    headers = ["Commit", "Subject"]
    table_data = []
    for line in lines:
        full_hash, short_hash, message = line.split(" ", maxsplit=2)
        table_data.append((f"[{short_hash}]({commit_url_prefix}{full_hash})", message))

    return tabulate(table_data, headers=headers, tablefmt="pipe")


def convert_pip_requirements_to_table(requirements: List[str]):
    headers = ["PIP package", "Version required"]
    table_data = []
    for dependency in requirements:
        found = re.match(r"(^[^<=>~]*)([^<=>~]?.*)$", dependency)
        if found:
            package = found.group(1)
            version_required = found.group(2)
            table_data.append((package, version_required))
        else:
            table_data.append((dependency, ""))
    return tabulate(table_data, headers=headers, tablefmt="pipe")


def convert_cross_package_dependencies_to_table(cross_package_dependencies: List[str], url_prefix: str):
    headers = ["Dependent package"]
    table_data = []
    for dependency in cross_package_dependencies:
        pip_package_name = f"apache-airflow-backport-providers-{dependency.replace('.','-')}"
        url_suffix = f"{dependency.replace('.','/')}"
        table_data.append((f"[{pip_package_name}]({url_prefix}{url_suffix})",))
    return tabulate(table_data, headers=headers, tablefmt="pipe")


LICENCE = """<!--
 Licensed to the Apache Software Foundation (ASF) under one
 or more contributor license agreements.  See the NOTICE file
 distributed with this work for additional information
 regarding copyright ownership.  The ASF licenses this file
 to you under the Apache License, Version 2.0 (the
 "License"); you may not use this file except in compliance
 with the License.  You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing,
 software distributed under the License is distributed on an
 "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 KIND, either express or implied.  See the License for the
 specific language governing permissions and limitations
 under the License.
 -->
"""

PROVIDERS_CHANGES_PREFIX = "PROVIDERS_CHANGES_"

ReleaseInfo = collections.namedtuple("ReleaseInfo", "release_version last_commit_hash content file_name")


def get_all_releases(package_path: str) -> List[ReleaseInfo]:
    past_releases: List[ReleaseInfo] = []
    changes_file_names = listdir(package_path)
    for file_name in sorted(changes_file_names, reverse=True):
        if file_name.startswith(PROVIDERS_CHANGES_PREFIX) and file_name.endswith(".md"):
            changes_file_path = os.path.join(package_path, file_name)
            with open(changes_file_path, "rt") as changes_file:
                content = changes_file.read()
            # Find first commit
            found = re.search(r'/([a-z0-9]*)\)', content, flags=re.MULTILINE)
            if not found:
                raise Exception(f"Commit not found in {changes_file_path}. Something is wrong there.")
            last_commit_hash = found.group(1)
            release_version = file_name[len(PROVIDERS_CHANGES_PREFIX):][:-3]
            past_releases.append(ReleaseInfo(release_version=release_version,
                                             last_commit_hash=last_commit_hash,
                                             content=content,
                                             file_name=file_name))
    return past_releases


def get_previous_release(last_release: str,
                         past_releases: List[ReleaseInfo],
                         current_release_version: str) -> Optional[str]:
    previous_release = None
    if last_release == current_release_version:
        # Re-running for current release - use previous release as base for git log
        if len(past_releases) > 1:
            previous_release = past_releases[1].last_commit_hash
    else:
        previous_release = past_releases[0].last_commit_hash if past_releases else None
    return previous_release


def check_if_release_version_ok(past_releases, release_version):
    last_release = past_releases[0].release_version if past_releases else None
    if last_release and last_release > release_version:
        print(f"The release {release_version} must be not less than "
              f"{last_release} - last release for the package")
        sys.exit(2)
    return last_release


def get_cross_provider_dependent_packages(package_id: str) -> List[str]:
    with open(os.path.join(PROVIDERS_PATH, "dependencies.json"), "rt") as dependencies_file:
        dependent_packages = json.load(dependencies_file).get(package_id) or []
    return dependent_packages


def get_git_command(previous_release):
    git_cmd = ["git", "log", "--pretty=format:%H %h %s"]
    if previous_release:
        git_cmd.append(f"{previous_release}...HEAD")
    git_cmd.extend(['--', '.'])
    return git_cmd


def store_current_changes(package_path: str, current_release_version: str, current_changes: str):
    current_changes_file_path = os.path.join(package_path,
                                             PROVIDERS_CHANGES_PREFIX + current_release_version + ".md")
    with open(current_changes_file_path, "wt") as current_changes_file:
        current_changes_file.write(current_changes)
        current_changes_file.write("\n")


def update_release_notes_for_package(package_id: str, current_release_version: str):
    full_package_name = f"airflow.providers.{package_id}"
    package_path = os.path.join(PROVIDERS_PATH, *package_id.split("."))
    class_summary = get_package_class_summary(full_package_name)
    past_releases = get_all_releases(package_path=package_path)
    last_release = check_if_release_version_ok(past_releases, current_release_version)
    cross_providers_dependencies = get_cross_provider_dependent_packages(package_id=package_id)
    previous_release = get_previous_release(last_release=last_release, past_releases=past_releases,
                                            current_release_version=current_release_version)
    git_cmd = get_git_command(previous_release)
    changes = subprocess.check_output(git_cmd, cwd=package_path, universal_newlines=True)
    if changes == "":
        print(f"The code has not changed since last release {last_release}. Skipping generating README.")
        return
    changes_table = convert_git_changes_to_table(
        changes,
        commit_url_prefix="https://github.com/apache/airflow/commit/")
    pip_requirements_table = convert_pip_requirements_to_table(PROVIDERS_REQUIREMENTS[package_id])
    cross_providers_dependencies_table = \
        convert_cross_package_dependencies_to_table(
            cross_providers_dependencies,
            url_prefix="https://github.com/apache/airflow/tree/master/airflow/providers/")
    context: Dict[str, Any] = {
        "PACKAGE_ID": package_id,
        "PACKAGE_PIP_NAME": f"apache-airflow-backport-providers-{package_id.replace('.', '-')}",
        "FULL_PACKAGE_NAME": full_package_name,
        "RELEASE": current_release_version,
        "CURRENT_CHANGES_TABLE": changes_table,
        "CROSS_PROVIDERS_DEPENDENCIES": cross_providers_dependencies,
        "CROSS_PROVIDERS_DEPENDENCIES_TABLE": cross_providers_dependencies_table,
        "PIP_REQUIREMENTS": PROVIDERS_REQUIREMENTS[package_id],
        "PIP_REQUIREMENTS_TABLE": pip_requirements_table
    }
    current_changes = prepare_readme_from_template(template_name="PROVIDERS_CHANGES", context=context)
    store_current_changes(package_path=package_path, current_release_version=current_release_version,
                          current_changes=current_changes)
    context.update(class_summary)
    all_releases = get_all_releases(package_path)
    context["RELEASES"] = all_releases
    readme = LICENCE
    readme += prepare_readme_from_template(template_name="PROVIDERS_README", context=context)
    readme += prepare_readme_from_template(template_name="PROVIDERS_CLASSES", context=context)
    for a_release in all_releases:
        readme += a_release.content
    readme_file_path = os.path.join(package_path, "README.md")
    with open(readme_file_path, "wt") as readme_file:
        readme_file.write(readme)
    print(f"Generated {readme_file_path} file for the {package_id} provider")


def import_all_providers_classes():
    for loader, module_name, is_pkg in pkgutil.walk_packages([SOURCE_DIR_PATH]):
        if module_name.startswith("airflow.providers"):
            # TODO: remove this exclusion once hdfs works for python 3
            # https://github.com/apache/airflow/pull/5659
            if not module_name.endswith(".hdfs"):
                _module = loader.find_module(module_name).load_module(module_name)
                globals()[module_name] = _module
                for attribute_name in dir(_module):
                    attribute = getattr(_module, attribute_name)
                    if isclass(attribute):
                        globals()[module_name + "." + attribute_name] = attribute


def update_release_notes_for_packages(package_list: List[str], release_version: str):
    """
    Updates release notes for packages specified
    """
    import_all_providers_classes()
    if len(package_list) == 0:
        package_list = PROVIDERS_REQUIREMENTS.keys()
    for package in package_list:
        update_release_notes_for_package(package, release_version)


if __name__ == "__main__":
    LIST_BACKPORT_PACKAGES = "list-backport-packages"
    UPDATE_PACKAGE_RELEASE_NOTES = "update-package-release-notes"

    possible_first_params = get_provider_packages()
    possible_first_params.append(LIST_BACKPORT_PACKAGES)
    possible_first_params.append(UPDATE_PACKAGE_RELEASE_NOTES)
    if len(sys.argv) == 1:
        print()
        print("ERROR! Missing first param")
        print()
        usage()
    elif sys.argv[1] == "prepare":
        print("Copying sources and doing refactor")
        copy_and_refactor_sources()
    elif sys.argv[1] not in possible_first_params:
        print()
        print(f"ERROR! Wrong first param: {sys.argv[1]}")
        print()
        usage()
    elif "--help" in sys.argv or "-h" in sys.argv or len(sys.argv) < 2:
        usage()
    elif len(sys.argv) > 1 and sys.argv[1] == LIST_BACKPORT_PACKAGES:
        for key in PROVIDERS_REQUIREMENTS:
            print(key)
    elif len(sys.argv) > 1 and sys.argv[1] == UPDATE_PACKAGE_RELEASE_NOTES:
        if len(sys.argv) == 2 or not re.match(r'\d{4}\.\d{2}\.\d{2}', sys.argv[2]):
            print("Please provide release tag as parameter in the form of YYYY.MM.DD")
            sys.exit(1)
        release = sys.argv[2]
        update_release_notes_for_packages(sys.argv[3:], release_version=release)

    else:
        provider_package = sys.argv[1]
        if provider_package not in get_provider_packages():
            raise Exception(f"The package {provider_package} is not a backport package. "
                            f"Use one of {get_provider_packages()}")
        del sys.argv[1]
        print(f"Building backport package: {provider_package}")
        dependencies = PROVIDERS_REQUIREMENTS[provider_package]
        do_setup_package_providers(provider_package_id=provider_package,
                                   package_dependencies=dependencies,
                                   extras=find_package_extras(provider_package))
