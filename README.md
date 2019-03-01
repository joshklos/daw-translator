# daw-translator
Python script to convert DAW (digital audio workstation) session files between different DAWs

**Still in initial development, currently the two interpreters written so far only read the files**

Supported DAWs (pre-installed interpreters):
  - Hindenburg
  - Reaper

Installing Additional Interpreters:
  - Add the interpreter python file to the interpreters folder
  - Add the interpreter name to the import list at the beginning interpreter_index.py
  - Add a record for the interpreter to the 'interpreters' tuple including:
    1. A list of any extensions that interpreter can convert from
    2. The name of the DAW that interpreter (and the file extensions) are associated with
    3. The Interpreter class
  - That's it, you should now be able to use the new interpreter

 Writing New Interpreters:
   - This project will be most useful if others help to build the library of interpreters.
   Requirements:
    - The interpreter should be written as a class
    - It should have a "read" function that accepts two parameters 1) The original session file 2) a debug setting,
      this function should read the session file and convert it to a Session object as defined in "object_classes"
      and return that session object
    - It should have a "write" function that accepts two parameters 1) A session object 2) a debug setting,
      this function should take a session object and create a string that can be written out to a file that will create
      the appropriate file, it should return that string to be written to a file by main.py
