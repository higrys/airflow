<!--
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


# Package apache-airflow-backport-providers-dingding

**Table of contents**

- [Backport package](#backport-package)
- [Installation](#installation)
- [Compatibility](#compatibility)
- [Cross provider package dependencies](#cross-provider-package-dependencies)
- [Provider class summary](#provider-class-summary)
    - [Moved operators](#moved-operators)
    - [Moved hooks](#moved-hooks)
- [Releases](#releases)
    - [Release 2020.05.10](#release-2020.05.10)

## Backport package

This is a backport providers package for `dingding` provider. All classes for this provider package
are in `airflow.providers.dingding` python package.

## Installation

You can install this package on top of an existing airflow 1.10.* installation via
`pip install apache-airflow-backport-providers-dingding`

## Compatibility

For full compatibility and test status of the backport packages check
[Airflow Backport Package Compatibility](https://cwiki.apache.org/confluence/display/AIRFLOW/Backported+providers+packages+for+Airflow+1.10.*+series)

## Cross provider package dependencies

Those are dependencies that might be needed in order to use all the features of the package.
You need to install the specified backport providers package in order to use them.

| Dependent package                                                                                              |
|:---------------------------------------------------------------------------------------------------------------|
| [apache-airflow-backport-providers-http](https://github.com/apache/airflow/tree/master/airflow/providers/http) |

# Provider class summary

All classes in Airflow 2.0 are in `airflow.providers.dingding` package.


## Operators




### Moved operators

| Airflow 2.0 operators: `airflow.providers.dingding` package                                                                           | Airflow 1.10.* previous location (usually `airflow.contrib`)                                                                                       |
|:--------------------------------------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------|
| [operators.dingding.DingdingOperator](https://github.com/apache/airflow/blob/master/airflow/providers/dingding/operators/dingding.py) | [operators.dingding_operator.DingdingOperator](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/operators/dingding_operator.py) |





## Hooks



### Moved hooks

| Airflow 2.0 hooks: `airflow.providers.dingding` package                                                                   | Airflow 1.10.* previous location (usually `airflow.contrib`)                                                                   |
|:--------------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------|
| [hooks.dingding.DingdingHook](https://github.com/apache/airflow/blob/master/airflow/providers/dingding/hooks/dingding.py) | [hooks.dingding_hook.DingdingHook](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/hooks/dingding_hook.py) |




## Releases

### Release 2020.05.10

| Commit                                                                                         | Subject                                                                                                                                                            |
|:-----------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [4bde99f13](https://github.com/apache/airflow/commit/4bde99f1323d72f6c84c1548079d5e98fc0a2a9a) | Make airflow/providers pylint compatible (#7802)                                                                                                                   |
| [3320e432a](https://github.com/apache/airflow/commit/3320e432a129476dbc1c55be3b3faa3326a635bc) | [AIRFLOW-6817] Lazy-load `airflow.DAG` to keep user-facing API untouched (#7517)                                                                                   |
| [4d03e33c1](https://github.com/apache/airflow/commit/4d03e33c115018e30fa413c42b16212481ad25cc) | [AIRFLOW-6817] remove imports from `airflow/__init__.py`, replaced implicit imports with explicit imports, added entry to `UPDATING.MD` - squashed/rebased (#7456) |
| [97a429f9d](https://github.com/apache/airflow/commit/97a429f9d0cf740c5698060ad55f11e93cb57b55) | [AIRFLOW-6714] Remove magic comments about UTF-8 (#7338)                                                                                                           |
| [83c037873](https://github.com/apache/airflow/commit/83c037873ff694eed67ba8b30f2d9c88b2c7c6f2) | [AIRFLOW-6674] Move example_dags in accordance with AIP-21 (#7287)                                                                                                 |
| [ceea293c1](https://github.com/apache/airflow/commit/ceea293c1652240e7e856c201e4341a87ef97a0f) | [AIRFLOW-6656] Fix AIP-21 moving (#7272)                                                                                                                           |
| [9a04013b0](https://github.com/apache/airflow/commit/9a04013b0e40b0d744ff4ac9f008491806d60df2) | [AIRFLOW-6646][AIP-21] Move protocols classes to providers package (#7268)                                                                                         |
| [c42a375e7](https://github.com/apache/airflow/commit/c42a375e799e5adb3f9536616372dc90ff47e6c8) | [AIRFLOW-6644][AIP-21] Move service classes to providers package (#7265)                                                                                           |
