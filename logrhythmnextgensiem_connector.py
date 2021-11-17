# File: logrhythmnextgensiem_connector.py
#
# Copyright (c) 2021 Splunk Inc.
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
# Python 3 Compatibility imports
from __future__ import print_function, unicode_literals

# Phantom App imports
import phantom.app as phantom
from phantom.action_result import ActionResult
from phantom.base_connector import BaseConnector

import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

from logrhythmnextgensiem_consts import *


class RetVal(tuple):

    def __new__(cls, val1, val2=None):
        return tuple.__new__(RetVal, (val1, val2))


class LogrhythmNextgenSiemConnector(BaseConnector):

    def __init__(self):

        # Call the BaseConnectors init first
        super(LogrhythmNextgenSiemConnector, self).__init__()

        self._state = None

        # Variable to hold a base_url in case the app makes REST calls
        # Do note that the app json defines the asset config, so please
        # modify this as you deem fit.
        self._base_url = None

    def _process_empty_response(self, response, action_result):
        if response.status_code == 200:
            return RetVal(phantom.APP_SUCCESS, {})

        return RetVal(
            action_result.set_status(
                phantom.APP_ERROR, "Empty response and no information in the header"
            ), None
        )

    def _process_html_response(self, response, action_result):
        # An html response, treat it like an error
        status_code = response.status_code

        try:
            soup = BeautifulSoup(response.text, "html.parser")
            error_text = soup.text
            split_lines = error_text.split('\n')
            split_lines = [x.strip() for x in split_lines if x.strip()]
            error_text = '\n'.join(split_lines)
        except:
            error_text = "Cannot parse error details"

        message = "Status Code: {0}. Data from server:\n{1}\n".format(status_code, error_text)

        message = message.replace(u'{', '{{').replace(u'}', '}}')
        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _process_json_response(self, r, action_result):
        # Try a json parse
        try:
            resp_json = r.json()
        except Exception as e:
            return RetVal(
                action_result.set_status(
                    phantom.APP_ERROR, "Unable to parse JSON response. Error: {0}".format(str(e))
                ), None
            )

        # Please specify the status codes here
        if 200 <= r.status_code < 399:
            return RetVal(phantom.APP_SUCCESS, resp_json)

        # Processing the error returned in the json
        status_msg = resp_json.get("statusMessage", "")
        resp_msg = resp_json.get("responseMessage", "")
        message = "Error from server. Status Code: {0} Status Message: {1} Response message: {2}".format(
            r.status_code,
            status_msg,
            resp_msg
        )

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _process_response(self, r, action_result):
        # store the r_text in debug data, it will get dumped in the logs if the action fails
        if hasattr(action_result, 'add_debug_data'):
            action_result.add_debug_data({'r_status_code': r.status_code})
            action_result.add_debug_data({'r_text': r.text})
            action_result.add_debug_data({'r_headers': r.headers})

        # Process each 'Content-Type' of response separately

        # Process a json response
        if 'json' in r.headers.get('Content-Type', ''):
            return self._process_json_response(r, action_result)

        # Process an HTML response, Do this no matter what the api talks.
        # There is a high chance of a PROXY in between phantom and the rest of
        # world, in case of errors, PROXY's return HTML, this function parses
        # the error and adds it to the action_result.
        if 'html' in r.headers.get('Content-Type', ''):
            return self._process_html_response(r, action_result)

        # it's not content-type that is to be parsed, handle an empty response
        if not r.text:
            return self._process_empty_response(r, action_result)

        # everything else is actually an error at this point
        message = "Can't process response from server. Status Code: {0} Data from server: {1}".format(
            r.status_code,
            r.text.replace('{', '{{').replace('}', '}}')
        )

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _make_rest_call(self, endpoint, action_result, method="get", **kwargs):
        # **kwargs can be any additional parameters that requests.request accepts

        config = self.get_config()

        resp_json = None

        try:
            request_func = getattr(requests, method)
        except AttributeError:
            return RetVal(
                action_result.set_status(phantom.APP_ERROR, "Invalid method: {0}".format(method)),
                resp_json
            )

        # Create a URL to connect to
        url = self._base_url + endpoint

        try:
            r = request_func(
                url,
                verify=config.get('verify_server_cert', False),
                headers=self._headers,
                proxies=self._proxies,
                **kwargs
            )
        except Exception as e:
            return RetVal(
                action_result.set_status(
                    phantom.APP_ERROR, "Error Connecting to server. Details: {0}".format(str(e))
                ), resp_json
            )

        return self._process_response(r, action_result)

    def _handle_test_connectivity(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        self.save_progress("Connecting to endpoint")

        # make rest call
        ret_val, response = self._make_rest_call(LOGRHYTHM_ALARMS_API, action_result, params=None)

        if phantom.is_fail(ret_val):
            self.save_progress("Test Connectivity Failed.")
            return action_result.get_status()

        # Return success
        self.save_progress("Test Connectivity Passed")
        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_on_poll(self, param):
        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))
        action_result = self.add_action_result(ActionResult(dict(param)))

        config = self.get_config()

        params = {
            "orderBy": "dateInserted"
        }

        # Use dateInserted to get alarms from a specific date on.
        # Valid dateInserted entries:
        #   4/19/2021 13:00:00
        #   4/19/2021
        #   4/19/2021 3:30
        if self.is_poll_now():
            params["dateInserted"] = (
                datetime.utcnow() - timedelta(days=int(config['poll_now_ingestion_span']))).strftime(LOGRHYTHM_DATETIME_FORMAT)
            # Forcing max alarms returned = max containers specified in dialog
            params["count"] = param[phantom.APP_JSON_CONTAINER_COUNT]
        elif self._state.get('first_run', True):
            self._state['first_run'] = False
            params["count"] = config['max_alarms']
            params["dateInserted"] = (
                    datetime.utcnow() - timedelta(days=int(config['first_scheduled_ingestion_span']))
                ).strftime(LOGRHYTHM_DATETIME_FORMAT)
            self._state['last_time'] = datetime.utcnow().strftime(LOGRHYTHM_DATETIME_FORMAT)
        else:
            params["count"] = config['max_alarms']
            params["dateInserted"] = self._state['last_time']
            self._state['last_time'] = datetime.utcnow().strftime(LOGRHYTHM_DATETIME_FORMAT)

        # make rest call
        ret_val, response = self._make_rest_call(LOGRHYTHM_ALARMS_API, action_result, params=params)

        if phantom.is_fail(ret_val):
            return ret_val

        tot_alarms = response.get('alarmsCount', 0)
        if tot_alarms < 1:
            return action_result.set_status(phantom.APP_SUCCESS, LOGRHYTHM_NOALARMS)

        alarms = response.get('alarmsSearchDetails', [])
        for alarm in alarms:
            alarm_id = alarm['alarmId']

            container = {}
            container['name'] = "{0} on {1} at {2}".format(alarm['alarmRuleName'], alarm['entityName'], alarm['dateInserted'])
            container['description'] = "LogRhythm Alarm ingested by Phantom"
            container['source_data_identifier'] = alarm_id

            ret_val, alarm_resp = self._make_rest_call(
                LOGRHYTHM_ALARMEVENTS_ENDPOINT.format(alarmid=alarm_id), action_result)

            if phantom.is_fail(ret_val):
                return ret_val

            artifacts = []
            for event in alarm_resp.get('alarmsEventDetails', []):

                artifact = {}
                artifact['label'] = 'event'
                artifact['name'] = event['commonEventName']
                artifact['source_data_identifier'] = event['commonEventId']

                cef = {}
                for k, v in event.items():
                    if v is not None:
                        cef[k] = v

                artifact['cef'] = cef
                artifacts.append(artifact)

            artifact = {}
            artifact['label'] = 'alarm'
            artifact['name'] = 'Alarm Info'
            artifact['source_data_identifier'] = alarm_id
            artifact['cef_types'] = {'alarmId': ['logrhythm alarm id']}

            cef = {}
            for k, v in alarm.items():
                if v is not None:
                    cef[k] = v

            artifact['cef'] = cef
            artifacts.append(artifact)
            container['artifacts'] = artifacts

            ret_val, message, container_id = self.save_container(container)

            if phantom.is_fail(ret_val):
                return action_result.set_status(phantom.APP_ERROR, message)

        if not self.is_poll_now() and len(alarms) == int(params["count"]):
            self._state['last_time'] = (datetime.strptime(alarms[-1]['dateInserted'],
                LOGRHYTHM_DATETIME_FORMAT) + timedelta(seconds=1)).strftime(LOGRHYTHM_DATETIME_FORMAT)

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_update_alarm(self, param):
        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))
        action_result = self.add_action_result(ActionResult(dict(param)))

        payload = {}
        method = "patch"
        endpoint = LOGRHYTHM_ALARM_ENDPOINT.format(alarmid=param['id'])

        # rbp = Risk Based Priority (valid values: 0-100)

        if "status" in param:
            payload["alarmStatus"] = param.get("status", "")
            if "rbp" in param:
                # Update both status and rbp
                payload["rBP"] = param.get("rbp", 0)
        elif "rbp" in param:
            # RBP only to update
            payload["rBP"] = param.get("rbp", 0)
        elif "comment" in param:
            payload["alarmComment"] = param.get("comment", "")
            method = "post"
            endpoint += "/comment"
        else:
            not_found = ["status", "comment", "rbp"]
            return action_result.set_status(phantom.APP_ERROR, LOGRHYTHM_PARAMS_NOTFOUND.format(params=not_found))

        # make rest call
        ret_val, response = self._make_rest_call(endpoint, action_result, params=None, method=method, data=json.dumps(payload))

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        # Add the response into the data section
        action_result.add_data(response)
        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_get_events(self, param):
        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))
        action_result = self.add_action_result(ActionResult(dict(param)))

        # make rest call
        ret_val, response = self._make_rest_call(
            LOGRHYTHM_ALARMEVENTS_ENDPOINT.format(alarmid=param['id']), action_result, params=None
        )

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        self.save_progress(LOGRHYTHM_OK)
        # Add the response into the data section
        for event in response["alarmsEventDetails"]:
            action_result.add_data(event)

        # Add a dictionary that is made up of the most important values from data into the summary
        summary = action_result.update_summary({})
        summary['num_events'] = len(response['alarmsEventDetails'])

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_get_summary(self, param):
        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))
        action_result = self.add_action_result(ActionResult(dict(param)))

        # make rest call
        ret_val, response = self._make_rest_call(
            LOGRHYTHM_ALARMSUMMARY_ENDPOINT.format(alarmid=param['id']), action_result, params=None
        )

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        self.save_progress(LOGRHYTHM_OK)
        # Add the response into the data section
        action_result.add_data(response["alarmSummaryDetails"])

        # Add a dictionary that is made up of the most important values from data into the summary
        summary = action_result.update_summary({})
        summary['tot_events_summary'] = len(response['alarmSummaryDetails']['alarmEventSummary'])

        return action_result.set_status(phantom.APP_SUCCESS)

    def handle_action(self, param):
        ret_val = phantom.APP_SUCCESS

        # Get the action that we are supposed to execute for this App Run
        action_id = self.get_action_identifier()

        self.debug_print("action_id", self.get_action_identifier())

        if action_id == 'test_connectivity':
            ret_val = self._handle_test_connectivity(param)

        elif action_id == 'on_poll':
            ret_val = self._handle_on_poll(param)

        elif action_id == 'update_alarm':
            ret_val = self._handle_update_alarm(param)

        elif action_id == 'get_events':
            ret_val = self._handle_get_events(param)

        elif action_id == 'get_summary':
            ret_val = self._handle_get_summary(param)

        return ret_val

    def initialize(self):
        # Load the state in initialize, use it to store data
        # that needs to be accessed across actions
        self._state = self.load_state()

        # get the asset config
        config = self.get_config()
        """
        # Access values in asset config by the name

        # Required values can be accessed directly
        required_config_name = config['required_config_name']

        # Optional values should use the .get() function
        optional_config_name = config.get('optional_config_name')
        """

        self._headers = {
            'Authorization': 'Bearer {}'.format(config['api_key']),
            'Content-Type': 'application/json',
            'cache-control': 'no-cache'
        }

        self._proxies = {}
        env_vars = config.get('_reserved_environment_variables', {})
        if 'HTTP_PROXY' in env_vars:
            self._proxies['http'] = env_vars['HTTP_PROXY']['value']
        if 'HTTPS_PROXY' in env_vars:
            self._proxies['https'] = env_vars['HTTPS_PROXY']['value']

        self._base_url = config.get('base_url')

        # Security check on URL format
        if not self._base_url.endswith('/'):
            self._base_url += "/"

        return phantom.APP_SUCCESS

    def finalize(self):
        # Save the state, this data is saved across actions and app upgrades
        self.save_state(self._state)
        return phantom.APP_SUCCESS


