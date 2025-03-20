# File: logrhythmnextgensiem_consts.py
#
# Copyright (c) 2021-2025 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.
#
#
LOGRHYTHM_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"

# Endpoints
LOGRHYTHM_ALARMS_API = "lr-alarm-api/alarms"
LOGRHYTHM_ALARM_ENDPOINT = LOGRHYTHM_ALARMS_API + "/{alarmid}"
LOGRHYTHM_ALARMEVENTS_ENDPOINT = LOGRHYTHM_ALARMS_API + "/{alarmid}/events"
LOGRHYTHM_ALARMSUMMARY_ENDPOINT = LOGRHYTHM_ALARMS_API + "/{alarmid}/summary"

# Messages
LOGRHYTHM_OK = "Connected successfully to endpoint. Checking returned reply"
LOGRHYTHM_NOALARMS = "No alarms to ingest"
LOGRHYTHM_PARAMS_NOTFOUND = "Configuration parameter(s) {params} not found"
LOGRHYTHM_STATE_FILE_CORRUPT_ERR = "Error occurred while loading the state file due to its unexpected format.\
     Resetting the state file with the default format. Please try again."

# constants relating to "get_error_msg_from_exception"
LOGRHYTHM_ERR_MSG_UNAVAILABLE = "Error message unavailable. Please check the asset configuration and|or action parameters"

# Constants relating to 'validate_integer'
VALID_INT_MSG = "Please provide a valid integer value in the '{param}' parameter"
NON_NEG_INT_MSG = "Please provide a valid non-negative integer value in the '{param}' parameter"
