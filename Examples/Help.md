## File Templates

To generate logs, you will need three models: **Process Model**, **Data Access Model**, and **Organizational Model**. Templates for these models are available in the `Examples` directory of this repository.

---

### Process Model (DECLARE)

The DECLARE template is composed of activities and rules.

* To add more activities, include new lines at the beginning with the keyword `activity` followed by the activity name.
* To add rules, write the rule name and the activities affected by it, followed by optional activation parameters.

> Note: Some DECLARE rules may not yet be supported.

---

### Data Access Model

* The **first column** of this template contains the data objects that can be accessed. Please keep the column title as **`Data Objects`** when customizing your own.
* The **other columns** define the permitted operations of each activity on the data objects listed in the first column.

Use the following notation:

* Place the **activity name** at the top of the column.
* List the permitted operations separated by commas for each data object:

  * `c` = create
  * `u` = update
  * `r` = read
  * `d` = delete

**Capital letters** indicate mandatory operations, **lowercase letters** indicate optional operations, and the absence of a letter indicates the operation is **forbidden**.

---

### Organizational Model

In this template, do not change the column headers, since they match the log column names for easier processing.

* The **first column** refers to the case name. Add a profile and resources to each case, following the pattern `case_{number}` starting from `case_0`. Remember to verify the number of cases you want to generate.
* The **second column** specifies the profile name.
* The **third column** lists the resources for this profile, separated by commas.

---

All activity names, resources, profiles, and data objects can be customized. The generator will issue warnings if something is not valid.
