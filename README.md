# wikiedits-api

A Python client library for accessing Wikipedia editor analytics from the Wikimedia Analytics API.

## Installation

```bash
pip install wikiedits-api
```

Or install from source:

```bash
git clone https://github.com/cswatt/wikiedits-api.git
cd wikiedits-api
pip install -e .
```

## Usage

On 3 December 2024, Yoon Suk Yeol attempted to declare martial law in the Republic of Korea. Between 3 December 2024 00:00 GMT and 4 December 2024 00:00 GMT, how many edits were made to the [English Wikipedia page about the ensuing political crisis](https://en.wikipedia.org/wiki/2024_South_Korean_martial_law_crisis)?

```python
import wikiedits

wikiedits.edits(
  "20241203", 
  "20241204", 
  project="en.wikipedia.org",
  page_title="2024_South_Korean_martial_law_crisis")
```

```
713
```

During that same month, how many edits were made to the Korean-language Wikipedia project?

```python
wikiedits.edits(
  "20241201", 
  "20241231", 
  project="ko.wikipedia.org")
```

```
148092
```

On 4 December 2024, Michel Barnier became the first French prime minister to lose a vote of no-confidence since 1962. How much did the [English-language Michel Barnier page](https://en.wikipedia.org/wiki/Michel_Barnier) change between 4 December 2024 00:00 GMT and 5 December 2025 00:00 GMT?

Net byte changes (additions minus deletions):

```python
wikiedits.bytes(
  "20241204", 
  "20241205",
  diff_type="net",
  project="en.wikipedia.org",
  page_title="Michel_Barnier")
```

```
1627
```

Absolute byte changes (additions plus deletions):

```python
wikiedits.bytes(
  "20241204", 
  "20241205",
  diff_type="absolute",
  project="en.wikipedia.org",
  page_title="Michel_Barnier")
```

```
2247
```

How many pages received 100 or more edits in the English Wikipedia project in 2024?

```python
wikiedits.pages(
  "20240101", 
  "20241231",
  change_type="edited",
  project="en.wikipedia.org",
  activity_level="100..-edits")
```

```
5362
```

What were the 5 most edited articles (by number of edits) in the English Wikipedia project on New Year's Day 2025?

```python
wikiedits.top(
  "20250101",
  by="edits",
  count=5,
  page_type="content",
  project="en.wikipedia.org")
```

```
[{'page_title': '2025_New_Orleans_truck_attack', 'edits': 726, 'rank': 1}, 
 {'page_title': 'Jimmy_Carter', 'edits': 113, 'rank': 2}, 
 {'page_title': 'Islington_Handball_Club', 'edits': 102, 'rank': 3}, 
 {'page_title': 'List_of_Saturday_Night_Live_writers', 'edits': 98, 'rank': 4}, 
 {'page_title': '2025', 'edits': 87, 'rank': 5}]
```

See [docs/functions.md](docs/functions.md) for a complete list of functions and parameter details.


## Rate Limits

The Wikimedia API has rate limits. The library includes a 30-second timeout for requests. For high-volume usage, consider implementing delays between requests.

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and add tests
4. Run tests: `python -m pytest`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Links

- [Wikimedia Analytics API Documentation](https://wikimedia.org/api/rest_v1/#/)

## Claude Code workflow

### Slash commands

-`/rename-fn <old> <new>`: Renames a function across the project.