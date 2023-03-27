## Hammertrack
![image](https://user-images.githubusercontent.com/105011940/228033347-2dc7df90-6d22-4520-965a-a286b2caedcc.png)
Hammertrack
is a custom file metadata integration between Hammerspace and Ftrack allowing simple selection of files for instantiation in other sites
<!-- ABOUT THE PROJECT -->
## About The Project
Hammertrack is a Ftrack listener that monitors changes to custom location fields in the Ftrack application. Changes to location settings
triggers updates to custom metadata on files and directories associated with specific tasks within Ftrack. This metadata can be used to drive data placement and location
using SmartObjectives on a Hammerspace Global Data Environment.

Currently, hammertrack.py watches for location labels to be added to or removed from Tasks in Ftrack. When 
it sees a location label in the custom field it adds them as Hammerspace labels to the root 
of the specified task folders on a Hammerspace file system. The label schema is configured in Ftrack to match the configuration in hammertrack.py,
and the label names are passed through directly as Hammerspace labels.

<p align="right">(<a href="#top">back to top</a>)</p>

### Built With

* [Python](https://python.org/)
* [Hammerspace Toolkit](https://github.com/hammer-space/hstk)
