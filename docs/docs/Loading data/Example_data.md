# Example data

*Sweatpy* comes included with a range of example data for testing purposes.

```python
import json

import sweat

example_fit = sweat.example_data(path='4078723797.fit')
```

You can use the example data for testing:

```python
import sweat

data = sweat.read_fit(example_fit.path)
```

If you are looking for a specific file type or sport you can also filter the example data, which returns a `filter` iterable that you can iterator over:
```
import sweat

example_data = sweat.example_data(
    file_type=sweat.FileTypeEnum.fit,
    sport=sweat.SportEnum.cycling)

for ed in example_data:
    # Do fancy things with example data...
```
