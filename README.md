# Datasets
I have finally got tired have creating individual `get_data` scripts that do the same things over and over again everytime I start a new project.

This module creates a template for downloading and simple processing using shared functions.

It follows structurally somewhat like HuggingFace's datasets module, but simpler.

## Functions
The only function of importance (at the moment) is the `download` function. Usage is simple:
```
download(dataset_name='renet2', download_location='./data')
```

## Datasets
Information on the individual datasets can be seen in their respective folders.