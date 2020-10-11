# Snippitz
A personal file manager specializing in synaptically organizing and files and folder.

# Abstraction
Provide snippitz with the path of a file or folder and it will return all files and folders connected to it.
The connections between files and folders are entirely customizable and the meaning of these connections is given by the user.

For example, photos taken during a road trip may be catagorized as "road trip" but there may be photos that could be catagorized as "family photos" or "historic landmarks"
By connecting each photo to its appropriate tag, you can place photos in multiple groups without needing to store multiple copies of the photo.

On top of allowing you to traverse these connecitons, snippitz also provides methods for creating, managing, and removing these connections.

As of this point, snippitz is only a gate keeper to the file manager, providing an API for other programs to use. Should the user want to browse their files, a separate program will need to be written.
