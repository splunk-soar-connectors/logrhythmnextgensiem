# LogRhythm NextGen SIEM

Publisher: Splunk Community \
Connector Version: 1.0.3 \
Product Vendor: LogRhythm \
Product Name: LogRhythm NextGen SIEM \
Minimum Product Version: 5.0.0

This app supports ingestion and several investigative actions on LogRhythm NextGen SIEM

### Configuration variables

This table lists the configuration variables required to operate LogRhythm NextGen SIEM. These variables are specified when configuring a LogRhythm NextGen SIEM asset in Splunk SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**base_url** | required | string | Base URL (e.g. https://mylogrhythm.net:8501) |
**api_key** | required | password | API Token |
**verify_server_cert** | optional | boolean | Verify server certificate |
**poll_now_ingestion_span** | required | numeric | Poll last n days for 'Poll Now' |
**first_scheduled_ingestion_span** | required | numeric | Poll last n days for first scheduled polling |
**max_alarms** | required | numeric | Maximum number of alarms to ingest for scheduled polling |

### Supported Actions

[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied configuration \
[on poll](#action-on-poll) - Ingest alarms from LogRhythm \
[update alarm](#action-update-alarm) - Update an alarm \
[get events](#action-get-events) - Get an alarm's events \
[get summary](#action-get-summary) - Get an alarm's summary

## action: 'test connectivity'

Validate the asset configuration for connectivity using supplied configuration

Type: **test** \
Read only: **True**

#### Action Parameters

No parameters are required for this action

#### Action Output

No Output

## action: 'on poll'

Ingest alarms from LogRhythm

Type: **ingest** \
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**container_id** | optional | Parameter ignored in this app | numeric | |
**start_time** | optional | Parameter ignored in this app | numeric | |
**end_time** | optional | Parameter ignored in this app | numeric | |
**container_count** | optional | Maximum number of container records to query for | numeric | |
**artifact_count** | optional | Parameter ignored in this app | numeric | |

#### Action Output

No Output

## action: 'update alarm'

Update an alarm

Type: **generic** \
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** | required | Alarm ID | string | `logrhythm alarm id` |
**status** | optional | New status for the alarm | string | |
**rbp** | optional | New RBP for the alarm | numeric | |
**comment** | optional | New comment to add to alarm | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.comment | string | | |
action_result.parameter.id | string | `logrhythm alarm id` | |
action_result.parameter.rbp | numeric | | |
action_result.parameter.status | string | | |
action_result.data.\*.responseMessage | string | | |
action_result.status | string | | success failed |
action_result.summary | numeric | | |
action_result.message | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'get events'

Get an alarm's events

Type: **investigate** \
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** | required | Alarm ID | string | `logrhythm alarm id` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.id | string | `logrhythm alarm id` | 194 195 |
action_result.data.\*.account | string | | |
action_result.data.\*.amount | numeric | | |
action_result.data.\*.bytesIn | numeric | | 0 |
action_result.data.\*.bytesOut | numeric | | 0 |
action_result.data.\*.classificationId | numeric | | 3200 |
action_result.data.\*.classificationName | string | | Error |
action_result.data.\*.classificationTypeName | string | | |
action_result.data.\*.command | string | | |
action_result.data.\*.commonEventId | numeric | | -1100403 -1100001 |
action_result.data.\*.commonEventName | string | | LogRhythm AI Comm Manager Heartbeat Missed LogRhythm Mediator Heartbeat Missed |
action_result.data.\*.count | numeric | | 1 |
action_result.data.\*.directionId | numeric | | |
action_result.data.\*.directionName | string | | Local |
action_result.data.\*.domain | string | `domain` | |
action_result.data.\*.duration | numeric | | |
action_result.data.\*.entityId | numeric | | 0 |
action_result.data.\*.entityName | string | | |
action_result.data.\*.group | string | | |
action_result.data.\*.impactedEntityId | numeric | | 1 |
action_result.data.\*.impactedEntityName | string | | Primary Site |
action_result.data.\*.impactedHostId | numeric | | 1 |
action_result.data.\*.impactedHostName | string | `host name` | logr-siem-01 |
action_result.data.\*.impactedIP | string | | |
action_result.data.\*.impactedInterface | string | | |
action_result.data.\*.impactedLocation.locationId | numeric | | -1 |
action_result.data.\*.impactedLocation.name | string | | |
action_result.data.\*.impactedMAC | string | | |
action_result.data.\*.impactedNATIP | string | | |
action_result.data.\*.impactedNATPort | numeric | `port` | -1 |
action_result.data.\*.impactedName | string | | logr-siem-01 |
action_result.data.\*.impactedNetwork.name | string | | |
action_result.data.\*.impactedNetwork.networkId | numeric | | -1 |
action_result.data.\*.impactedPort | numeric | `port` | -1 |
action_result.data.\*.impactedZone | string | | Unknown Internal |
action_result.data.\*.itemsPacketsIn | string | | |
action_result.data.\*.itemsPacketsOut | string | | |
action_result.data.\*.logDate | string | | 2017-06-29T03:50:11.000000 2017-08-04T18:27:38.000163 |
action_result.data.\*.logMessage | string | | |
action_result.data.\*.logSourceHostId | numeric | | -1000000 |
action_result.data.\*.logSourceHostName | string | `host name` | logr-siem-01 * |
action_result.data.\*.logSourceName | string | | LogRhythm |
action_result.data.\*.logSourceTypeName | string | | LogRhythm Diagnostics |
action_result.data.\*.login | string | | |
action_result.data.\*.messageId | numeric | | 0 |
action_result.data.\*.mpeRuleId | numeric | | -1 |
action_result.data.\*.mpeRuleName | string | | |
action_result.data.\*.normalDateMax | string | | 2017-06-29T03:50:11.000000 2017-08-04T18:27:38.000163 |
action_result.data.\*.objectName | string | | |
action_result.data.\*.objectType | string | | |
action_result.data.\*.originEntityId | numeric | | 1 |
action_result.data.\*.originEntityName | string | | Primary Site |
action_result.data.\*.originHostId | numeric | | 1 |
action_result.data.\*.originHostName | string | `host name` | logr-siem-01 |
action_result.data.\*.originIP | string | | |
action_result.data.\*.originInterface | string | | |
action_result.data.\*.originLocation.locationId | numeric | | -1 |
action_result.data.\*.originLocation.name | string | | |
action_result.data.\*.originMAC | string | | |
action_result.data.\*.originNATIP | string | | |
action_result.data.\*.originNATPort | numeric | `port` | -1 |
action_result.data.\*.originName | string | | logr-siem-01 |
action_result.data.\*.originNetwork.name | string | | |
action_result.data.\*.originNetwork.networkId | numeric | | -1 |
action_result.data.\*.originPort | numeric | | -1 |
action_result.data.\*.originZone | string | | Unknown Internal |
action_result.data.\*.priority | numeric | | 67 |
action_result.data.\*.process | string | | |
action_result.data.\*.processId | numeric | `pid` | -1 |
action_result.data.\*.protocolId | numeric | | -1 |
action_result.data.\*.protocolName | string | | |
action_result.data.\*.quantity | numeric | | |
action_result.data.\*.rate | numeric | | |
action_result.data.\*.recipient | string | | |
action_result.data.\*.sender | string | | |
action_result.data.\*.serviceId | numeric | | 0 |
action_result.data.\*.serviceName | string | | |
action_result.data.\*.session | string | | |
action_result.data.\*.severity | string | | |
action_result.data.\*.size | numeric | | |
action_result.data.\*.subject | string | | |
action_result.data.\*.url | string | `url` | |
action_result.data.\*.vendorMsgId | string | | |
action_result.data.\*.version | string | | |
action_result.status | string | | success failed |
action_result.summary.num_events | numeric | | |
action_result.message | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'get summary'

Get an alarm's summary

Type: **investigate** \
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** | required | Alarm ID | string | `logrhythm alarm id` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.id | string | `logrhythm alarm id` | 194 195 |
action_result.data.\*.additionalDetails | string | | |
action_result.data.\*.alarmEventSummary.\*.commonEventId | numeric | | -1100403 -1100001 |
action_result.data.\*.alarmEventSummary.\*.commonEventName | string | | LogRhythm AI Comm Manager Heartbeat Missed LogRhythm Mediator Heartbeat Missed |
action_result.data.\*.alarmEventSummary.\*.impactedEntityName | string | | Primary Site |
action_result.data.\*.alarmEventSummary.\*.impactedHostId | string | | |
action_result.data.\*.alarmEventSummary.\*.impactedUser | string | | |
action_result.data.\*.alarmEventSummary.\*.impactedUserIdentityId | numeric | | |
action_result.data.\*.alarmEventSummary.\*.impactedUserIdentityName | string | | |
action_result.data.\*.alarmEventSummary.\*.msgClassId | numeric | | |
action_result.data.\*.alarmEventSummary.\*.msgClassName | string | | |
action_result.data.\*.alarmEventSummary.\*.originEntityName | string | | Primary Site |
action_result.data.\*.alarmEventSummary.\*.originHostId | numeric | | 1 |
action_result.data.\*.alarmEventSummary.\*.originUser | string | | |
action_result.data.\*.alarmEventSummary.\*.originUserIdentifyId | numeric | | |
action_result.data.\*.alarmEventSummary.\*.originUserIdentifyName | string | | |
action_result.data.\*.alarmRuleGroup | string | | |
action_result.data.\*.alarmRuleId | numeric | | |
action_result.data.\*.briefDescription | string | | |
action_result.data.\*.dateInserted | string | | |
action_result.data.\*.rbpAvg | numeric | | 50 |
action_result.data.\*.rbpMax | numeric | | 0 100 |
action_result.status | string | | success failed |
action_result.summary.tot_events_summary | numeric | | |
action_result.message | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

______________________________________________________________________

Auto-generated Splunk SOAR Connector documentation.

Copyright 2025 Splunk Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
