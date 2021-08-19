# PhysioNet 2019

## Dataset summary
Contains the data from ["Early Prediction of Sepsis from Clinical Data -- the PhysioNet Computing in Cardiology Challenge 2019"](https://physionet.org/content/challenge-2019/1.0.0/).

This official challenge used a utility score labelling, however its use is a little complicated and so we opt for a more standard 0-1 labelling and do not provide the conversion functions (these can be found from the example code on the PhysioNet website though).

### Processed folder
Contains a single `.npz` file that can be loaded as follows
```python
import numpy as np
npz = np.loadz(filename, allow_pickle=True)
print(npz.files)
```
and the contained files will be shown to be `['data', 'labels', 'columns']`. Both `data` and `labels` are numpy objects that are essentially lists of numpy arrays, with each list element being a 2d array that contains the information from a single patient, labels being of course the corresponding labels to the data attributes. `columns` is a list of strings that correspond to the column names of the data.


### Link
https://physionet.org/content/challenge-2019/1.0.0/

### Citation
```bibtex
@inproceedings{reyna2019early,
  title={Early prediction of sepsis from clinical data: the PhysioNet/Computing in Cardiology Challenge 2019},
  author={Reyna, Matthew A and Josef, Chris and Seyedi, Salman and Jeter, Russell and Shashikumar, Supreeth P and Westover, M Brandon and Sharma, Ashish and Nemati, Shamim and Clifford, Gari D},
  booktitle={2019 Computing in Cardiology (CinC)},
  pages={Page--1},
  year={2019},
  organization={IEEE}
}
```



