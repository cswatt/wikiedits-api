# Function reference

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

### Basic API wrappers

Wrapper functions for all endpoints in the [Wikimedia Edit Analytics API][https://doc.wikimedia.org/generated-data-platform/aqs/analytics-api/reference/edits.html].

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