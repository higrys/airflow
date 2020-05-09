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


# Package apache-airflow-backport-providers-http

**Table of contents**

- [Backport package](#backport-package)
- [Installation](#installation)
- [Compatibility](#compatibility)
- [Provider class summary](#provider-class-summary)
    - [Moved operators](#moved-operators)
    - [Moved sensors](#moved-sensors)
    - [Moved hooks](#moved-hooks)
- [Releases](#releases)
    - [Release 2020.05.10](#release-2020.05.10)

## Backport package

This is a backport providers package for `http` provider. All classes for this provider package
are in `airflow.providers.http` python package.

## Installation

You can install this package on top of an existing airflow 1.10.* installation via
`pip install apache-airflow-backport-providers-http`

## Compatibility

For full compatibility and test status of the backport packages check
[Airflow Backport Package Compatibility](https://cwiki.apache.org/confluence/display/AIRFLOW/Backported+providers+packages+for+Airflow+1.10.*+series)

# Provider class summary

All classes in Airflow 2.0 are in `airflow.providers.http` package.


## Operators




### Moved operators

| Airflow 2.0 operators: `airflow.providers.http` package                                                                     | Airflow 1.10.* previous location (usually `airflow.contrib`)                                                                                 |
|:----------------------------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------|
| [operators.http.SimpleHttpOperator](https://github.com/apache/airflow/blob/master/airflow/providers/http/operators/http.py) | [airflow.operators.http_operator.SimpleHttpOperator](https://github.com/apache/airflow/blob/v1-10-stable/airflow/operators/http_operator.py) |




## Sensors



### Moved sensors

| Airflow 2.0 sensors: `airflow.providers.http` package                                                           | Airflow 1.10.* previous location (usually `airflow.contrib`)                                                                 |
|:----------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------|
| [sensors.http.HttpSensor](https://github.com/apache/airflow/blob/master/airflow/providers/http/sensors/http.py) | [airflow.sensors.http_sensor.HttpSensor](https://github.com/apache/airflow/blob/v1-10-stable/airflow/sensors/http_sensor.py) |



## Hooks



### Moved hooks

| Airflow 2.0 hooks: `airflow.providers.http` package                                                       | Airflow 1.10.* previous location (usually `airflow.contrib`)                                                       |
|:----------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------|
| [hooks.http.HttpHook](https://github.com/apache/airflow/blob/master/airflow/providers/http/hooks/http.py) | [airflow.hooks.http_hook.HttpHook](https://github.com/apache/airflow/blob/v1-10-stable/airflow/hooks/http_hook.py) |




## Releases

### Release 2020.05.10

| Commit                                                                                         | Subject                                                                                                                                                            |
|:-----------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [249e80b96](https://github.com/apache/airflow/commit/249e80b960ab3453763903493bbb77651be9073b) | Add http system test (#8591)                                                                                                                                       |
| [ddd005e3b](https://github.com/apache/airflow/commit/ddd005e3b97e82ce715dc6604ff60ed5768de6ea) | [AIRFLOW-5156] Fixed doc strigns for HttpHook (#8434)                                                                                                              |
| [d61a476da](https://github.com/apache/airflow/commit/d61a476da3a649bf2c1d347b9cb3abc62eae3ce9) | [AIRFLOW-5156] Added auth type to HttpHook (#8429)                                                                                                                 |
| [4bde99f13](https://github.com/apache/airflow/commit/4bde99f1323d72f6c84c1548079d5e98fc0a2a9a) | Make airflow/providers pylint compatible (#7802)                                                                                                                   |
| [be2b2baa7](https://github.com/apache/airflow/commit/be2b2baa7c5f53c2d73646e4623cdb6731551b70) | Add missing call to Super class in &#39;http&#39;, &#39;grpc&#39; &amp; &#39;slack&#39; providers (#7826)                                                                                      |
| [3320e432a](https://github.com/apache/airflow/commit/3320e432a129476dbc1c55be3b3faa3326a635bc) | [AIRFLOW-6817] Lazy-load `airflow.DAG` to keep user-facing API untouched (#7517)                                                                                   |
| [4d03e33c1](https://github.com/apache/airflow/commit/4d03e33c115018e30fa413c42b16212481ad25cc) | [AIRFLOW-6817] remove imports from `airflow/__init__.py`, replaced implicit imports with explicit imports, added entry to `UPDATING.MD` - squashed/rebased (#7456) |
| [9cbd7de6d](https://github.com/apache/airflow/commit/9cbd7de6d115795aba8bfb8addb060bfdfbdf87b) | [AIRFLOW-6792] Remove _operator/_hook/_sensor in providers package and add tests (#7412)                                                                           |
| [f3ad5cf61](https://github.com/apache/airflow/commit/f3ad5cf6185b9d406d0fb0a4ecc0b5536f79217a) | [AIRFLOW-4681] Make sensors module pylint compatible (#7309)                                                                                                       |
| [97a429f9d](https://github.com/apache/airflow/commit/97a429f9d0cf740c5698060ad55f11e93cb57b55) | [AIRFLOW-6714] Remove magic comments about UTF-8 (#7338)                                                                                                           |
| [83c037873](https://github.com/apache/airflow/commit/83c037873ff694eed67ba8b30f2d9c88b2c7c6f2) | [AIRFLOW-6674] Move example_dags in accordance with AIP-21 (#7287)                                                                                                 |
| [9a04013b0](https://github.com/apache/airflow/commit/9a04013b0e40b0d744ff4ac9f008491806d60df2) | [AIRFLOW-6646][AIP-21] Move protocols classes to providers package (#7268)                                                                                         |
