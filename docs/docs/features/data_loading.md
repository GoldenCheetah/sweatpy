# Data loading

*Sweatpy* has built-in support for loading these activity file formats:

- [FIT files](#reading-fit-files)

...and coming soon:

- TCX files
- GPX files

## Reading FIT files
The `read_fit()` function accepts strings, [pathlib](https://docs.python.org/3/library/pathlib.html) objects and other file-like objects and returns a [pandas.DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) with column names matching *Sweatpy* [nomenclature](nomenclature.md).

```python
import sweat

example_fit = sweat.examples(path='4078723797.fit')

data = sweat.read_fit(example_fit.path)
```
