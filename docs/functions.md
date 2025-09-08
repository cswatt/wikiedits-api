# Function reference
- [`edits`](#edits): How many edits have been made in a given time period
- `bytes`: How much things have changed, in bytes, in a given time period
- `pages`: How many pages have been added or modified in a given time period
- `top`: Which pages have been changed the most
- [Basic API wrappers](#basic-api-wrappers)
   - [`/edits/aggregate`](#edits_aggregate)
   - [`/edits/per-page`](#edits_per_page)
   - [`/bytes-difference/net/aggregate`](#bytes_diff_net_aggregate)
   - [`/bytes-difference/net/per-page`](#bytes_diff_per_page)
   - [`/bytes-difference/absolute/aggregate`](#bytes_diff_abs_aggregate)
   - [`/bytes-difference/absolute/per-page`](#bytes_diff_abs_per_page)
   - [`/edited-pages/new`](#new_pages)
   - [`/edited-pages/aggregate`](#edited_pages)
   - [`/edited-pages/top-by-net-bytes-difference/`](#top_by_net_diff)
   - [`/edited-pages/top-by-absolute-bytes-difference/`](#top_by_abs_diff)
   - [`/edited-pages/top-by-edits/`](#top_by_edits)

### `edits`

`edits(start, end, project='all-projects', page_title=None, editor_type='all-editor-types')`

How many edits have been made between `start` and `end`?

<details>
<summary>Parameters</summary>

- `start` (str, **required**): First day to include. YYYYMMDD, ISO format, or human-readable.
- `end` (str, **required**): Last day to include. YYYYMMDD, ISO format, or human-readable.
- `project` (str, _optional_, default: `all-projects`): The Wikimedia project to look at, e.g. `en.wikipedia.org`, `all-wikipedia-projects`, `all-projects`.
- `page_title` (str, _optional_, default: `None`): The title of a page. If not specified, looks at the whole project.
- `editor_type` (str, _optional_, default: `all-editor-types`): Type of editor.
   Allowed: `all-editor-types`, `anonymous`, `group-bot` (registered accounts belonging to the bot group), `name-bot` (registered accounts with bot-like names), `user`

</details>

#### Examples

On 3 December 2024, Yoon Suk Yeol attempted to declare martial law in the Republic of Korea. Between 3 December 2024 00:00 GMT and 4 December 2024 00:00 GMT, how many edits were made to the [English Wikipedia page about the ensuing political crisis](https://en.wikipedia.org/wiki/2024_South_Korean_martial_law_crisis)?

```python
import wikiedits

wikiedits.edits("20241203", 
                "20241204", 
                project="en.wikipedia.org",
                page_title="2024_South_Korean_martial_law_crisis")
```

```
713
```

During that month, how many edits were made to the Korean-language Wikipedia project?

```python
import wikiedits

wikiedits.edits("20241201", 
                "20241231", 
                project="ko.wikipedia.org")
```

```
148092
```

### `bytes`

`bytes(start, end, diff_type='absolute', project='all-projects', page_title=None, editor_type='all-editor-types', page_type='all-page-types)`

How many bytes have changed between `start` and `end`?

<details>
<summary>Parameters</summary>

- `start` (str, **required**): First day to include. YYYYMMDD, ISO format, or human-readable.
- `end` (str, **required**): Last day to include. YYYYMMDD, ISO format, or human-readable.
- `diff_type` (str, _optional_, default: `absolute`): How to add up changes.
   Allowed: `absolute` (additions plus deletions), `net` (additions minus deletions)
- `project` (str, _optional_, default: `all-projects`): The Wikimedia project to look at, e.g. `en.wikipedia.org`, `all-wikipedia-projects`, `all-projects`.
- `page_title` (str, _optional_, default: `None`): The title of a page. If not specified, looks at the whole project.
- `editor_type` (str, _optional_, default: `all-editor-types`): Type of editor.
   Allowed: `all-editor-types`, `anonymous`, `group-bot` (registered accounts belonging to the bot group), `name-bot` (registered accounts with bot-like names), `user`
- `page_type` (str, _optional_, default: `all-page-types`): Type of page. If you specify `page_title`, this value is ignored.
   Allowed: `all-page-types`, `content` (articles), `non-content` (e.g. discussion pages)

</details>

#### Examples

On 4 December 2024, Michel Barnier became the first French prime minister to lose a vote of no-confidence since 1962. How much did the [English-language Michel Barnier page](https://en.wikipedia.org/wiki/Michel_Barnier) change between 4 December 2024 00:00 GMT and 5 December 2025 00:00 GMT?

Net byte changes (additions minus deletions):

```python
import wikiedits

wikiedits.bytes("20241204", 
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
import wikiedits

wikiedits.bytes("20241204", 
                "20241205",
                diff_type="absolute",
                project="en.wikipedia.org",
                page_title="Michel_Barnier")
```

```
2247
```

### `pages`

`pages(start, end, change_type='edited', project='all-projects', editor_type='all-editor-types', activity_level='all-activity-levels', page_type='all-page-types')`

How many pages were created or edited between `start` and `end`?

<details>
<summary>Parameters</summary>

- `start` (str, **required**): First day to include. YYYYMMDD, ISO format, or human-readable.
- `end` (str, **required**): Last day to include. YYYYMMDD, ISO format, or human-readable.
- `change_type` (str, _optional_, default: `edited`): Whether to ask for new or edited pages.
   Allowed: `new`, `edited`
- `project` (str, _optional_, default: `all-projects`): The Wikimedia project to look at, e.g. `en.wikipedia.org`, `all-wikipedia-projects`, `all-projects`.
- `editor_type` (str, _optional_, default: `all-editor-types`): Type of editor.
   Allowed: `all-editor-types`, `anonymous`, `group-bot` (registered accounts belonging to the bot group), `name-bot` (registered accounts with bot-like names), `user`
- `activity_level` (str, _optional_, default: `all-activity-levels`): Editor activity range. If `change_type == "new"`, this value is ignored.
   Allowed: `all-activity-levels`, `1..4-edits`, `5..24-edits`, `25..99-edits`, `100..-edits`
- `page_type` (str, _optional_, default: `all-page-types`): Type of page. 
   Allowed: `all-page-types`, `content` (articles), `non-content` (e.g. discussion pages)

</details>

#### Examples

How many new pages were created on New Year's Day 2025 by logged-in users in the English Wikipedia project?

```python
wikiedits.pages("20250101", 
                "20250102",
                change_type="new",
                project="en.wikipedia.org",
                editor_type="user")
```

```
3920
```

How many pages received 100 or more edits iin the English Wikipedia project in 2024?

```python
wikiedits.pages("20240101", 
                "20241231",
                change_type="edited",
                project="en.wikipedia.org",
                activity_level="100..-edits")
```

```
5362
```

### `top`

#### Examples

### Basic API wrappers

Wrapper functions for all endpoints in the [Wikimedia Edit Analytics API](https://doc.wikimedia.org/generated-data-platform/aqs/analytics-api/reference/edits.html).

### `edits_aggregate`

`edits_aggregate(project, granularity, start, end, editor_type='all-editor-types', page_type='all-page-types')`

Get number of edits.

<details>
<summary>Parameters</summary>

- `project` (str): The Wikimedia project to look at, e.g. `en.wikipedia.org`, `all-wikipedia-projects`, `all-projects`
- `granularity` (str): Time interval between data points.
   Allowed: `daily`, `monthly`
- `start` (str): First day to include. YYYYMMDD, ISO format, or human-readable.
- `end` (str): Last day to include. YYYYMMDD, ISO format, or human-readable.
- `editor_type` (str): Type of editor.
   Allowed: `all-editor-types`, `anonymous`, `group-bot` (registered accounts belonging to the bot group), `name-bot` (registered accounts with bot-like names), `user`
- `page_type` (str): Type of page.
   Allowed: `all-page-types`, `content` (articles), `non-content` (e.g. discussion pages)

</details>

### edits_per_page
`edits_per_page(project, page_title, granularity, start, end, editor_type='all-editor-types')`

Get number of edits to a page.

<details>
<summary>Parameters</summary>

- `project` (str): The Wikimedia project to look at, e.g. `en.wikipedia.org`, `all-wikipedia-projects`, `all-projects`
- `page_title` (str): Page title in URL-encoded format, e.g. `Climate_change`
- `granularity` (str): Time interval between data points.
   Allowed: `daily`, `monthly`
- `start` (str): First day to include. YYYYMMDD, ISO format, or human-readable.
- `end` (str): Last day to include. YYYYMMDD, ISO format, or human-readable.
- `editor_type` (str): Type of editor.
   Allowed: `all-editor-types`, `anonymous`, `group-bot` (registered accounts belonging to the bot group), `name-bot` (registered accounts with bot-like names), `user`
- `page_type` (str): Type of page.
   Allowed: `all-page-types`, `content` (articles), `non-content` (e.g. discussion pages)

</details>

### bytes_diff_net_aggregate
`bytes_diff_net_aggregate(project, granularity, start, end, editor_type='all-editor-types', page_type='all-page-types')`

Get net byte changes (additions minus deletions).

<details>
<summary>Parameters</summary>

- `project` (str): The Wikimedia project to look at, e.g. `en.wikipedia.org`, `all-wikipedia-projects`, `all-projects`
- `granularity` (str): Time interval between data points.
   Allowed: `daily`, `monthly`
- `start` (str): First day to include. YYYYMMDD, ISO format, or human-readable.
- `end` (str): Last day to include. YYYYMMDD, ISO format, or human-readable.
- `editor_type` (str): Type of editor.
   Allowed: `all-editor-types`, `anonymous`, `group-bot` (registered accounts belonging to the bot group), `name-bot` (registered accounts with bot-like names), `user`
- `page_type` (str): Type of page.
   Allowed: `all-page-types`, `content` (articles), `non-content` (e.g. discussion pages)

</details>

### bytes_diff_per_page

`bytes_diff_per_page(project, page_title, granularity, start, end, editor_type='all-editor-types')`

Get net byte changes (additions minus deletions) to a page.

<details>
<summary>Parameters</summary>

- `project` (str): The Wikimedia project to look at, e.g. `en.wikipedia.org`, `all-wikipedia-projects`, `all-projects`
- `page_title` (str): Page title in URL-encoded format, e.g. `Climate_change`
- `granularity` (str): Time interval between data points.
   Allowed: `daily`, `monthly`
- `start` (str): First day to include. YYYYMMDD, ISO format, or human-readable.
- `end` (str): Last day to include. YYYYMMDD, ISO format, or human-readable.
- `editor_type` (str): Type of editor.
   Allowed: `all-editor-types`, `anonymous`, `group-bot` (registered accounts belonging to the bot group), `name-bot` (registered accounts with bot-like names), `user`
- `page_type` (str): Type of page.
   Allowed: `all-page-types`, `content` (articles), `non-content` (e.g. discussion pages)

</details>

### bytes_diff_abs_aggregate
`bytes_diff_abs_aggregate(project, granularity, start, end, editor_type='all-editor-types', page_type='all-page-types')`

<details>
<summary>Parameters</summary>

- `project` (str): The Wikimedia project to look at, e.g. `en.wikipedia.org`, `all-wikipedia-projects`, `all-projects`
- `granularity` (str): Time interval between data points.
   Allowed: `daily`, `monthly`
- `start` (str): First day to include. YYYYMMDD, ISO format, or human-readable.
- `end` (str): Last day to include. YYYYMMDD, ISO format, or human-readable.
- `editor_type` (str): Type of editor.
   Allowed: `all-editor-types`, `anonymous`, `group-bot` (registered accounts belonging to the bot group), `name-bot` (registered accounts with bot-like names), `user`
- `page_type` (str): Type of page.
   Allowed: `all-page-types`, `content` (articles), `non-content` (e.g. discussion pages)

</details>

Get absolute byte changes (total additions + deletions).

### bytes_diff_abs_per_page
`bytes_diff_abs_per_page(project, page_title, granularity, start, end, editor_type='all-editor-types')`

Get absolute byte changes (additions + deletions) to a page.

<details>
<summary>Parameters</summary>

- `project` (str): The Wikimedia project to look at, e.g. `en.wikipedia.org`, `all-wikipedia-projects`, `all-projects`
- `page_title` (str): Page title in URL-encoded format, e.g. `Climate_change`
- `granularity` (str): Time interval between data points.
   Allowed: `daily`, `monthly`
- `start` (str): First day to include. YYYYMMDD, ISO format, or human-readable.
- `end` (str): Last day to include. YYYYMMDD, ISO format, or human-readable.
- `editor_type` (str): Type of editor.
   Allowed: `all-editor-types`, `anonymous`, `group-bot` (registered accounts belonging to the bot group), `name-bot` (registered accounts with bot-like names), `user`
- `page_type` (str): Type of page.
   Allowed: `all-page-types`, `content` (articles), `non-content` (e.g. discussion pages)

</details>

### new_pages
`new_pages(project, granularity, start, end, editor_type='all-editor-types', page_type='all-page-types')`

Get number of new pages.

<details>
<summary>Parameters</summary>

- `project` (str): The Wikimedia project to look at, e.g. `en.wikipedia.org`, `all-wikipedia-projects`, `all-projects`
- `granularity` (str): Time interval between data points.
   Allowed: `daily`, `monthly`
- `start` (str): First day to include. YYYYMMDD, ISO format, or human-readable.
- `end` (str): Last day to include. YYYYMMDD, ISO format, or human-readable.
- `editor_type` (str): Type of editor.
   Allowed: `all-editor-types`, `anonymous`, `group-bot` (registered accounts belonging to the bot group), `name-bot` (registered accounts with bot-like names), `user`
- `page_type` (str): Type of page.
   Allowed: `all-page-types`, `content` (articles), `non-content` (e.g. discussion pages)

</details>

### edited_pages
`edited_pages(project, granularity, start, end, editor_type='all-editor-types', page_type='all-page-types', activity_level='all-activity-levels')`

Get number of edited pages.

<details>
<summary>Parameters</summary>

- `project` (str): The Wikimedia project to look at, e.g. `en.wikipedia.org`, `all-wikipedia-projects`, `all-projects`
- `granularity` (str): Time interval between data points.
   Allowed: `daily`, `monthly`
- `start` (str): First day to include. YYYYMMDD, ISO format, or human-readable.
- `end` (str): Last day to include. YYYYMMDD, ISO format, or human-readable.
- `editor_type` (str): Type of editor.
   Allowed: `all-editor-types`, `anonymous`, `group-bot` (registered accounts belonging to the bot group), `name-bot` (registered accounts with bot-like names), `user`
- `page_type` (str): Type of page.
   Allowed: `all-page-types`, `content` (articles), `non-content` (e.g. discussion pages)
- `activity_level` (str) : Editor activity range.
   Allowed: `all-activity-levels`, `1..4-edits`, `5..24-edits`, `25..99-edits`, `100..-edits`

</details>

### top_by_edits
`top_by_edits(project, date, editor_type='all-editor-types', page_type='all-page-types')`

List most-edited pages by number of edits.

<details>
<summary>Parameters</summary>

- `project` (str): The Wikimedia project to look at, e.g. `en.wikipedia.org`, `all-wikipedia-projects`, `all-projects`
- `date` (str): Date. YYYYMMDD, ISO format, or human-readable.
- `editor_type` (str): Type of editor.
   Allowed: `all-editor-types`, `anonymous`, `group-bot` (registered accounts belonging to the bot group), `name-bot` (registered accounts with bot-like names), `user`
- `page_type` (str): Type of page.
   Allowed: `all-page-types`, `content` (articles), `non-content` (e.g. discussion pages)

</details>

### top_by_net_diff
`top_by_net_diff(project, date, editor_type='all-editor-types', page_type='all-page-types')`

List most-edited pages by net byte change (additions minus deletions).

<details>
<summary>Parameters</summary>

- `project` (str): The Wikimedia project to look at, e.g. `en.wikipedia.org`, `all-wikipedia-projects`, `all-projects`
- `date` (str): Date. YYYYMMDD, ISO format, or human-readable.
- `editor_type` (str): Type of editor.
   Allowed: `all-editor-types`, `anonymous`, `group-bot` (registered accounts belonging to the bot group), `name-bot` (registered accounts with bot-like names), `user`
- `page_type` (str): Type of page.
   Allowed: `all-page-types`, `content` (articles), `non-content` (e.g. discussion pages)

</details>

### top_by_abs_diff
`top_by_abs_diff(project, date, editor_type='all-editor-types', page_type='all-page-types')`

List most-edited pages by absolute byte change (additions plus deletions).

<details>
<summary>Parameters</summary>

- `project` (str): The Wikimedia project to look at, e.g. `en.wikipedia.org`, `all-wikipedia-projects`, `all-projects`
- `date` (str): Date. YYYYMMDD, ISO format, or human-readable.
- `editor_type` (str): Type of editor.
   Allowed: `all-editor-types`, `anonymous`, `group-bot` (registered accounts belonging to the bot group), `name-bot` (registered accounts with bot-like names), `user`
- `page_type` (str): Type of page.
   Allowed: `all-page-types`, `content` (articles), `non-content` (e.g. discussion pages)

</details>