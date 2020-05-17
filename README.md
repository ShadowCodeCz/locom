# Locom

[![PyPI-Status](https://img.shields.io/pypi/v/locom.svg)](https://pypi.org/project/locom/)
[![PyPI-Versions](https://img.shields.io/pypi/pyversions/locom.svg)](https://pypi.org/project/locom/)
[![GitHub issues](https://img.shields.io/github/issues/ShadowCodeCz/locom)](https://github.com/ShadowCodeCz/locom/issues)
[![Build Status](https://travis-ci.com/ShadowCodeCz/locom.svg?branch=master)](https://travis-ci.com/ShadowCodeCz/locom)
[![GitHub license](https://img.shields.io/github/license/ShadowCodeCz/locom)](https://github.com/ShadowCodeCz/locom/blob/master/LICENSE)


Locom is the acronym **lo**g **com**ments. 
It is designed to help with log analysis. 

If you are a tester or systems analyst, you need to go through the logs frequently. 
It is very often useful to take notes or highlight some lines. 
If the log is from complex system, it would be useful share your comments with others. 
It means commented log should be saved in some common format. 
This is exactly what this tool is for.

## Installation 
```python
pip install locom 
``` 

## How it works
1. Get *log file*, which needs to be commented on.

2. Create *rules file*, which describe comments and highlights of the rows.

3. Run *locom* in command line.

4. Get html version of the log with comments and highlights.

## Example
This example is placed [example directory].

### Log: input.txt
```
Brno
Fake row
Prague
Fake row
Bratislava
Fake row
Vienna
Fake row
Warsaw
Fake row
Berlin
Fake row
Paris
Fake row
Stockholm
Fake row
Madrid
Fake row
```

### Rules File: rules.txt
```
re     Brno          red       red comment
re     Prague        green     green comment
re     Bratislava    blue      blue comment
re     Vienna        yellow    yellow comment
row    9             gray      gray comment
row    11            violet    violet comment
re     Paris         low       low row and comment
re     Stockholm     normal    normal row and comment
re     Madrid        hide
```

### CLI
```
locom cli -r rules.txt -i input.txt -o output_example.html  --title "Example of rows and comments" --description "This example shows all possible type of rows and comments."
```
Note: Used Python has to have */Scripts* in the path. 

### Output HTML: output_example.html
![html output example][output_example]

Missing line 17 is not a error. It is result of *hide* render.

## Rules File
One line in file is one rule. Every rules has 3 mandatory parts and 1 optional part. **Parts are separated by 4+ whitespaces**.

Consider this example with named parts. 
```
re                     Brno                red            red comment
[row recognizer type]  [recognizer value]  [render type]  [comment - optional]
```

### Recognizer
2 types of recognizers are implemented:
* **re** - Recognizer value is regular expression for this type of recognizer.

* **row** - Recognizer value is row number for this type of recognizer.

### Renders
List of all renders:
* red
* green 
* blue
* yellow
* gray
* violet
* low 
* normal
* hide

[output_example]: https://github.com/ShadowCodeCz/locom/blob/master/example_img.png?raw=true "HTML output example"
[example directory]: https://github.com/ShadowCodeCz/locom/tree/master/example