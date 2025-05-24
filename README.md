<div align="center">
  <h1>
    <img alt="QueryHound Logo" src="https://github.com/user-attachments/assets/b38871d0-6576-4fe3-b5ef-4bef7b1c417d" width="400" />
  </h1>
  <br>
</div>

# QueryHound

## Overview

**QueryHound** is a Python tool designed to simplify the creation of custom BloodHound queries in JSON format.  
It was developed as part of the [Exegol](https://github.com/ThePorgs/Exegol) project and can be conveniently placed in:  
 `/home/<user>/.exegol/my-resources/setup/bloodhound/customqueries_merge`  
from where it directly generates compatible JSON files ready for use with BloodHound.
> [!CAUTION]
> **This project is currently in Beta and may contain bugs.**  
> Your feedback is highly appreciated. please feel free to open issues or submit pull requests to help improve it!  


---

## Features

- Interactive prompt to create, edit, remove, and manage BloodHound queries  
- Supports multiple sub-queries with "final" flags  
- Easy loading and saving of queries in JSON files  
- Optional graphical-like interface for query summaries (via pager)  
- CLI options for quick actions and streamlined workflow

---

## Installation & Usage

Clone or download the repository, then simply run:

```bash
python3 bloodhound_query.py
````

You will be guided step-by-step through query creation and management.

For more details and command-line options, use:

```bash
python3 bloodhound_query.py -h
```

---

## Planned Improvements

* Develop a more graphical (GUI) interface for easier query creation
* Enhance validation and error handling
* Add templates for common BloodHound query scenarios

---

<div align="center">
  <em>Made for Exegol & BloodHound users</em>
</div>
