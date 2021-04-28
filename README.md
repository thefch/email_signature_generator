# Simple email signature generator

`data.csv` holds the details of the people/person

Only tested with Microsoft Outlook (Desktop) 

<b>Copy</b> and <b>paste</b> from the HTML page into Outlook

##### `data.csv`
 - Holds all data related to user
 - Can be modified manually but remember to have a sequence of consecutive ids
 - Put any info that are required in the signature for each person
 - Do not modify the field names, if so, internal app changes need to be done.
##### `settings.csv`
 - Holds setting data for each company/template
 - Add related social media links
 - Icon links can be changed through here
 - Only the listed ones are supported
 - Template name need to have a related folder with that name 
 >eg. company-slug/template-name

##### logos
 - The logos need to be replaces accordingly from `static\assets`
 - Need to be added manually to the template to avoid any issues with two or more logos in one signature 


> <b>Keep</b> the `data.csv` file safe!

---

#### `venv`
Create a new enviroment with `python -m venv <name_of_virtualenv>` or `py -m venv <name_of_virtualenv>`

##Notes
 - Template code (HTML) should be pasted/writen inside `{% block content %}`
and `{% endblock %}` to avoid issues with the functionality of `copy` button.

 - The script for `copyToClipboard()` is located in `base.html` and will be added after every signature. If removed from `base.html` will cause issues with the `copy` button.

 - If `copy` is not working, use the traditional method: `select->right-click->copy`
   <br><br>
>if there is a styling problem when copying and pasting the signature on outlook, try copying to a word document and then outlook
