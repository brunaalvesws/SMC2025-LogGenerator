## Files templates

To generate some logs, you will need the specified models: Process model, Data Access Model and Organizational Model. The templates for this models are available in the directory "Examples" of this repository. 

# Declare Process Model
The DECLARE template is composed by activities and rules. You can add more activities adding lines in the begining with 'activity' before the activity name. You can add rules adding the Rule name and the activities affected by it followed by optional activation parameters. Some DECLARE rules may not be supported yet.

# Data Access Model
The first column of this template contains the Data Objects that can be accessed, please, keep the column title 'Data Objects' when customizing your own. The other columns are the activities permited operations to each data object of the first column. Put the activity name in the begining of the column and its permited operations separated by comma, the available operations are c (create), u (update), r (read) and d (delete). Capital letters indicate mandatory operations, small letters indicate optional operation and the absense of the letter indicates the operation is forbidden.

# Organizational Model
In this template, please do not change the column header, it has the same name of the log columns to make it easier. The first column refers to the case name, so you need to add an profile and resources to each case. Follow the pattern 'case_{number of the case}' starting by 0. Then, in the second column, add a profile name and in the third column, add a resource list for this profile separated by comma.

All the activity names, resources, profiles and data objects can be customized. The generator will warn you if something is not right.