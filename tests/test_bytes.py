from unittest.mock import patch

from wikiedits.client import bytes


@patch('wikiedits.client.bytes_diff_abs_aggregate')
def test_bytes_aggregate_absolute(mock_abs_agg):
  mock_abs_agg.return_value = [
    {"abs_bytes_diff": 100},
    {"abs_bytes_diff": 200},
    {"abs_bytes_diff": 50}
  ]

  result = bytes(
    start="20251101",
    end="20251103",
    diff_type="absolute",
    project="en.wikipedia.org"
  )

  mock_abs_agg.assert_called_once_with(
    project="en.wikipedia.org",
    granularity="daily",
    start="20251101",
    end="20251103",
    editor_type="all-editor-types",
    page_type="all-page-types"
  )
  assert result == 350


@patch('wikiedits.client.bytes_diff_net_aggregate')
def test_bytes_aggregate_net(mock_net_agg):
  mock_net_agg.return_value = [
    {"net_bytes_diff": -50},
    {"net_bytes_diff": 150},
    {"net_bytes_diff": -25}
  ]

  result = bytes(
    start="20251101",
    end="20251103",
    diff_type="net",
    project="fr.wikipedia.org"
  )

  mock_net_agg.assert_called_once_with(
    project="fr.wikipedia.org",
    granularity="daily",
    start="20251101",
    end="20251103",
    editor_type="all-editor-types",
    page_type="all-page-types"
  )
  assert result == 75


@patch('wikiedits.client.bytes_diff_abs_per_page')
def test_bytes_per_page_absolute(mock_abs_per_page):
  mock_abs_per_page.return_value = [
    {"abs_bytes_diff": 75},
    {"abs_bytes_diff": 125}
  ]

  result = bytes(
    start="20251101",
    end="20251102",
    diff_type="absolute",
    project="es.wikipedia.org",
    page_title="Test_Page"
  )

  mock_abs_per_page.assert_called_once_with(
    project="es.wikipedia.org",
    page_title="Test_Page",
    granularity="daily",
    start="20251101",
    end="20251102",
    editor_type="all-editor-types"
  )
  assert result == 200


@patch('wikiedits.client.bytes_diff_net_per_page')
def test_bytes_per_page_net(mock_net_per_page):
  mock_net_per_page.return_value = [
    {"net_bytes_diff": 40},
    {"net_bytes_diff": -10},
    {"net_bytes_diff": 30}
  ]

  result = bytes(
    start="20251101",
    end="20251103",
    diff_type="net",
    project="de.wikipedia.org",
    page_title="Another_Page"
  )

  mock_net_per_page.assert_called_once_with(
    project="de.wikipedia.org",
    page_title="Another_Page",
    granularity="daily",
    start="20251101",
    end="20251103",
    editor_type="all-editor-types"
  )
  assert result == 60


def test_bytes_with_custom_parameters():
  with patch('wikiedits.client.bytes_diff_abs_aggregate') as mock_abs_agg:
    mock_abs_agg.return_value = [{"abs_bytes_diff": 500}]

    result = bytes(
      start="20251201",
      end="20251201",
      diff_type="absolute",
      project="ja.wikipedia.org",
      editor_type="user",
      page_type="content"
    )

    mock_abs_agg.assert_called_once_with(
      project="ja.wikipedia.org",
      granularity="daily",
      start="20251201",
      end="20251201",
      editor_type="user",
      page_type="content"
    )
    assert result == 500


def test_bytes_empty_response():
  with patch('wikiedits.client.bytes_diff_net_aggregate') as mock_net_agg:
    mock_net_agg.return_value = []

    result = bytes(
      start="20251101",
      end="20251101",
      diff_type="net"
    )

    assert result == 0


def test_bytes_zero_values():
  with patch('wikiedits.client.bytes_diff_abs_per_page') as mock_abs_per_page:
    mock_abs_per_page.return_value = [
      {"abs_bytes_diff": 0},
      {"abs_bytes_diff": 0}
    ]

    result = bytes(
      start="20251101",
      end="20251102",
      diff_type="absolute",
      page_title="Empty_Page"
    )

    assert result == 0
