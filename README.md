# Simple email signature generator

`data.csv` needs to hold the details of the people/person

Only tested with Microsoft Outlook (Desktop) 

<b>Copy</b> and <b>paste</b> from the HTML page into Outlook

##### `data.csv`
 - holds all data related to user
 - can be modified manually but remember to have a sequence of concecutive ids
 - put any info that are required in the signature for each person

##### `settings.csv`
 - holds setting data for each company/template
 - add related social media links
 - icon links can be changed through here
 - only the listed ones are supported
 - template name need to have a related folder with that name 
 >eg. company-slug/template-name

##### logos
 - the logos needs to be replaces accordingly from `static\assets`
 - need to be added manually to the template to avoid any issues with two or more logos in one signature 


> <b>Keep</b> the `data.csv` file safe!

---

#### `venv`
Create a new enviroment with `python -m venv <name_of_virtualenv>` or `py -m venv <name_of_virtualenv>`

<br><br>
>if there is a styling problem when copying and pasting the signature on outlook, try copying to a word document and then outlook
