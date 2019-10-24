import base64
import datetime
import json
import pathlib
import sys
import urllib.request


metrics = [
  ('clones-count', 'clones', 'count'),
  ('clones-uniques', 'clones', 'uniques'),
  ('views-count', 'views', 'count'),
  ('views-uniques', 'views', 'uniques')
]

#https://stackoverflow.com/questions/29708708/http-basic-authentication-not-working-in-python-3-4
def fetch_repo_data(username, token, org, repo, stat_type, field_name):
  url = f'https://api.github.com/repos/{org}/{repo}/traffic/{stat_type}'
  req = urllib.request.Request(url)
  credentials = ('%s:%s' % (username,token))
  encoded_credentials = base64.b64encode(credentials.encode('ascii'))
  req.add_header('Authorization', 'Basic %s' % encoded_credentials.decode("ascii"))
  resp_json = json.loads(urllib.request.urlopen(req).read())
  return dict([(item['timestamp'], item[field_name]) for item in resp_json[stat_type]])


def check_completeness(label, date_count_dict):
  def parse_time(time_str):
    return datetime.datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%SZ')
  first_day_str = min(date_count_dict.keys())
  last_day_str = max(date_count_dict.keys())
  num_days_in_range = (parse_time(last_day_str) - parse_time(first_day_str)).days + 1
  complete = num_days_in_range == len(date_count_dict)
  summary = {}
  summary['start-date'] = first_day_str
  summary['end-date'] = last_day_str
  summary['num-days'] = len(date_count_dict)
  summary['complete'] = complete
  return summary


def update_repo_data(conf, org, repo):
  filepath = pathlib.Path(conf['base_dir']) / f'{org}-{repo}.json'
  if filepath.exists():
    with open(filepath) as f:
      repo_data_so_far = json.load(f)
  else:
    repo_data_so_far = {}
    for label in [m[0] for m in metrics]:
      repo_data_so_far[label] = {}
  totals = {}
  for label, stat_type, field_name in metrics:
    metric_data = fetch_repo_data(conf['username'], conf['token'], org, repo, stat_type, field_name)
    repo_data_so_far[label].update(metric_data)
    totals[label] = sum(repo_data_so_far[label].values())
    # FUTURE: check all metrics for completeness?
    last_summary = check_completeness(label, repo_data_so_far[label])
  repo_data_so_far['summary'] = last_summary
  repo_data_so_far['totals'] = totals
  with open(filepath, 'w') as f:
    json.dump(repo_data_so_far, f, indent=2)


def main():
  if len(sys.argv) < 2:
    print('Please give configuration file in json')
    exit()
  with open(sys.argv[1]) as f:
    conf = json.load(f)
  for repo in conf['repos']:
    update_repo_data(conf, repo['org'], repo['repo'])


if __name__ == "__main__":
    main()
