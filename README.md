## Hammertrack
![image](https://user-images.githubusercontent.com/105011940/228033347-2dc7df90-6d22-4520-965a-a286b2caedcc.png)
Hammertrack
is a custom file metadata integration between Hammerspace and Ftrack allowing simple selection of files for instantiation in other sites
<!-- ABOUT THE PROJECT -->
## About The Project
Hammertrack is a Ftrack listener that monitors changes to custom location fields in the Ftrack application. Changes to location settings
triggers updates to custom metadata on files and directories associated with specific tasks within Ftrack. This metadata can be used to drive data placement and location
using SmartObjectives on a Hammerspace Global Data Environment.

Currently, hammertrack.py watches for location fields to be added to or removed from Tasks in Ftrack. When 
it sees a location label in the custom field it adds them as Hammerspace labels to the root 
of the specified task folders on a Hammerspace file system. The label schema is configured in Ftrack to match the configuration in hammertrack.py,
and the label names are passed through directly as Hammerspace labels.

<p align="right">(<a href="#top">back to top</a>)</p>

### Built With

* [Python](https://python.org/)
* [Ftrack API](https://help.ftrack.com/en/articles/1054630-getting-started-with-the-api)
* [Hammerspace Toolkit](https://github.com/hammer-space/hstk)
<p align="right">(<a href="#top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

Here are some basics on getting up and running. Everyone's Ftrack instance is configured a bit differently and
will require some configuration.
### Prerequisites

1. [Ftrack API](https://help.ftrack.com/en/articles/1054630-getting-started-with-the-api) installed and configured `$ pip install ftrack-python-api`
2. [Hammerspace Toolkit](https://github.com/hammer-space/hstk) (hstk) installed: `$ pip install hstk`
3. Hammerspace file system mounted

### Installation

1. Clone this repository `git clone https://github.com/kircktd/hsft.git`
2. Copy or link hammertrack.py to the working directory on your server
3. Install requirements `pip install -r requirements.txt`

### Configuration

1. Edit the hammertrack.py script to set the location sites using a key word value and menu name to match the settings in Ftrack for the site locations (line 90).
2. Copy or link shothammer_config.yml to shotgunEvents working directory 
3. One or more Hammerspace clusters set up with keyword-based objectives to drive data placement 
(e.g. `IF HAS_KEYWORD("SGHS_LOCATION") THEN {SLO('place-on-local-volumes)}`)
