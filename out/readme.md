# This Folder is The Default Folder of the outpu
### The Folder contain all the old .htm specified with date ( all pic's links are changed)
### You can change the folder of the ouput :
1. Go to body_generator.py file 
2. Go to the bottom of the code and make the change as you see here : 
```python 
if __name__ == "__main__":
    # By default The folder is "out"
    # Body_GENERATOR()
    Body_GENERATOR(out_choice="THE_NAME_OF_THE_FOLDER")
```