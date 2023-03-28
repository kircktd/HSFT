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

### Configuration

1. You first need to setup your storage location and storage senerio and define the centralized storage senerio using your Hammerspace fileshare.
    ![image](https://user-images.githubusercontent.com/105011940/228307502-308db076-748e-4b02-8ab9-c97eef800fd4.png)
    ![image](https://user-images.githubusercontent.com/105011940/228307807-56aa2865-f2e4-4a4b-8eef-7d9c7b6f20b3.png)

3. Go to the setting page with in Ftrack and selctect "Custom Attributes"
![image](https://user-images.githubusercontent.com/105011940/228266626-44af6aa0-57cc-4606-903e-b1c728917ff7.png)
3. Create a new Custom Attribute where you define the locations of your Hammerspace clusters. You must enter a "menu' name that is normally the location, and then for each menu name you have to add a value which in this example the value is the 3 letter acronym for the local airport associated with the city name.

     ![image](https://user-images.githubusercontent.com/105011940/228268855-b55805f4-76a1-4fa4-ab65-2c7204b22ed1.png)
4. Next you need to add the custom attribute to your Ftrack project. Select Attributes, Custom Attributes, Task.

     ![image](https://user-images.githubusercontent.com/105011940/228275544-05e83a65-ae41-40cf-afdd-209d5d010b22.png)


5. Edit the hammertrack.py script to set the location sites using a key word value and menu name to match the settings in Ftrack for the site locations (line 90). 

     ![image](https://user-images.githubusercontent.com/105011940/228274133-c9e93751-0dd6-4502-8f12-9da2c02396bc.png)

6. One or more Hammerspace clusters set up with label-based objectives to drive data placement 
(e.g. `IF HAS_LABEL("LOCATION") THEN {SLO('place-on-local-volumes)}`)
7. Add the value labels to each Hammerspace cluster by logging into each Hammerspace primary anvil and adding the associated labels. Once completed do a "label-list" to verify all the required labels are defined. Repeat this step on all primary Anvil servers.

      ![image](https://user-images.githubusercontent.com/105011940/228278000-2d4e1a69-489c-4bd9-81d3-bc18468f5fb5.png)
      ![image](https://user-images.githubusercontent.com/105011940/228278742-e725880c-5d61-4566-b789-dbb018a786e3.png)
 
 8. Launch the hammpertrack.py script in the backround on your Windows or Linux server. The listener will monitor for location changes in Ftrack project and will update the metatdata for the files on the Hammerspace fileshare with the appropiate labels. Once these labels are detected by the Hammerspace sweeper as valid objectives the files associated with the labels will be placed-on the Hammerspace cluster that is associated with the specified location.

<!-- USAGE EXAMPLES -->
## Usage

Once the Ftrack instance and the hammertrack.py script have been configured it will recognize location change events on Tasks and act accordingly. Launch the hammertrack.py script on your windows or linux server where the Hammerspace Fileshare is mounted. With in the project view select a task and update the location field (make sure you hit the save button after the update). Once that is done the script will pick-up on the event and will update the directory for the specified project with the unique location metadata.
   ![image](https://user-images.githubusercontent.com/105011940/228309945-68bab50b-56f5-4a84-8804-27e94fda6838.png)


 

