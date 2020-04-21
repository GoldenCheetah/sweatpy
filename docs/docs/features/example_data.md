# Example data

*Sweatpy* comes included with a range of example data for testing purposes.

An index of the data is kept [here](https://github.com/GoldenCheetah/sweatpy/blob/master/sweat/examples/index.yml).

```python
import json

import sweat

example_fit = sweat.examples(path='4078723797.fit')
```

You can use the example data for testing:

```python
import sweat

data = sweat.read_fit(example_fit.path)
```

If you are looking for a specific file type or sport you can also filter the example data, which returns a [filter](https://docs.python.org/3/library/functions.html#filter) iterable that you can iterator over:
```
import sweat

examples = sweat.examples(
    file_type=sweat.FileTypeEnum.fit,
    sport=sweat.SportEnum.cycling)

for example in examples:
    # Do fancy things with example data...
```
