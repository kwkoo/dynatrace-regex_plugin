# Dynatrace Regex Plugin


This plugin captures values from a text file using regular expressions.

The plugin requires the [OneAgent Plugin SDK](https://dynatrace.github.io/plugin-sdk/index.html).

## Customizing the plugin

Insert the list of regular expressions into `regex_plugin.py`:


	metrics = [ Metric("loadingDuration", '.*Loading Duration is\s*([^\s]*)'), \
	            Metric("scriptPass", '.*Script Pass') ]

If the regular expression has a capture group, the value in the capture group will be used as the metric value.

For example, when the regular expression `.*Loading Duration is\s*([^\s]*)` is matched against `Login Loading Duration is  21.4 secs`, the value captured will be `21.4`.

If the regular expression does not have a capture group, the plugin will output a value of 1 for the metric if the pattern is found and 0 if the pattern is not found.

The name for each metric must match the key for each timeseries specified in `plugin.json`:

	"metrics": [
	  {
	    "timeseries": {
	      "key": "loadingDuration",
	      "unit": "Second",
	      "displayname": "Loading Duration"
	    },
	    "alert_settings": [
	      {
	        ...
	      }
	    ]
	  },
	  {
	    "timeseries": {
	      "key": "scriptPass",
	      "unit": "Count",
	      "displayname":"Script Pass"
	    }
	  }
	],

`plugin.json` is currently configured to activate the plugin whenever a Java process is started:

	"processTypeNames" : [ "JAVA" ],

Refer to the [documentation](https://dynatrace.github.io/plugin-sdk/api/plugin_json_apidoc.html#metadata) for a list of process type names.

## Building the plugin

1. Install Python 3.5.
2. Install the OneAgent SDK.
3. Modify the metrics list in `regex_plugin.py`.
4. Modify the metrics in `plugin.json`.
5. Build the plugin using `oneagent_build_plugin --no_upload`.
6. Install the plugin `.zip` file using the web UI - Settings / Monitored technologies / Custom plugins / Upload OneAgent plugin.
7. Configure the plugin by setting the log filename and the PGI name in the plugin configuration screen.
8. Start the process (configured by in `processTypeNames` and PGI name).

## Testing your regular expressions

You may want to test your regular expressions by setting them in `regex_tester.py` and invoking that. Once you are sure that your regular expressions work, you can copy them into `regex_plugin.py`.

## Error building the plugin

If you encounter the following error when building the plugin:

	Created distribution of the plugin: [('bdist_wheel', '3.5', '/tmp/tmpdmhabckq/dist/regex_plugin-0.1-py3-none-any.whl')]
	Installing plugin to temporary location
	Error occured: module 'pip' has no attribute 'main'

Edit `PYTHON_DIR/site-packages/ruxit/tools/build_plugin.py`, look for the line that says: `pip_status = pip.main([`

Comment that line out, and insert the following:

	#pip_status = pip.main([
	pip_status = subprocess.call([sys.executable, '-m', 'pip',
	    "install",
	    '--ignore-installed',
