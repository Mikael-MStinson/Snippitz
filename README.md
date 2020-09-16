# Snippitz
A personal file manager specializing in semantically organizing and accessing small files and chunks of data


## Design Notes
Start simple. Build a system that can take a new file and automatically tie it to the tag "unsorted".
Tags in this sense are going to be files themselves.
Then give it the ability to tie files to other files.
Lastly give it the ability to retrieve files based on tags - e.g. retrieve all files tied to x.

As for the file structure, I think everything should be organized by year/month/day. This should reduce the amount of data pulled from the harddrive when accessing it.
Though it might also be worth it to sort things by file type. For now, let's just use the year/month/day structure.


I might utilize databases for some of these functions, but for the most part, I'm going to be storing all files in their raw form. That way programs have direct access to them.

the business logic should be separate from the ui logic, with the intention of evenually plugging an AI into it.

lastly, the file structure will be backed up and synced with google, but I should plan on it working with other sync programs too.
This means that should a file not be present, the system should notify the user and tell them to resync it.

I'll need an entry point.
Those will most likely be tags, though we could make a catagory called entry points.

I think for now, this is enough.

#### Methods:
* register_file - creates a new file and ties it to the "unsorted" tag 
* tie - takes 2 files and ties them together
* severe - severe the tie between two files
* list - gets all files associated to that file
* address_of - gets the address of a file
