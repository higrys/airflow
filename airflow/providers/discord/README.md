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


# Package apache-airflow-backport-providers-discord

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

This is a backport providers package for `discord` provider. All classes for this provider package
are in `airflow.providers.discord` python package.

## Installation

You can install this package on top of an existing airflow 1.10.* installation via
`pip install apache-airflow-backport-providers-discord`

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

All classes in Airflow 2.0 are in `airflow.providers.discord` package.


## Operators




### Moved operators

| Airflow 2.0 operators: `airflow.providers.discord` package                                                                                               | Airflow 1.10.* previous location (usually `airflow.contrib`)                                                                                                           |
|:---------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [operators.discord_webhook.DiscordWebhookOperator](https://github.com/apache/airflow/blob/master/airflow/providers/discord/operators/discord_webhook.py) | [operators.discord_webhook_operator.DiscordWebhookOperator](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/operators/discord_webhook_operator.py) |





## Hooks



### Moved hooks

| Airflow 2.0 hooks: `airflow.providers.discord` package                                                                                       | Airflow 1.10.* previous location (usually `airflow.contrib`)                                                                                       |
|:---------------------------------------------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------|
| [hooks.discord_webhook.DiscordWebhookHook](https://github.com/apache/airflow/blob/master/airflow/providers/discord/hooks/discord_webhook.py) | [hooks.discord_webhook_hook.DiscordWebhookHook](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/hooks/discord_webhook_hook.py) |




## Releases

### Release 2020.05.10

| Commit                                                                                         | Subject                                                                    |
|:-----------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------|
| [97a429f9d](https://github.com/apache/airflow/commit/97a429f9d0cf740c5698060ad55f11e93cb57b55) | [AIRFLOW-6714] Remove magic comments about UTF-8 (#7338)                   |
| [ceea293c1](https://github.com/apache/airflow/commit/ceea293c1652240e7e856c201e4341a87ef97a0f) | [AIRFLOW-6656] Fix AIP-21 moving (#7272)                                   |
| [9a04013b0](https://github.com/apache/airflow/commit/9a04013b0e40b0d744ff4ac9f008491806d60df2) | [AIRFLOW-6646][AIP-21] Move protocols classes to providers package (#7268) |
| [c42a375e7](https://github.com/apache/airflow/commit/c42a375e799e5adb3f9536616372dc90ff47e6c8) | [AIRFLOW-6644][AIP-21] Move service classes to providers package (#7265)   |
