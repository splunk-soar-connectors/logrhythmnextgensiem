[comment]: # "  Copyright (c) 2021 Splunk Inc."
[comment]: # ""
[comment]: # "  Licensed under the Apache License, Version 2.0 (the \"License\");"
[comment]: # "  you may not use this file except in compliance with the License."
[comment]: # "  You may obtain a copy of the License at"
[comment]: # ""
[comment]: # "      http://www.apache.org/licenses/LICENSE-2.0"
[comment]: # ""
[comment]: # "  Unless required by applicable law or agreed to in writing, software distributed under"
[comment]: # "  the License is distributed on an \"AS IS\" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,"
[comment]: # "  either express or implied. See the License for the specific language governing permissions"
[comment]: # "  and limitations under the License."
[comment]: # ""

Important notes

*   This app differs from its parent **LogRhythm SIEM** by leveraging LogRhythm RESTful API, in compliance with future releases of LogRhythm NextGen SIEM
*   This app is compatible with Phantom **5.0.0+**

**Port Information**
    - The app uses HTTP/ HTTPS protocol for communicating with the ServiceNow server. Below are the default ports used by Splunk SOAR.

    Service Name | Transport Protocol | Port
    ------------ | ------------------ | ----
    **http** | tcp | 80
    **https** | tcp | 443
