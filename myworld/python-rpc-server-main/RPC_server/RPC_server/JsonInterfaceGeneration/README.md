JSON Interface Generator

Generates a JSON interface from the docstring of a function or a class.


Example of testInterface.py's output:
Example 1:
```json
{
   "foo":{
      "info":"Summarize the function in one line.",
      "parameters":{
         "var1":{
            "type":"array_like",
            "info":"Array_like means all those objects -- lists, nested lists, etc. -- that can be converted to an array.  We can also refer to variables like `var1`."
         },
         "var2":{
            "type":"int",
            "info":"The type above can either refer to an actual Python type (e.g. ``int``), or describe the type of the variable in more detail, e.g. ``(N,) ndarray`` or ``array_like``."
         },
         "*args":{
            "type":"iterable",
            "info":"Other arguments."
         },
         "long_var_name":{
            "type":"{'hi', 'ho'}",
            "default":"'hi'",
            "info":"Choices in brackets, default first when optional."
         },
         "only_seldom_used_keyword":{
            "type":"int",
            "WARNING":"parameter is optional, but no default value found",
            "info":"Infrequently used parameters can be described under this optional section to prevent cluttering the Parameters section."
         },
         "**kwargs":{
            "type":"dict",
            "info":"Other infrequently used keyword arguments. Note that all keyword arguments appearing after the first parameter specified under the Other Parameters section, should also be described under this section."
         }
      },
      "returns":{
         "anonymous value 1":{
            "type":"type",
            "info":"Explanation of anonymous return value of type ``type``."
         },
         "describe":{
            "type":"type",
            "info":"Explanation of return value named `describe`."
         },
         "out":{
            "type":"type",
            "info":"Explanation of `out`."
         },
         "anonymous value 2":{
            "type":"type_without_description",
            "info":""
         }
      }
   }
}
```
Example 2:
```json
{
   "DDS_Interface":{
      "info":"information about the class DDS_Interface. This is another line.  This line is NOT ignored.",
      "functions":{
         "get_overtemp":{
            "info":"returns true if the DDS core temperature is to hot.",
            "parameters":{
               
            },
            "returns":{
               "temperature":{
                  "type":"bool",
                  "info":"true, if too hot."
               }
            }
         },
         "set_state":{
            "info":"sets the triple frequency, amplitude and phase.",
            "parameters":{
               "frequency":{
                  "type":"float",
                  "info":"DDS frequency in Hz."
               },
               "amplitude":{
                  "type":"float",
                  "info":"Amplitude in dB. Max limit is 26dB."
               },
               "phase":{
                  "type":"float",
                  "info":"Offset Phase in radiant to atomic clock, if connected."
               }
            },
            "returns":{
               
            }
         }
      }
   }
}
```
Example 3:
```json
{
   "generate":{
      "info":"Generates a JSON interface for a function or class.",
      "parameters":{
         "input_":{
            "type":"[class, function]",
            "info":"Function or class to be described."
         }
      },
      "returns":{
         "anonymous value 1":{
            "type":"str",
            "info":"JSON 
interface containing information about the function/class."
         }
      }
   }
}
```
Example 4:
```json
{
   "generate_func":{
      "info":"Generates a dictionary describing info, parameters and returns of a function from its docstring.",
      "parameters":{
         "input_":{
            "type":"function",
            "info":"The function to be described."
         },
         "indent":{
            "type":"int",
            "default":"1, for functions inside a class 2",
            "info":"Factor describing the indentation"
         }
      },
      "returns":{
         "func_dict":{
            "type":"dict",
            "info":"Dictionary that contains info, parameters and returns of a function."
         }
      }
   }
}
```