def main():
    import pudb
    import argparse
    import sys

    pudb.set_trace()

    argparser = argparse.ArgumentParser()

    argparser.add_argument('input_test_json', help='Input Test JSON file')
    argparser.add_argument('-u', '--username', help='username', required=False)
    argparser.add_argument('-p', '--password', help='password', required=False)

    args = argparser.parse_args()
    session_id = None

    username = args.username
    password = args.password

    if username is not None and password is None:

        # User specified a username but not a password, so ask
        import getpass
        password = getpass.getpass("Password: ")

    if username and password:
        try:
            login_url = LogrhythmNextgenSiemConnector._get_phantom_base_url() + '/login'

            print("Accessing the Login page")
            r = requests.get(login_url, timeout=60)
            csrftoken = r.cookies['csrftoken']

            data = dict()
            data['username'] = username
            data['password'] = password
            data['csrfmiddlewaretoken'] = csrftoken

            headers = dict()
            headers['Cookie'] = 'csrftoken=' + csrftoken
            headers['Referer'] = login_url

            print("Logging into Platform to get the session id")
            r2 = requests.post(login_url, data=data, headers=headers, timeout=60)
            session_id = r2.cookies['sessionid']
        except Exception as e:
            print("Unable to get session id from the platform. Error: " + str(e))
            sys.exit(1)

    with open(args.input_test_json) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=4))

        connector = LogrhythmNextgenSiemConnector()
        connector.print_progress_message = True

        if session_id is not None:
            in_json['user_session_token'] = session_id
            connector._set_csrf_info(csrftoken, headers['Referer'])

        ret_val = connector._handle_action(json.dumps(in_json), None)
        print(json.dumps(json.loads(ret_val), indent=4))

    sys.exit(0)


if __name__ == '__main__':
    main()
