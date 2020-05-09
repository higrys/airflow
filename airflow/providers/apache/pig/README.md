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


# Package apache-airflow-backport-providers-apache-pig

**Table of contents**

- [Backport package](#backport-package)
- [Installation](#installation)
- [Compatibility](#compatibility)
- [Provider class summary](#provider-class-summary)
    - [Moved operators](#moved-operators)
    - [Moved hooks](#moved-hooks)
- [Releases](#releases)
    - [Release 2020.05.10](#release-2020.05.10)

## Backport package

This is a backport providers package for `apache.pig` provider. All classes for this provider package
are in `airflow.providers.apache.pig` python package.

## Installation

You can install this package on top of an existing airflow 1.10.* installation via
`pip install apache-airflow-backport-providers-apache-pig`

## Compatibility

For full compatibility and test status of the backport packages check
[Airflow Backport Package Compatibility](https://cwiki.apache.org/confluence/display/AIRFLOW/Backported+providers+packages+for+Airflow+1.10.*+series)

# Provider class summary

All classes in Airflow 2.0 are in `airflow.providers.apache.pig` package.


## Operators




### Moved operators

| Airflow 2.0 operators: `airflow.providers.apache.pig` package                                                            | Airflow 1.10.* previous location (usually `airflow.contrib`)                                                                        |
|:-------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------|
| [operators.pig.PigOperator](https://github.com/apache/airflow/blob/master/airflow/providers/apache/pig/operators/pig.py) | [airflow.operators.pig_operator.PigOperator](https://github.com/apache/airflow/blob/v1-10-stable/airflow/operators/pig_operator.py) |





## Hooks



### Moved hooks

| Airflow 2.0 hooks: `airflow.providers.apache.pig` package                                                       | Airflow 1.10.* previous location (usually `airflow.contrib`)                                                       |
|:----------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------|
| [hooks.pig.PigCliHook](https://github.com/apache/airflow/blob/master/airflow/providers/apache/pig/hooks/pig.py) | [airflow.hooks.pig_hook.PigCliHook](https://github.com/apache/airflow/blob/v1-10-stable/airflow/hooks/pig_hook.py) |




## Releases

### Release 2020.05.10

| Commit                                                                                         | Subject                                                                                  |
|:-----------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------|
| [4bde99f13](https://github.com/apache/airflow/commit/4bde99f1323d72f6c84c1548079d5e98fc0a2a9a) | Make airflow/providers pylint compatible (#7802)                                         |
| [7e6372a68](https://github.com/apache/airflow/commit/7e6372a681a2a543f4710b083219aeb53b074388) | Add call to Super call in apache providers (#7820)                                       |
| [3320e432a](https://github.com/apache/airflow/commit/3320e432a129476dbc1c55be3b3faa3326a635bc) | [AIRFLOW-6817] Lazy-load `airflow.DAG` to keep user-facing API untouched (#7517)         |
| [9cbd7de6d](https://github.com/apache/airflow/commit/9cbd7de6d115795aba8bfb8addb060bfdfbdf87b) | [AIRFLOW-6792] Remove _operator/_hook/_sensor in providers package and add tests (#7412) |
| [97a429f9d](https://github.com/apache/airflow/commit/97a429f9d0cf740c5698060ad55f11e93cb57b55) | [AIRFLOW-6714] Remove magic comments about UTF-8 (#7338)                                 |
| [83c037873](https://github.com/apache/airflow/commit/83c037873ff694eed67ba8b30f2d9c88b2c7c6f2) | [AIRFLOW-6674] Move example_dags in accordance with AIP-21 (#7287)                       |
| [0481b9a95](https://github.com/apache/airflow/commit/0481b9a95786a62de4776a735ae80e746583ef2b) | [AIRFLOW-6539][AIP-21] Move Apache classes to providers.apache package (#7142)           |
