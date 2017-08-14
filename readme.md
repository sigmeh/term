<h4>term</h4>
<h5></h5>

`term` is a command line interface (CLI) emulator for web browsers
which utilizes jquery ajax calls to pass user-typed commands from 
the virtual terminal (in browser) to python scripts on the server. 


Usage:

	$ git clone https://github.com/sigmeh/term
	$ cd term/term
	$ python start.py


The system's default web browser opens a window that points to localhost:8000/term

![term_sample](/media/term_media.png)


The server scripts attempt to 
execute user-typed shell commands and return the results (stdout) for display
to the user (back in the browser's virtual terminal). 

Functionality is predicated on pseudo-traversing the filesystem while keeping
track of current_session (saved to file), which includes current_dir and command 
history. 


In this way the entire filesystem is acccessible to the virtual shell interface. 

It is therefore critical to treat the tool with the same level of care exercised 
when running commands directly in terminal. 