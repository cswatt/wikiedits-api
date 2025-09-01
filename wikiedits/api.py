import requests

__version__ = "0.1.0"

BASE_URL = "https://wikimedia.org/api/rest_v1/metrics"

DEFAULT_HEADERS = {
  "User-Agent": "wikiedits-api/{version}".format(version=__version__),
  "Accept": "application/json"
}

# number of new pages
NP_ENDPOINT = "edited-pages/new"
NP_ARGS = "{project}/{editor_type}/{page_type}/{granularity}/{start}/{end}"

def _make_request(endpoint, args, api_base_url=BASE_URL):
  url = "/".join([api_base_url, endpoint, args])
  response = requests.get(url, headers=DEFAULT_HEADERS, timeout=30)
  return response.json()

def new_pages(project, start, end,
              editor_type='all-editor-types', page_type='all-page-types', granularity='daily'):
  args = NP_ARGS.format(project=project,
                        editor_type=editor_type,
                        page_type=page_type,
                        granularity=granularity,
                        start=start,
                        end=end)
  return _make_request(NP_ENDPOINT, args)
  