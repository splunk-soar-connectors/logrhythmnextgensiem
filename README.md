[comment]: # "Auto-generated SOAR connector documentation"
# LogRhythm NextGen SIEM

Publisher: Splunk Community  
Connector Version: 1\.0\.3  
Product Vendor: LogRhythm  
Product Name: LogRhythm NextGen SIEM  
Product Version Supported (regex): "\.\*"  
Minimum Product Version: 5\.0\.0  

This app supports ingestion and several investigative actions on LogRhythm NextGen SIEM

[comment]: # " File: readme.md"
[comment]: # "  Copyright (c) 2021 Splunk Inc."
[comment]: # "  Licensed under the Apache License, Version 2.0 (the 'License');"
[comment]: # "  you may not use this file except in compliance with the License."
[comment]: # "  You may obtain a copy of the License at"
[comment]: # ""
[comment]: # "      http://www.apache.org/licenses/LICENSE-2.0"
[comment]: # "  Unless required by applicable law or agreed to in writing, software distributed under"
[comment]: # "  the License is distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,"
[comment]: # "  either express or implied. See the License for the specific language governing permissions"
[comment]: # "  and limitations under the License."
[comment]: # ""
Important notes

-   This app differs from its parent **LogRhythm SIEM** by leveraging LogRhythm RESTful API, in
    compliance with future releases of LogRhythm NextGen SIEM
-   This app is compatible with Phantom **5.0.0+**

## Port Information

The app uses HTTP/ HTTPS protocol for communicating with the LogRhythm NextGen SIEM. Below are the
default ports used by the Splunk SOAR Connector.

| SERVICE NAME | TRANSPORT PROTOCOL | PORT |
|--------------|--------------------|------|
| http         | tcp                | 80   |
| https        | tcp                | 443  |


### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a LogRhythm NextGen SIEM asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**base\_url** |  required  | string | Base URL \(e\.g\. https\://mylogrhythm\.net\:8501\)
**api\_key** |  required  | password | API Token
**verify\_server\_cert** |  optional  | boolean | Verify server certificate
**poll\_now\_ingestion\_span** |  required  | numeric | Poll last n days for 'Poll Now'
**first\_scheduled\_ingestion\_span** |  required  | numeric | Poll last n days for first scheduled polling
**max\_alarms** |  required  | numeric | Maximum number of alarms to ingest for scheduled polling

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied configuration  
[on poll](#action-on-poll) - Ingest alarms from LogRhythm  
[update alarm](#action-update-alarm) - Update an alarm  
[get events](#action-get-events) - Get an alarm's events  
[get summary](#action-get-summary) - Get an alarm's summary  

## action: 'test connectivity'
Validate the asset configuration for connectivity using supplied configuration

Type: **test**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'on poll'
Ingest alarms from LogRhythm

Type: **ingest**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**container\_id** |  optional  | Parameter ignored in this app | numeric | 
**start\_time** |  optional  | Parameter ignored in this app | numeric | 
**end\_time** |  optional  | Parameter ignored in this app | numeric | 
**container\_count** |  optional  | Maximum number of container records to query for | numeric | 
**artifact\_count** |  optional  | Parameter ignored in this app | numeric | 

#### Action Output
No Output  

## action: 'update alarm'
Update an alarm

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** |  required  | Alarm ID | string |  `logrhythm alarm id` 
**status** |  optional  | New status for the alarm | string | 
**rbp** |  optional  | New RBP for the alarm | numeric | 
**comment** |  optional  | New comment to add to alarm | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.comment | string | 
action\_result\.parameter\.id | string |  `logrhythm alarm id` 
action\_result\.parameter\.rbp | numeric | 
action\_result\.parameter\.status | string | 
action\_result\.data\.\*\.responseMessage | string | 
action\_result\.status | string | 
action\_result\.summary | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'get events'
Get an alarm's events

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** |  required  | Alarm ID | string |  `logrhythm alarm id` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.id | string |  `logrhythm alarm id` 
action\_result\.data\.\*\.account | string | 
action\_result\.data\.\*\.amount | numeric | 
action\_result\.data\.\*\.bytesIn | numeric | 
action\_result\.data\.\*\.bytesOut | numeric | 
action\_result\.data\.\*\.classificationId | numeric | 
action\_result\.data\.\*\.classificationName | string | 
action\_result\.data\.\*\.classificationTypeName | string | 
action\_result\.data\.\*\.command | string | 
action\_result\.data\.\*\.commonEventId | numeric | 
action\_result\.data\.\*\.commonEventName | string | 
action\_result\.data\.\*\.count | numeric | 
action\_result\.data\.\*\.directionId | numeric | 
action\_result\.data\.\*\.directionName | string | 
action\_result\.data\.\*\.domain | string |  `domain` 
action\_result\.data\.\*\.duration | numeric | 
action\_result\.data\.\*\.entityId | numeric | 
action\_result\.data\.\*\.entityName | string | 
action\_result\.data\.\*\.group | string | 
action\_result\.data\.\*\.impactedEntityId | numeric | 
action\_result\.data\.\*\.impactedEntityName | string | 
action\_result\.data\.\*\.impactedHostId | numeric | 
action\_result\.data\.\*\.impactedHostName | string |  `host name` 
action\_result\.data\.\*\.impactedIP | string | 
action\_result\.data\.\*\.impactedInterface | string | 
action\_result\.data\.\*\.impactedLocation\.locationId | numeric | 
action\_result\.data\.\*\.impactedLocation\.name | string | 
action\_result\.data\.\*\.impactedMAC | string | 
action\_result\.data\.\*\.impactedNATIP | string | 
action\_result\.data\.\*\.impactedNATPort | numeric |  `port` 
action\_result\.data\.\*\.impactedName | string | 
action\_result\.data\.\*\.impactedNetwork\.name | string | 
action\_result\.data\.\*\.impactedNetwork\.networkId | numeric | 
action\_result\.data\.\*\.impactedPort | numeric |  `port` 
action\_result\.data\.\*\.impactedZone | string | 
action\_result\.data\.\*\.itemsPacketsIn | string | 
action\_result\.data\.\*\.itemsPacketsOut | string | 
action\_result\.data\.\*\.logDate | string | 
action\_result\.data\.\*\.logMessage | string | 
action\_result\.data\.\*\.logSourceHostId | numeric | 
action\_result\.data\.\*\.logSourceHostName | string |  `host name` 
action\_result\.data\.\*\.logSourceName | string | 
action\_result\.data\.\*\.logSourceTypeName | string | 
action\_result\.data\.\*\.login | string | 
action\_result\.data\.\*\.messageId | numeric | 
action\_result\.data\.\*\.mpeRuleId | numeric | 
action\_result\.data\.\*\.mpeRuleName | string | 
action\_result\.data\.\*\.normalDateMax | string | 
action\_result\.data\.\*\.objectName | string | 
action\_result\.data\.\*\.objectType | string | 
action\_result\.data\.\*\.originEntityId | numeric | 
action\_result\.data\.\*\.originEntityName | string | 
action\_result\.data\.\*\.originHostId | numeric | 
action\_result\.data\.\*\.originHostName | string |  `host name` 
action\_result\.data\.\*\.originIP | string | 
action\_result\.data\.\*\.originInterface | string | 
action\_result\.data\.\*\.originLocation\.locationId | numeric | 
action\_result\.data\.\*\.originLocation\.name | string | 
action\_result\.data\.\*\.originMAC | string | 
action\_result\.data\.\*\.originNATIP | string | 
action\_result\.data\.\*\.originNATPort | numeric |  `port` 
action\_result\.data\.\*\.originName | string | 
action\_result\.data\.\*\.originNetwork\.name | string | 
action\_result\.data\.\*\.originNetwork\.networkId | numeric | 
action\_result\.data\.\*\.originPort | numeric | 
action\_result\.data\.\*\.originZone | string | 
action\_result\.data\.\*\.priority | numeric | 
action\_result\.data\.\*\.process | string | 
action\_result\.data\.\*\.processId | numeric |  `pid` 
action\_result\.data\.\*\.protocolId | numeric | 
action\_result\.data\.\*\.protocolName | string | 
action\_result\.data\.\*\.quantity | numeric | 
action\_result\.data\.\*\.rate | numeric | 
action\_result\.data\.\*\.recipient | string | 
action\_result\.data\.\*\.sender | string | 
action\_result\.data\.\*\.serviceId | numeric | 
action\_result\.data\.\*\.serviceName | string | 
action\_result\.data\.\*\.session | string | 
action\_result\.data\.\*\.severity | string | 
action\_result\.data\.\*\.size | numeric | 
action\_result\.data\.\*\.subject | string | 
action\_result\.data\.\*\.url | string |  `url` 
action\_result\.data\.\*\.vendorMsgId | string | 
action\_result\.data\.\*\.version | string | 
action\_result\.status | string | 
action\_result\.summary\.num\_events | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'get summary'
Get an alarm's summary

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** |  required  | Alarm ID | string |  `logrhythm alarm id` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.id | string |  `logrhythm alarm id` 
action\_result\.data\.\*\.additionalDetails | string | 
action\_result\.data\.\*\.alarmEventSummary\.\*\.commonEventId | numeric | 
action\_result\.data\.\*\.alarmEventSummary\.\*\.commonEventName | string | 
action\_result\.data\.\*\.alarmEventSummary\.\*\.impactedEntityName | string | 
action\_result\.data\.\*\.alarmEventSummary\.\*\.impactedHostId | string | 
action\_result\.data\.\*\.alarmEventSummary\.\*\.impactedUser | string | 
action\_result\.data\.\*\.alarmEventSummary\.\*\.impactedUserIdentityId | numeric | 
action\_result\.data\.\*\.alarmEventSummary\.\*\.impactedUserIdentityName | string | 
action\_result\.data\.\*\.alarmEventSummary\.\*\.msgClassId | numeric | 
action\_result\.data\.\*\.alarmEventSummary\.\*\.msgClassName | string | 
action\_result\.data\.\*\.alarmEventSummary\.\*\.originEntityName | string | 
action\_result\.data\.\*\.alarmEventSummary\.\*\.originHostId | numeric | 
action\_result\.data\.\*\.alarmEventSummary\.\*\.originUser | string | 
action\_result\.data\.\*\.alarmEventSummary\.\*\.originUserIdentifyId | numeric | 
action\_result\.data\.\*\.alarmEventSummary\.\*\.originUserIdentifyName | string | 
action\_result\.data\.\*\.alarmRuleGroup | string | 
action\_result\.data\.\*\.alarmRuleId | numeric | 
action\_result\.data\.\*\.briefDescription | string | 
action\_result\.data\.\*\.dateInserted | string | 
action\_result\.data\.\*\.rbpAvg | numeric | 
action\_result\.data\.\*\.rbpMax | numeric | 
action\_result\.status | string | 
action\_result\.summary\.tot\_events\_summary | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 