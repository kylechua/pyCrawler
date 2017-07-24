Web Crawler
===========

This application retrieves API data given a series of queries from an input file. It is intended to be modular to work with any API which returns JSON data.

* **Language:** Python 3.x
* **Storage:** File

---

### Using the crawler

1. Store the input file in the input file directory (by default it is './data/in/')

2. Run crawler.py

3. Provide the input filename and the desired output filename (including extensions)

4. The data will be parsed to the output file directory ('./data/out/')

---

### Input file syntax
* An input file should use the following syntax:
 * {source}
 * {query1}
 * {query2}
 * {query...}

* {source} should be either API URL, or a known source found in /package/info.py

* {query} syntax is as follows:
 * {arg1}={value},{arg2}={value},{arg...}={value}
 * Whitespace is considered a part of the query
 * Unspecified arguments will be considered empty

---

### Adding parser plugins

The web crawler will send the JSON data from the API request to a parser plugin. A couple of example plugins are provided in the package. In order to add additional plugins, simply include the module in /package/ and add the source to the database in  /package/info.py